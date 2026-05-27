import logging
from collections.abc import AsyncGenerator

import httpx
from fastapi import Depends

from api.config import Settings, get_settings
from application.use_cases.archive_offer import ArchiveOfferUseCase
from application.use_cases.load_offer_details import LoadOfferDetailsUseCase
from infrastructure.external_gateways.talentsoft_client import (
    TalentsoftConfig,
    TalentsoftFrontClient,
)

logger = logging.getLogger(__name__)


async def get_http_client() -> AsyncGenerator[httpx.AsyncClient, None]:
    async with httpx.AsyncClient() as client:
        yield client


def get_archive_offer_use_case(
    settings: Settings = Depends(get_settings),
    client: httpx.AsyncClient = Depends(get_http_client),
) -> ArchiveOfferUseCase | None:
    if not settings.web_base_url or not settings.web_api_key:
        return None
    return ArchiveOfferUseCase(
        client=client,
        web_base_url=settings.web_base_url,
        web_api_key=settings.web_api_key,
    )


async def get_load_offer_details_use_case(
    settings: Settings = Depends(get_settings),
) -> AsyncGenerator[LoadOfferDetailsUseCase | None, None]:
    if (
        not settings.talentsoft_front_client_id
        or not settings.talentsoft_front_client_secret
        or not settings.talentsoft_front_base_url
    ):
        yield None
    else:
        config = TalentsoftConfig(
            base_url=settings.talentsoft_front_base_url,
            client_id=settings.talentsoft_front_client_id,
            client_secret=settings.talentsoft_front_client_secret,
        )
        async with TalentsoftFrontClient(config=config, logger=logger) as client:
            yield LoadOfferDetailsUseCase(talentsoft_client=client)
