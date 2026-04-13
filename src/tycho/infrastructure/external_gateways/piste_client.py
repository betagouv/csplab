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
        self.logger.debug(f"OAuth URL: {self.config.oauth_base_url}")

    async def _get_token(self):
        oauth_url = f"{self.config.oauth_base_url}api/oauth/token"
        response = await self.post(
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
            error_msg = f"Invalid OAuth response format: {response.text}"
            self.logger.error(error_msg)
            raise ExternalApiError(
                error_msg,
                details={
                    "response_text": response.text,
                    "oauth_url": oauth_url,
                },
            ) from err

        self.access_token = token_data.access_token
        self.expires_at = time.time() + token_data.expires_in
        self.logger.info("OAuth token obtained successfully")

    async def _ensure_token(self):
        if not self.access_token or time.time() >= self.expires_at:
            await self._get_token()

    async def request(self, method: str, url: str, **kwargs) -> IAsyncHttpResponse:
        await self._ensure_token()
        headers = kwargs.get("headers", {})
        headers["Authorization"] = f"Bearer {self.access_token}"
        kwargs["headers"] = headers

        url = f"{self.config.ingres_base_url}/{url}"

        self.logger.info(f"Making {method} request to: {url}")

        if method.upper() == "GET":
            response = await self.get(url, headers=headers, params=kwargs.get("params"))
        elif method.upper() == "POST":
            response = await self.post(
                url,
                headers=headers,
                data=kwargs.get("data"),
                json=kwargs.get("json"),
                files=kwargs.get("files"),
            )
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")

        self.logger.info(f"API response status: {response.status_code}")

        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as err:
            error_msg = f"INGRES API error: {response.status_code}"

            raise ExternalApiError(
                error_msg,
                status_code=response.status_code,
                details={
                    "ingres_status": response.status_code,
                    "method": method,
                    "url": url,
                    "response_text": response.text,
                },
            ) from err

        return response
