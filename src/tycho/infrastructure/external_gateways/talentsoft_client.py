"""Client for Talentsoft API."""

import asyncio
from http import HTTPStatus
from time import time
from typing import Any, Dict, List, Optional, Tuple, cast

from domain.services.logger_interface import ILogger
from infrastructure.exceptions.exceptions import ExternalApiError
from infrastructure.external_gateways.configs.talentsoft_config import TalentsoftConfig
from infrastructure.external_gateways.dtos.talentsoft_dtos import (
    CachedToken,
    TalentsoftTokenResponse,
)
from infrastructure.gateways.shared.async_http_client import AsyncHttpClient

TOKEN_ENDPOINT = "/api/token"  # noqa


class TalentsoftFrontClient(AsyncHttpClient):
    """Client for interacting with Talentsoft API Front."""

    def __init__(
        self,
        config: TalentsoftConfig,
        logger_service: ILogger,
        timeout: int = 30,
        max_retries: int = 2,
    ):
        """Initialize client with config and logger."""
        super().__init__(timeout=timeout)
        self.config = config
        self.max_retries = max_retries
        self.cached_token: Optional[CachedToken] = None
        self.logger = logger_service.get_logger("TalentsoftClient")
        self._token_lock = asyncio.Lock()

    async def _fetch_new_token(self) -> str:
        """Fetch a new access token."""
        url = f"{self.config.base_url}{TOKEN_ENDPOINT}"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        data = {
            "grant_type": "client_credentials",
            "client_id": self.config.client_id,
            "client_secret": self.config.client_secret,
        }

        try:
            response = await self.post(url, headers=headers, data=data)
            response.raise_for_status()
            payload = response.json()
        except Exception as exc:
            self.logger.exception("Failed to fetch token from Talentsoft API Front")
            raise ExternalApiError(
                message=f"Token request failed: {exc}", api_name="Talentsoft Front API"
            ) from exc

        try:
            typed_payload = cast(Dict[str, Any], payload)  # mypy
            token_response = TalentsoftTokenResponse(**typed_payload)
        except Exception as exc:
            self.logger.error("Invalid token response format: %s", payload)
            raise ExternalApiError(
                message=f"Invalid token response: {exc}",
                api_name="Talentsoft Front API",
            ) from exc

        self.cached_token = CachedToken(
            access_token=token_response.access_token,
            token_type=token_response.token_type,
            expires_at_epoch=time() + token_response.expires_in,
            refresh_token=token_response.refresh_token,
        )
        return self.cached_token.access_token

    async def get_access_token(self) -> str:
        """Get valid access token, refreshing if needed."""
        async with self._token_lock:
            if self.cached_token and self.cached_token.is_valid():
                return self.cached_token.access_token
            return await self._fetch_new_token()
