"""
Pure API layer for /api/v2/offersummaries.

Responsibilities:
- Execute the GET request with proper Authorization header
- No mapping / no business transformation
"""

from __future__ import annotations

from typing import Any, Dict, Optional

import requests

from apps.ingestion.config import TalentSoftConfig
from core.services.logger_interface import ILogger

from .exceptions import TalentSoftApiError


class OfferSummariesApi:
    """HTTP calls for TalentSoft offer summaries."""

    ENDPOINT = "/api/v2/offersummaries"

    def __init__(
        self,
        config: TalentSoftConfig,
        logger_service: ILogger,
        session: requests.Session,
        timeout: int = 30,
    ):
        self._config = config
        self._logger = logger_service.get_logger("OfferSummariesApi")
        self._session = session
        self._timeout = timeout

    def _build_url(self) -> str:
        base = str(self._config.base_url).rstrip("/")
        path = self.ENDPOINT.lstrip("/")
        return f"{base}/{path}"

    def fetch(self, bearer_token: str, params: Optional[Dict[str, Any]] = None) -> requests.Response:
        """GET /api/v2/offersummaries with Bearer token."""
        url = self._build_url()
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {bearer_token}",
        }

        self._logger.info("TalentSoft offersummaries call: GET %s", url)

        try:
            return self._session.get(url, headers=headers, params=params, timeout=self._timeout)
        except requests.RequestException as exc:
            self._logger.exception("TalentSoft offersummaries request failed (network)")
            raise TalentSoftApiError(f"TalentSoft offersummaries request failed: {exc}") from exc
