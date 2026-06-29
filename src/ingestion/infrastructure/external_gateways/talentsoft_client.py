import asyncio
import logging
from dataclasses import dataclass
from http import HTTPStatus
from time import time
from typing import Any, Dict, List, Mapping, Optional, Tuple, cast

from pydantic import ValidationError

from domain.entities.raw_offer import RawOffer
from domain.gateways.offers_gateway import IOffersGateway
from infrastructure.exceptions.exceptions import ExternalApiError
from infrastructure.external_gateways.dtos.talentsoft_dtos import (
    CachedToken,
    TalentsoftDetailOffer,
    TalentsoftOffer,
    TalentsoftOffersResponse,
    TalentsoftTokenResponse,
)
from infrastructure.gateways.async_http_client import AsyncHttpClient

TOKEN_ENDPOINT = "/api/token"  # noqa
OFFERS_ENDPOINT = "/api/v2/offersummaries"
DETAIL_OFFER_ENDPOINT = "/api/v2/offers/getoffer"


@dataclass
class TalentsoftConfig:
    base_url: str
    client_id: str
    client_secret: str

    def __post_init__(self) -> None:
        self.base_url = self.base_url.rstrip("/")


class BaseTalentsoftClient(AsyncHttpClient):
    api_name: str

    def __init__(  # noqa: PLR0913
        self,
        base_url: str,
        client_id: str,
        client_secret: str,
        logger: logging.Logger,
        timeout: int = 30,
        max_retries: int = 2,
    ):
        super().__init__(timeout=timeout)
        self.base_url = base_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.max_retries = max_retries
        self.logger = logger
        self.cached_token: Optional[CachedToken] = None
        self._token_lock = asyncio.Lock()

    async def _fetch_new_token(self) -> str:
        url = f"{self.base_url}{TOKEN_ENDPOINT}"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        data: Dict[str, str] = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }

        for attempt in range(self.max_retries + 1):
            try:
                response = await self.post(url, headers=headers, data=data)
                response.raise_for_status()
                payload = response.json()
                break
            except Exception as exc:
                if attempt == self.max_retries:
                    self.logger.error("Failed to fetch token from %s", self.api_name)
                    raise ExternalApiError(
                        message=f"Token request failed: {exc}", api_name=self.api_name
                    ) from exc
                self.logger.warning(
                    "Token fetch attempt %d failed, retrying: %s", attempt + 1, exc
                )

        try:
            token_response = TalentsoftTokenResponse(**cast(Dict[str, Any], payload))
        except ValidationError as exc:
            self.logger.error("Invalid token response format: %s", payload)
            raise ExternalApiError(
                message=f"Invalid token response: {exc}", api_name=self.api_name
            ) from exc

        self.cached_token = CachedToken(
            access_token=token_response.access_token,
            token_type=token_response.token_type,
            expires_at_epoch=time() + token_response.expires_in,
            refresh_token=token_response.refresh_token,
        )
        return self.cached_token.access_token

    async def get_access_token(self) -> str:
        async with self._token_lock:
            if self.cached_token and self.cached_token.is_valid():
                return self.cached_token.access_token
            return await self._fetch_new_token()

    def _build_auth_headers(self, token: str) -> Dict[str, str]:
        return {"Accept": "application/json", "Authorization": f"Bearer {token}"}

    async def _make_authenticated_request(
        self, url: str, params: Mapping[str, int | str]
    ) -> Any:
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

                if response.status_code == HTTPStatus.NOT_FOUND:
                    raise ExternalApiError(
                        message=f"Resource not found at {url}",
                        status_code=HTTPStatus.NOT_FOUND,
                        api_name=self.api_name,
                    )
                response.raise_for_status()
                return response

            except ExternalApiError:
                raise
            except Exception as exc:
                if attempt == self.max_retries:
                    self.logger.error(
                        "Failed to get response from %s: %s", self.api_name, url
                    )
                    raise ExternalApiError(
                        message=f"Request failed after retries: {exc}",
                        api_name=self.api_name,
                    ) from exc
                self.logger.warning(
                    "Request attempt %d failed, retrying: %s", attempt + 1, exc
                )

        raise ExternalApiError(  # pragma: no cover
            message="Unexpected end of retry loop", api_name=self.api_name
        )


class TalentsoftFrontClient(BaseTalentsoftClient, IOffersGateway):
    api_name = "Talentsoft Front API"

    def __init__(self, config: TalentsoftConfig, logger: logging.Logger, **kwargs):
        super().__init__(
            base_url=config.base_url,
            client_id=config.client_id,
            client_secret=config.client_secret,
            logger=logger,
            timeout=kwargs.get("timeout", 30),
            max_retries=kwargs.get("max_retries", 2),
        )

    async def get_all(
        self, count: int = 1000, start: int = 1
    ) -> Tuple[List[TalentsoftOffer], bool]:
        url = f"{self.base_url}{OFFERS_ENDPOINT}"
        params = {"count": count, "start": start}

        response = await self._make_authenticated_request(url, params)

        try:
            typed_response = TalentsoftOffersResponse.model_validate(response.json())
            offers = typed_response.data
            pagination = typed_response.pagination
        except ValidationError as e:
            raise ExternalApiError(
                f"Invalid response structure: {e}", api_name=self.api_name
            ) from e

        has_more = pagination.hasMore

        return offers, has_more

    async def get_detail(self, reference: str) -> RawOffer:
        if not reference:
            raise ExternalApiError(
                message="Reference is required", api_name=self.api_name
            )

        url = f"{self.base_url}{DETAIL_OFFER_ENDPOINT}"
        params = {"reference": reference}

        try:
            response = await self._make_authenticated_request(url, params)
        except ExternalApiError as e:
            if e.status_code == HTTPStatus.NOT_FOUND:
                raise ExternalApiError(
                    message=f"Offer not found for reference: {reference}",
                    api_name=self.api_name,
                ) from e
            raise

        try:
            talentsoft_offer = TalentsoftDetailOffer.model_validate(response.json())
        except ValidationError as e:
            raise ExternalApiError(
                f"Invalid response structure: {e}", api_name=self.api_name
            ) from e

        return RawOffer(reference=reference, data=talentsoft_offer.model_dump())
