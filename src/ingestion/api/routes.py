import logging

import httpx
from fastapi import APIRouter, Depends, HTTPException, Request

from api.config import get_settings
from api.talentsoft import verify_talentsoft_signature
from api.webhook import TalentsoftWebhookPayload, should_archive

logger = logging.getLogger(__name__)

public_router = APIRouter()


@public_router.get("/health")
def health():
    return {"status": "healthy"}


@public_router.post(
    "/webhooks/talentsoft", dependencies=[Depends(verify_talentsoft_signature)]
)
async def talentsoft_webhook(request: Request):
    body = await request.body()
    logger.info("TalentSoft webhook received", extra={"body": body.decode()})

    if not body:
        return {"status": "ok"}

    payload = TalentsoftWebhookPayload.model_validate_json(body)

    if not should_archive(payload):
        return {"status": "ok"}

    if not payload.reference:
        logger.warning("Archive event received without reference, skipping")
        return {"status": "ok"}

    settings = get_settings()
    if not settings.web_base_url or not settings.web_api_key:
        raise HTTPException(status_code=500, detail="Web service not configured")

    url = f"{settings.web_base_url}/api/offers/{payload.reference}/archive"
    async with httpx.AsyncClient() as client:
        response = await client.post(
            url, headers={"Authorization": f"Api-Key {settings.web_api_key}"}
        )
        response.raise_for_status()

    return {"status": "ok"}
