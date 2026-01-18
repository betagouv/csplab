"""Client for Talentsoft API."""

import asyncio
from http import HTTPStatus
from time import time
from typing import Any, Dict, List, Optional, Tuple, cast

from domain.services.async_http_client_interface import IAsyncHttpResponse
from domain.services.logger_interface import ILogger
from domain.types import JsonDataType
from infrastructure.exceptions.exceptions import ExternalApiError
from infrastructure.external_gateways.configs.talentsoft_config import TalentsoftConfig
from infrastructure.external_gateways.dtos.talentsoft_dtos import (
    CachedToken,
    TalentsoftTokenResponse,
)
from infrastructure.gateways.shared.async_http_client import AsyncHttpClient

TOKEN_ENDPOINT = "/api/token"  # noqa
OFFERS_ENDPOINT = "/api/v2/offersummaries"


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

    def _build_auth_headers(self, token: str) -> Dict[str, str]:
        """Build headers with authorization token."""
        return {
            "Accept": "application/json",
            "Authorization": f"Bearer {token}",
        }

    async def _make_authenticated_request(
        self, url: str, params: Dict[str, int]
    ) -> IAsyncHttpResponse:
        """Make HTTP request with automatic retry on 401."""
        token = await self.get_access_token()

        for attempt in range(self.max_retries + 1):
            try:
                response = await self.get(
                    url, headers=self._build_auth_headers(token), params=params
                )

                if (
                    response.status_code == HTTPStatus.UNAUTHORIZED
                    and attempt < self.max_retries
                ):
                    self.logger.info(
                        "Token expired, fetching new token (attempt %d)", attempt + 1
                    )
                    self.cached_token = None
                    token = await self.get_access_token()
                    continue

                response.raise_for_status()
                return response

            except Exception as exc:
                if attempt == self.max_retries:
                    self.logger.exception(
                        "Failed to get response from Talentsoft API Front: %s", url
                    )
                    raise ExternalApiError(
                        message=f"Request failed after retries: {exc}",
                        api_name="Talentsoft Front API",
                    ) from exc

                self.logger.warning(
                    "Request attempt %d failed, retrying: %s", attempt + 1, exc
                )

        # This should never be reached, but added for type safety
        raise ExternalApiError(
            message="Unexpected end of retry loop",
            api_name="Talentsoft Front API",
        )

    async def get_offers(
        self, count: int = 1000, start: int = 1
    ) -> Tuple[List[JsonDataType], bool]:
        """Fetch job offers from Talentsoft API Front."""
        url = f"{self.config.base_url}{OFFERS_ENDPOINT}"
        params = {"count": count, "start": start}

        response = await self._make_authenticated_request(url, params)
        json = response.json()

        # TO BE REVIEWED REGARDING JsonDataType
        payload = cast(Dict[str, Any], json)

        offers = payload.get("data", [])
        if not isinstance(offers, list):
            offers = []

        has_more = bool(payload.get("_pagination", {}).get("hasMore", False))

        return offers, has_more
