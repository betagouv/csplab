"""
Token service for TalentSoft.

Responsibilities:
- Call POST /api/token with body params: grant_type, client_id, client_secret
- Cache token in memory
- Refresh on expiry
"""

from __future__ import annotations

import time
from typing import Optional

import requests

from apps.ingestion.config import TalentSoftConfig
from core.services.logger_interface import ILogger

from ..dtos.talentsoft_token_dto import CachedToken, TalentSoftTokenResponse
from .credentials import parse_credentials
from .exceptions import TalentSoftAuthError


class TalentSoftTokenService:
    """Retrieve and cache OAuth2 access token for TalentSoft."""

    TOKEN_ENDPOINT = "api/token"

    def __init__(
        self,
        config: TalentSoftConfig,
        logger_service: ILogger,
        session: requests.Session,
        timeout: int = 30,
    ):
        self._config = config
        self._logger = logger_service.get_logger("TalentSoftTokenService")
        self._session = session
        self._timeout = timeout
        self._cached: Optional[CachedToken] = None

    def _build_url(self, endpoint: str) -> str:
        base = str(self._config.base_url).rstrip("/")
        path = endpoint.lstrip("/")
        return f"{base}/{path}"

    def get_access_token(self) -> CachedToken:
        """Return a valid cached token, fetching a new one if needed."""
        if self._cached is None or self._cached.is_expired():
            self._cached = self._fetch_token()
        return self._cached

    def force_refresh(self) -> CachedToken:
        """Force token refresh (used on 401 retry)."""
        self._cached = self._fetch_token()
        return self._cached

    def _fetch_token(self) -> CachedToken:
        """
        POST /api/token with x-www-form-urlencoded body:
          grant_type=client_credentials&client_id=XXX&client_secret=YYY
        """
        try:
            creds = parse_credentials(self._config.api_key)
        except ValueError as exc:
            raise TalentSoftAuthError(str(exc)) from exc

        url = self._build_url(self.TOKEN_ENDPOINT)

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        # IMPORTANT: body parameters exactly as required
        data = {
            "grant_type": creds.grant_type,
            "client_id": creds.client_id,
            "client_secret": creds.client_secret,
        }

        self._logger.info("Requesting TalentSoft token: POST %s", url)

        try:
            response = self._session.post(url, headers=headers, data=data, timeout=self._timeout)
        except requests.RequestException as exc:
            self._logger.exception("TalentSoft token request failed (network)")
            raise TalentSoftAuthError(f"TalentSoft token request failed: {exc}") from exc

        if response.status_code >= 400:
            preview = (response.text or "")[:500]
            self._logger.error("TalentSoft token request failed: %s - %s", response.status_code, preview)
            raise TalentSoftAuthError(f"TalentSoft token request failed: {response.status_code}")

        try:
            payload = response.json() if response.content else {}
        except ValueError:
            payload = {}

        access_token = str(payload.get("access_token") or "")
        token_type = str(payload.get("token_type") or "bearer")
        refresh_token = payload.get("refresh_token")

        expires_in_raw = payload.get("expires_in")
        try:
            expires_in = int(expires_in_raw)
        except (TypeError, ValueError):
            expires_in = 0

        if not access_token:
            self._logger.error("TalentSoft token response missing access_token: %s", payload)
            raise TalentSoftAuthError("TalentSoft token response missing access_token")

        
        if expires_in <= 0:
            expires_in = 10 * 60

        token_response = TalentSoftTokenResponse(
            access_token=access_token,
            token_type=token_type,
            expires_in=expires_in,
            refresh_token=str(refresh_token) if refresh_token else None,
        )

        cached = CachedToken(
            access_token=token_response.access_token,
            token_type=token_response.token_type,
            expires_at_epoch=time.time() + token_response.expires_in,
            refresh_token=token_response.refresh_token,
        )

        self._logger.info("TalentSoft token retrieved (expires_in=%ss)", expires_in)
        return cached
