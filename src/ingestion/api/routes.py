import logging

from fastapi import APIRouter, Depends, Request

from api.talentsoft import verify_talentsoft_signature

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
    return {"status": "ok"}
