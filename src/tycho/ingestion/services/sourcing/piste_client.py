"""Client for PISTE API authentication and INGRES API calls."""

import logging
import time

import environ
import requests

logger = logging.getLogger(__name__)

# HTTP status constants
HTTP_OK = 200


class PisteClient:
    """Client for interacting with PISTE OAuth and INGRES APIs."""

    def __init__(self):
        """Initialize PisteClient with environment variables."""
        env = environ.Env()
        self.oauth_base_url = env.str("TYCHO_PISTE_OAUTH_BASE_URL")
        self.ingres_base_url = env.str("TYCHO_INGRES_BASE_URL")
        self.client_id = env.str("TYCHO_INGRES_CLIENT_ID")
        self.client_secret = env.str("TYCHO_INGRES_CLIENT_SECRET")
        self.access_token = None
        self.expires_at = 0
        logger.info("Initializing PisteClient")
        logger.debug(f"OAuth URL: {self.oauth_base_url}")

    def _get_token(self):
        """Get OAuth token from PISTE API."""
        oauth_url = f"{self.oauth_base_url}/api/oauth/token"
        response = requests.post(
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
            timeout=30,
        )
        if response.status_code != HTTP_OK:
            error_msg = f"OAuth failed: {response.status_code} - {response.text}"
            logger.error(error_msg)
            raise Exception(error_msg)

        data = response.json()
        self.access_token = data["access_token"]
        self.expires_at = time.time() + data["expires_in"]
        logger.info("OAuth token obtained successfully")

    def _ensure_token(self):
        if not self.access_token or time.time() >= self.expires_at:
            self._get_token()

    def request(self, method, endpoint, **kwargs):
        """Make authenticated request to INGRES API."""
        self._ensure_token()
        headers = kwargs.get("headers", {})
        headers["Authorization"] = f"Bearer {self.access_token}"
        kwargs["headers"] = headers

        # Extract timeout from kwargs to avoid duplication
        timeout = kwargs.pop("timeout", 30)
        url = f"{self.ingres_base_url}/{endpoint}"

        logger.info(f"Making {method} request to: {url}")

        response = requests.request(method, url, timeout=timeout, **kwargs)

        logger.info(f"API response status: {response.status_code}")
        if response.status_code != HTTP_OK:
            logger.warning(f"API response text: {response.text[:500]}...")

        return response
