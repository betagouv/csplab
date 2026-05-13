from collections.abc import AsyncGenerator

import httpx
from fastapi import Depends, HTTPException

from api.config import Settings, get_settings
from application.use_cases.archive_offer import ArchiveOfferUseCase


async def get_http_client() -> AsyncGenerator[httpx.AsyncClient, None]:
    async with httpx.AsyncClient() as client:
        yield client


def get_archive_offer_use_case(
    settings: Settings = Depends(get_settings),
    client: httpx.AsyncClient = Depends(get_http_client),
) -> ArchiveOfferUseCase:
    if not settings.web_base_url or not settings.web_api_key:
        raise HTTPException(status_code=500, detail="Web service not configured")
    return ArchiveOfferUseCase(
        client=client,
        web_base_url=settings.web_base_url,
        web_api_key=settings.web_api_key,
    )
