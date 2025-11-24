"""Client for PISTE API authentication and INGRES API calls."""

import time

import environ
import requests
from rest_framework import status

from apps.ingestion.infrastructure.exceptions import (
    ExternalApiError,
)
from core.services.http_client_interface import IHttpClient
from core.services.logger_interface import ILogger


class PisteClient:
    """Client for interacting with PISTE OAuth and INGRES APIs."""

    def __init__(self, http_client: IHttpClient, logger_service: ILogger):
        """Initialize with HTTP client."""
        self.http_client = http_client
        self.logger = logger_service.get_logger("PisteClient")
        env = environ.Env()
        self.oauth_base_url = env.str("TYCHO_PISTE_OAUTH_BASE_URL")
        self.ingres_base_url = env.str("TYCHO_INGRES_BASE_URL")
        self.client_id = env.str("TYCHO_INGRES_CLIENT_ID")
        self.client_secret = env.str("TYCHO_INGRES_CLIENT_SECRET")
        self.access_token = None
        self.expires_at = 0
        self.logger.info("Initializing PisteClient")
        self.logger.debug(f"OAuth URL: {self.oauth_base_url}")

    def _get_token(self):
        """Get OAuth token from PISTE API."""
        oauth_url = f"{self.oauth_base_url}/api/oauth/token"
        response = self.http_client.request(
            "POST",
            oauth_url,
            headers={
                "Accept": "application/json",
            },
            data={
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "scope": "openid",
            },
        )
        if response.status_code != status.HTTP_200_OK:
            error_msg = f"OAuth failed: {response.status_code} - {response.text}"
            self.logger.error(error_msg)
            raise ExternalApiError(
                error_msg,
                details={
                    "status_code": response.status_code,
                    "response_text": response.text,
                    "oauth_url": oauth_url,
                },
            )

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

        url = f"{self.ingres_base_url}/{endpoint}"

        self.logger.info(f"Making {method} request to: {url}")

        response = self.http_client.request(method, url, **kwargs)

        self.logger.info(f"API response status: {response.status_code}")

        if response.status_code != status.HTTP_200_OK:
            error_msg = f"INGRES API error: {response.status_code} - {response.text}"
            self.logger.error(f"API response text: {response.text[:500]}...")

            raise ExternalApiError(
                error_msg,
                status_code=response.status_code,
                details={
                    "ingres_status": response.status_code,
                    "method": method,
                    "endpoint": endpoint,
                    "response_text": response.text,
                },
            )

        return response
