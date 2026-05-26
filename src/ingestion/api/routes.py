import logging

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from pydantic import ValidationError

from api.dependencies import get_archive_offer_use_case, get_load_offer_details_use_case
from api.talentsoft import verify_talentsoft_signature
from application.use_cases.archive_offer import ArchiveOfferUseCase
from application.use_cases.load_offer_details import LoadOfferDetailsUseCase
from presentation.dtos.talentsoft_webhook import (
    TalentsoftWebhookPayload,
    should_archive,
    should_load_offer_details,
)

logger = logging.getLogger(__name__)

public_router = APIRouter()

_OK = {"status": "ok"}


@public_router.get("/health")
def health():
    return {"status": "healthy"}


@public_router.post(
    "/webhooks/talentsoft", dependencies=[Depends(verify_talentsoft_signature)]
)
async def talentsoft_webhook(
    request: Request,
    client_id: str = Query(...),
    archive_use_case: ArchiveOfferUseCase | None = Depends(get_archive_offer_use_case),
    load_offer_use_case: LoadOfferDetailsUseCase | None = Depends(
        get_load_offer_details_use_case
    ),
):
    body = await request.body()
    logger.debug(
        "Received TalentSoft webhook body",
        extra={"body": body.decode(), "client_id": client_id},
    )
    if not body:
        return _OK

    payload = _parse_payload(body, client_id)
    if payload is None:
        return _OK

    if should_archive(payload):
        if archive_use_case is None:
            raise HTTPException(status_code=500, detail="Web service not configured")
        return await _handle_archive(payload, client_id, archive_use_case)

    if should_load_offer_details(payload):
        if load_offer_use_case is None:
            raise HTTPException(
                status_code=500, detail="Talentsoft client not configured"
            )
        return await _handle_load_offer_details(payload, client_id, load_offer_use_case)

    logger.info(
        "Unhandled event type %s for reference %s and status_id %s",
        payload.event_type,
        payload.reference,
        payload.status_id,
        extra={"client_id": client_id},
    )
    return _OK


def _parse_payload(body: bytes, client_id: str) -> TalentsoftWebhookPayload | None:
    try:
        return TalentsoftWebhookPayload.model_validate_json(body)
    except ValidationError:
        logger.warning(
            "Unrecognised TalentSoft webhook payload, ignoring",
            extra={"body": body.decode(), "client_id": client_id},
        )
        return None


async def _handle_archive(
    payload: TalentsoftWebhookPayload,
    client_id: str,
    use_case: ArchiveOfferUseCase,
) -> dict:
    # `source_id` will not be `client_id` soon
    # https://github.com/betagouv/csplab/issues/573 is required
    await use_case.execute(reference=payload.reference, source_id=client_id)
    logger.info(
        "Handled event type %s for reference %s",
        payload.event_type,
        payload.reference,
        extra={"client_id": client_id},
    )
    return _OK


async def _handle_load_offer_details(
    payload: TalentsoftWebhookPayload,
    client_id: str,
    use_case: LoadOfferDetailsUseCase,
) -> dict:
    await use_case.execute(reference=payload.reference)
    logger.info(
        "Handled event type %s for reference %s",
        payload.event_type,
        payload.reference,
        extra={"client_id": client_id},
    )
    return _OK
