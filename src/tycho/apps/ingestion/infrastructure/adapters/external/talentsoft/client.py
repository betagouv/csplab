"""
High-level TalentSoft HTTP client.

Responsibilities:
- Provide `request(method, endpoint, **kwargs)` used by the existing facade
- Automatically obtain Bearer token
- Retry once on 401 (force token refresh)
- Normalize /api/v2/offersummaries response to {"offers":[...]} for ingestion compatibility
"""

from __future__ import annotations

import json
from typing import Any, Dict, Optional

import requests

from apps.ingestion.config import TalentSoftConfig
from core.services.logger_interface import ILogger

from .exceptions import TalentSoftApiError, TalentSoftAuthError
from .offersummaries_api import OfferSummariesApi
from .offersummaries_mapper import OfferSummariesMapper
from .token_service import TalentSoftTokenService


class TalentSoftHttpClient:
    """Real TalentSoft client with token + endpoint-specific normalization."""

    OFFER_SUMMARIES_ENDPOINT = "/api/v2/offersummaries"

    def __init__(
        self,
        config: TalentSoftConfig,
        logger_service: ILogger,
        timeout: int = 30,
        session: Optional[requests.Session] = None,
    ):
        self._config = config
        self._logger = logger_service.get_logger("TalentSoftHttpClient")
        self._timeout = timeout
        self._session = session or requests.Session()

        self._token_service = TalentSoftTokenService(
            config=config,
            logger_service=logger_service,
            session=self._session,
            timeout=timeout,
        )
        self._offers_api = OfferSummariesApi(
            config=config,
            logger_service=logger_service,
            session=self._session,
            timeout=timeout,
        )

    # -------------------------
    # URL helpers
    # -------------------------

    def _build_url(self, endpoint: str) -> str:
        if endpoint.startswith("http://") or endpoint.startswith("https://"):
            return endpoint
        base = str(self._config.base_url).rstrip("/")
        path = endpoint.lstrip("/")
        return f"{base}/{path}"

    def _is_offersummaries(self, endpoint: str) -> bool:
        ep = endpoint.strip()
        if ep.startswith("http://") or ep.startswith("https://"):
            return ep.rstrip("/").endswith(self.OFFER_SUMMARIES_ENDPOINT.rstrip("/"))
        return ep.lstrip("/").rstrip("/").endswith(self.OFFER_SUMMARIES_ENDPOINT.lstrip("/").rstrip("/"))

    # -------------------------
    # Public API (compat)
    # -------------------------

    def request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """
        Main entrypoint used by the facade.

        If endpoint is /api/v2/offersummaries:
          - calls offersummaries api
          - maps payload to {"offers": [...]}
          - returns a Response containing normalized JSON

        Otherwise:
          - performs a raw request with Bearer token (no mapping)
        """
        method_upper = method.upper().strip()

        if self._is_offersummaries(endpoint):
            return self._request_offersummaries(params=kwargs.get("params"))

        # Default: raw request with bearer token
        token = self._token_service.get_access_token()
        headers = dict(kwargs.get("headers") or {})
        headers.setdefault("Accept", "application/json")
        headers["Authorization"] = f"Bearer {token.access_token}"

        url = self._build_url(endpoint)
        self._logger.info("TalentSoft API call: %s %s", method_upper, url)

        try:
            resp = self._session.request(
                method=method_upper,
                url=url,
                headers=headers,
                params=kwargs.get("params"),
                data=kwargs.get("data"),
                json=kwargs.get("json"),
                timeout=self._timeout,
            )
        except requests.RequestException as exc:
            self._logger.exception("TalentSoft request failed (network): %s %s", method_upper, url)
            raise TalentSoftApiError(f"TalentSoft request failed: {exc}") from exc

        # retry once on 401
        if resp.status_code == 401:
            self._logger.warning("401 received; refreshing token and retrying once.")
            token = self._token_service.force_refresh()
            headers["Authorization"] = f"Bearer {token.access_token}"

            resp = self._session.request(
                method=method_upper,
                url=url,
                headers=headers,
                params=kwargs.get("params"),
                data=kwargs.get("data"),
                json=kwargs.get("json"),
                timeout=self._timeout,
            )

        return resp

    # -------------------------
    # Offersummaries flow
    # -------------------------

    def _request_offersummaries(self, params: Optional[Dict[str, Any]] = None) -> requests.Response:
        """
        Full flow for /api/v2/offersummaries:
        - get token
        - call endpoint
        - retry once on 401
        - normalize JSON
        """
        token = self._token_service.get_access_token()
        resp = self._offers_api.fetch(bearer_token=token.access_token, params=params)

        if resp.status_code == 401:
            self._logger.warning("offersummaries returned 401; refreshing token and retrying once.")
            token = self._token_service.force_refresh()
            resp = self._offers_api.fetch(bearer_token=token.access_token, params=params)

        if resp.status_code >= 400:
            preview = (resp.text or "")[:500]
            self._logger.error("offersummaries failed: %s - %s", resp.status_code, preview)
            raise TalentSoftApiError(f"TalentSoft offersummaries failed: {resp.status_code}")

        # Normalize content to {"offers":[...]}
        return self._normalize_offersummaries_response(resp)

    def _normalize_offersummaries_response(self, upstream: requests.Response) -> requests.Response:
        """Create a new Response that contains the normalized payload."""
        try:
            payload = upstream.json() if upstream.content else {}
        except ValueError:
            payload = {}

        normalized = OfferSummariesMapper.map_payload(payload)
        offers_count = len(normalized.get("offers") or [])
        self._logger.info("Normalized offersummaries payload: %s offers", offers_count)

        # Build a new response to avoid side effects on the upstream response object
        new_resp = requests.Response()
        new_resp.status_code = upstream.status_code
        new_resp.headers = dict(upstream.headers)
        new_resp.encoding = "utf-8"
        new_resp._content = json.dumps(normalized, ensure_ascii=False).encode("utf-8")
        new_resp.headers["Content-Type"] = "application/json; charset=utf-8"
        new_resp.url = upstream.url

        return new_resp
