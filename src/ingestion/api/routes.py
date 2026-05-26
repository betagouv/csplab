import logging

from fastapi import APIRouter, Depends, Query, Request
from pydantic import ValidationError

from api.dependencies import get_archive_offer_use_case
from api.talentsoft import verify_talentsoft_signature
from application.use_cases.archive_offer import ArchiveOfferUseCase
from presentation.dtos.talentsoft_webhook import (
    TalentsoftWebhookPayload,
    should_archive,
)

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
    client_id: str = Query(...),
    use_case: ArchiveOfferUseCase = Depends(get_archive_offer_use_case),
):
    body = await request.body()
    logger.debug(
        "Received TalentSoft webhook body",
        extra={"body": body.decode(), "client_id": client_id},
    )
    if not body:
        return {"status": "ok"}

    try:
        payload = TalentsoftWebhookPayload.model_validate_json(body)
    except ValidationError:
        logger.warning(
            "Unrecognised TalentSoft webhook payload, ignoring",
            extra={"body": body.decode(), "client_id": client_id},
        )
        return {"status": "ok"}

    if not should_archive(payload):
        logger.info(
            "Unhandled event type %s for reference %s and status_id %s",
            payload.event_type,
            payload.reference,
            payload.status_id,
            extra={"client_id": client_id},
        )
        return {"status": "ok"}

    # `source_id` will not be `client_id` soon
    # https://github.com/betagouv/csplab/issues/573 is required
    await use_case.execute(reference=payload.reference, source_id=client_id)
    logger.info(
        "Handled event type %s for reference %s",
        payload.event_type,
        payload.reference,
        extra={"client_id": client_id},
    )
    return {"status": "ok"}
