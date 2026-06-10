import json
import logging
from typing import cast

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from pydantic import ValidationError

from api.talentsoft import verify_talentsoft_signature
from application.pipelines.ingest_offer_pipeline import IngestOfferPipeline
from application.use_cases.archive_offer import ArchiveOfferUseCase
from application.use_cases.save_webhook import SaveWebhookUseCase
from domain.repositories.sources_repository import ISourcesRepository
from domain.value_objects.source import Source
from domain.value_objects.webhook_event import (
    WebhookEvent,
    should_archive,
    should_save_raw_offer,
)
from domain.value_objects.webhook_type import WebhookType
from infrastructure.di.container import (
    Container,
    get_ingest_offer_pipeline,
)
from presentation.dtos.talentsoft_webhook import TalentsoftWebhookPayload

logger = logging.getLogger(__name__)

public_router = APIRouter()

_OK = {"status": "ok"}


@public_router.get("/health")
def health():
    return {"status": "healthy"}


@public_router.post(
    "/webhooks/talentsoft", dependencies=[Depends(verify_talentsoft_signature)]
)
@inject
async def talentsoft_webhook(
    request: Request,
    client_id: str = Query(...),
    use_case: ArchiveOfferUseCase | None = Depends(
        Provide[Container.archive_offer_use_case]
    ),
    repository: ISourcesRepository = Depends(Provide[Container.sources_repository]),
    ingest_offer_pipeline: IngestOfferPipeline | None = Depends(
        get_ingest_offer_pipeline
    ),
    save_webhook_use_case: SaveWebhookUseCase = Depends(
        Provide[Container.save_webhook_use_case]
    ),
):
    body = await request.body()
    logger.debug(
        "Received TalentSoft webhook body",
        extra={"body": body.decode(), "client_id": client_id},
    )
    if not body:
        return _OK

    event = _parse_payload(body, client_id)
    if event is None:
        return _OK

    # verify_talentsoft_signature already rejected unknown client_ids
    source = cast(Source, repository.get_by_client_id_back(client_id))

    try:
        await save_webhook_use_case.execute(
            event=event,
            source=source,
            payload=json.loads(body),
            webhook_type=WebhookType.TALENTSOFT,
        )
    except Exception:
        logger.exception("Failed to store webhook for reference %s", event.reference)

    if should_archive(event):
        if use_case is None:
            raise HTTPException(status_code=500, detail="Web service not configured")
        return await _handle_archive(event, client_id, source.source_id, use_case)

    if should_save_raw_offer(event):
        if ingest_offer_pipeline is None:
            raise HTTPException(
                status_code=500, detail="Talentsoft client or database not configured"
            )
        return await _handle_ingest_offer(
            event, client_id, source.source_id, ingest_offer_pipeline
        )

    logger.info(
        "Unhandled event type %s for reference %s and status %s",
        event.event_type,
        event.reference,
        event.status,
        extra={"client_id": client_id},
    )
    return _OK


def _parse_payload(body: bytes, client_id: str) -> WebhookEvent | None:
    try:
        return TalentsoftWebhookPayload.model_validate_json(body).to_domain()
    except ValidationError:
        logger.warning(
            "Unrecognised TalentSoft webhook payload, ignoring",
            extra={"body": body.decode(), "client_id": client_id},
        )
        return None


async def _handle_archive(
    event: WebhookEvent,
    client_id: str,
    source_id: str,
    use_case: ArchiveOfferUseCase,
) -> dict:
    await use_case.execute(reference=event.reference, source_id=source_id)
    logger.info(
        "Handled event type %s for reference %s",
        event.event_type,
        event.reference,
        extra={"client_id": client_id, "source_id": source_id},
    )
    return _OK


async def _handle_ingest_offer(
    event: WebhookEvent,
    client_id: str,
    source_id: str,
    pipeline: IngestOfferPipeline,
) -> dict:
    await pipeline.execute(reference=event.reference, source_id=source_id)
    logger.info(
        "Handled event type %s for reference %s",
        event.event_type,
        event.reference,
        extra={"client_id": client_id, "source_id": source_id},
    )
    return _OK
