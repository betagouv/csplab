import json
import logging
from typing import cast

import httpx
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import Response
from pydantic import ValidationError
from referentiel.entities.source import Source

from api.config import get_settings
from api.talentsoft import verify_talentsoft_signature
from application.tasks.process_webhook import (
    archive_offer_webhook,
    save_raw_offer_webhook,
)
from application.use_cases.save_webhook import SaveWebhookUseCase
from domain.repositories.sources_repository import ISourcesRepository
from domain.value_objects.webhook_event import WebhookActionType, WebhookEvent
from infrastructure.di.container import Container
from infrastructure.value_objects import webhook_source
from presentation.dtos.talentsoft_webhook import TalentsoftWebhookPayload

logger = logging.getLogger(__name__)

public_router = APIRouter()

_OK = {"status": "ok"}


@public_router.get("/health")
def health():
    return {"status": "healthy"}


@public_router.api_route(
    "/flower/{path:path}",
    methods=["GET", "POST", "DELETE", "PUT", "PATCH", "HEAD", "OPTIONS"],
)
async def flower_proxy(path: str, request: Request):
    flower_port = get_settings().flower_port
    if not flower_port:
        raise HTTPException(status_code=503, detail="Flower is not configured")
    url = f"http://localhost:{flower_port}/flower/{path}"
    if request.url.query:
        url = f"{url}?{request.url.query}"
    async with httpx.AsyncClient() as client:
        proxied = await client.request(
            method=request.method,
            url=url,
            headers={k: v for k, v in request.headers.items() if k.lower() != "host"},
            content=await request.body(),
        )
    return Response(
        content=proxied.content,
        status_code=proxied.status_code,
        headers=dict(proxied.headers),
    )


@public_router.post(
    "/webhooks/talentsoft", dependencies=[Depends(verify_talentsoft_signature)]
)
@inject
async def talentsoft_webhook(
    request: Request,
    client_id: str = Query(...),
    repository: ISourcesRepository = Depends(Provide[Container.sources_repository]),
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
        webhook = await save_webhook_use_case.execute(
            event=event,
            source=source,
            payload=json.loads(body),
            webhook_type=webhook_source.SOURCE_TO_WEBHOOK_TYPE["talentsoft"],
        )
    except Exception:
        logger.exception("Failed to store webhook for reference %s", event.reference)
        return _OK

    if webhook.action_type is None:
        logger.info(
            "Unhandled event type %s for reference %s and status %s",
            event.event_type,
            event.reference,
            event.status,
            extra={"client_id": client_id},
        )
        return _OK

    if webhook.action_type == WebhookActionType.ARCHIVE:
        archive_offer_webhook.delay(str(webhook.id))
    elif webhook.action_type == WebhookActionType.SAVE_RAW_OFFER:
        save_raw_offer_webhook.delay(str(webhook.id))

    logger.info(
        "Enqueued processing for event %s reference %s",
        event.event_type,
        event.reference,
        extra={"client_id": client_id, "webhook_id": str(webhook.id)},
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
