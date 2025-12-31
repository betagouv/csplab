"""Client for PISTE API authentication and INGRES API calls."""

import time

import requests
from requests.exceptions import HTTPError

from apps.ingestion.config import PisteConfig
from apps.ingestion.infrastructure.adapters.external.http_client import HttpClient
from apps.shared.infrastructure.exceptions import (
    ExternalApiError,
)
from domain.services.logger_interface import ILogger


class PisteClient(HttpClient):
    """Client for interacting with PISTE OAuth and INGRES APIs."""

    def __init__(
        self,
        config: PisteConfig,
        logger_service: ILogger,
        timeout: int = 30,
    ):
        """Initialize with HTTP client."""
        super().__init__(timeout=timeout)
        self.config = config
        self.logger = logger_service.get_logger("INFRASTRUCTURE")
        self.access_token = None
        self.expires_at = 0
        self.logger.info("Initializing PisteClient")
        self.logger.debug(f"OAuth URL: {self.config.oauth_base_url}")

    def _get_token(self):
        """Get OAuth token from PISTE API."""
        oauth_url = f"{self.config.oauth_base_url}api/oauth/token"
        response = super().request(
            "POST",
            oauth_url,
            headers={
                "Accept": "application/json",
            },
            data={
                "grant_type": "client_credentials",
                "client_id": self.config.client_id,
                "client_secret": self.config.client_secret,
                "scope": "openid",
            },
        )
        try:
            response.raise_for_status()
        except HTTPError as err:
            error_msg = f"OAuth failed: {response.status_code} - {response.text}"
            self.logger.error(error_msg)
            raise ExternalApiError(
                error_msg,
                details={
                    "status_code": response.status_code,
                    "response_text": response.text,
                    "oauth_url": oauth_url,
                },
            ) from err

        data = response.json()
        self.access_token = data["access_token"]
        self.expires_at = time.time() + data["expires_in"]
        self.logger.info("OAuth token obtained successfully")

    def _ensure_token(self):
        if not self.access_token or time.time() >= self.expires_at:
            self._get_token()

    def request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Make authenticated request to INGRES API."""
        self._ensure_token()
        headers = kwargs.get("headers", {})
        headers["Authorization"] = f"Bearer {self.access_token}"
        kwargs["headers"] = headers

        url = f"{self.config.ingres_base_url}/{endpoint}"

        self.logger.info(f"Making {method} request to: {url}")

        response = super().request(method, url, **kwargs)

        self.logger.info(f"API response status: {response.status_code}")

        try:
            response.raise_for_status()
        except HTTPError as err:
            error_msg = f"INGRES API error: {response.status_code}"

            raise ExternalApiError(
                error_msg,
                status_code=response.status_code,
                details={
                    "ingres_status": response.status_code,
                    "method": method,
                    "endpoint": endpoint,
                    "response_text": response.text,
                },
            ) from err

        return response
