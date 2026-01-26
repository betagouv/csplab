"""Client for Talentsoft API."""

import asyncio
from http import HTTPStatus
from time import time
from typing import Any, Dict, List, Optional, Tuple, cast

from pydantic import HttpUrl, ValidationError

from domain.services.async_http_client_interface import IAsyncHttpResponse
from domain.services.logger_interface import ILogger
from infrastructure.exceptions.exceptions import ExternalApiError
from infrastructure.external_gateways.dtos.talentsoft_dtos import (
    CachedToken,
    TalentsoftOffer,
    TalentsoftOffersResponse,
    TalentsoftTokenResponse,
)
from infrastructure.gateways.shared.async_http_client import AsyncHttpClient

TOKEN_ENDPOINT = "/api/token"  # noqa
OFFERS_ENDPOINT = "/api/v2/offersummaries"


class TalentsoftFrontClient(AsyncHttpClient):
    """Client for interacting with Talentsoft API Front."""

    def __init__(
        self,
        base_url: HttpUrl,
        client_id: str,
        client_secret: str,
        logger_service: ILogger,
        **kwargs,
    ):
        """Initialize client with config and logger."""
        timeout = kwargs.get("timeout", 30)
        max_retries = kwargs.get("max_retries", 2)

        super().__init__(timeout=timeout)
        self.base_url = base_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.max_retries = max_retries
        self.cached_token: Optional[CachedToken] = None
        self.logger = logger_service.get_logger("TalentsoftClient")
        self._token_lock = asyncio.Lock()

    async def _fetch_new_token(self) -> str:
        """Fetch a new access token."""
        url = f"{self.base_url}{TOKEN_ENDPOINT}"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        data = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
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
        except ValidationError as exc:
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
    ) -> Tuple[List[TalentsoftOffer], bool]:
        """Fetch job offers from Talentsoft API Front."""
        url = f"{self.base_url}{OFFERS_ENDPOINT}"
        params = {"count": count, "start": start}

        response = await self._make_authenticated_request(url, params)

        try:
            typed_response = TalentsoftOffersResponse.model_validate(response.json())
            offers = typed_response.data
            pagination = typed_response.pagination
        except ValidationError as e:
            raise ExternalApiError(
                f"Invalid response structure: {e}", api_name="Talentsoft Front API"
            ) from e

        has_more = pagination.hasMore

        return offers, has_more
