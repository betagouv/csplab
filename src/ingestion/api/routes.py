import logging

from fastapi import APIRouter, Depends, Request
from pydantic import ValidationError

from api.dependencies import get_archive_offer_use_case
from api.talentsoft import verify_talentsoft_signature
from application.use_cases.archive_offer import ArchiveOfferUseCase
from presentation.dtos.talentsoft_webhook import TalentsoftWebhookPayload, should_archive

logger = logging.getLogger(__name__)

public_router = APIRouter()


@public_router.get("/health")
def health():
    return {"status": "healthy"}


@public_router.post(
    "/webhooks/talentsoft", dependencies=[Depends(verify_talentsoft_signature)]
)
async def talentsoft_webhook(
    request: Request,
    use_case: ArchiveOfferUseCase = Depends(get_archive_offer_use_case),
):
    body = await request.body()
    logger.info("TalentSoft webhook received", extra={"body": body.decode()})

    if not body:
        return {"status": "ok"}

    try:
        payload = TalentsoftWebhookPayload.model_validate_json(body)
    except ValidationError:
        logger.warning("Unrecognised TalentSoft webhook payload, ignoring")
        return {"status": "ok"}

    if not should_archive(payload):
        return {"status": "ok"}

    if not payload.reference:
        logger.warning("Archive event received without reference, skipping")
        return {"status": "ok"}

    await use_case.execute(payload.reference)
    return {"status": "ok"}
