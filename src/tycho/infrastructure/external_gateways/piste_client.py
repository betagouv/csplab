import time

import httpx
from pydantic import BaseModel

from config.app_config import PisteConfig
from domain.services.async_http_client_interface import IAsyncHttpResponse
from domain.services.logger_interface import ILogger
from infrastructure.exceptions.exceptions import ExternalApiError
from infrastructure.gateways.shared.async_http_client import AsyncHttpClient


class OAuthTokenResponse(BaseModel):
    access_token: str
    expires_in: int


class PisteClient(AsyncHttpClient):
    def __init__(
        self,
        config: PisteConfig,
        logger_service: ILogger,
        timeout: int = 30,
    ):
        super().__init__(timeout=timeout)
        self.config = config
        self.logger = logger_service
        self.access_token = None
        self.expires_at = 0
        self.logger.info("Initializing PisteClient")
        self.logger.debug("OAuth URL: %s", self.config.oauth_base_url)

    async def _get_token(self):
        oauth_url = f"{self.config.oauth_base_url}api/oauth/token"
        response = await super().post(
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
        except httpx.HTTPStatusError as err:
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

        try:
            token_data = OAuthTokenResponse.model_validate(response.json())
        except Exception as err:
            error_msg = "Invalid OAuth response format"
            self.logger.error(error_msg)
            raise ExternalApiError(
                error_msg,
                details={
                    "oauth_url": oauth_url,
                },
            ) from err

        self.access_token = token_data.access_token
        self.expires_at = time.time() + token_data.expires_in
        self.logger.info("OAuth token obtained successfully")

    async def _ensure_token(self):
        if not self.access_token or time.time() >= self.expires_at:
            await self._get_token()

    async def get(self, url: str, headers=None, params=None) -> IAsyncHttpResponse:
        await self._ensure_token()

        # Construct full URL
        full_url = f"{self.config.ingres_base_url}/{url}"

        # Add authorization header
        if headers is None:
            headers = {}
        headers["Authorization"] = f"Bearer {self.access_token}"

        self.logger.info("Making GET request to: %s", full_url)

        try:
            response = await super().get(full_url, headers=headers, params=params)
            self.logger.info("API response status: %d", response.status_code)
            response.raise_for_status()
            return response
        except httpx.HTTPStatusError as err:
            self.logger.error("INGRES API error: %d", response.status_code)
            raise ExternalApiError(
                f"INGRES API error: {response.status_code}",
                status_code=response.status_code,
                details={
                    "ingres_status": response.status_code,
                    "method": "GET",
                    "url": full_url,
                    "response_text": response.text,
                },
            ) from err

    async def post(
        self, url: str, headers=None, files=None, data=None, json=None
    ) -> IAsyncHttpResponse:
        await self._ensure_token()

        # Construct full URL
        full_url = f"{self.config.ingres_base_url}/{url}"

        # Add authorization header
        if headers is None:
            headers = {}
        headers["Authorization"] = f"Bearer {self.access_token}"

        self.logger.info("Making POST request to: %s", full_url)

        try:
            response = await super().post(
                full_url, headers=headers, files=files, data=data, json=json
            )
            self.logger.info("API response status: %d", response.status_code)
            response.raise_for_status()
            return response
        except httpx.HTTPStatusError as err:
            error_msg = "INGRES API error: %d"
            self.logger.error(error_msg, response.status_code)
            raise ExternalApiError(
                f"INGRES API error: {response.status_code}",
                status_code=response.status_code,
                details={
                    "ingres_status": response.status_code,
                    "method": "POST",
                    "url": full_url,
                    "response_text": response.text,
                },
            ) from err
