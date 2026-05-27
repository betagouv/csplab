import logging
from typing import Callable, TypeVar

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from pydantic import ValidationError
from starlette.datastructures import State

from api.config import Settings, get_settings
from api.talentsoft import verify_talentsoft_signature
from application.interfaces.sources_repository import ISourcesRepository
from application.use_cases.archive_offer import ArchiveOfferUseCase
from application.use_cases.load_offer_details import LoadOfferDetailsUseCase
from infrastructure.di.container import Container
from infrastructure.external_gateways.talentsoft_client import (
    TalentsoftConfig,
    TalentsoftFrontClient,
)
from presentation.dtos.talentsoft_webhook import (
    TalentsoftWebhookPayload,
    should_archive,
    should_load_offer_details,
)

logger = logging.getLogger(__name__)

public_router = APIRouter()

_OK = {"status": "ok"}

_T = TypeVar("_T")


def _state_setdefault(state: State, key: str, factory: Callable[[], _T]) -> _T:
    if not hasattr(state, key):
        setattr(state, key, factory())
    return getattr(state, key)


def get_load_offer_details_use_case(
    request: Request,
    settings: Settings = Depends(get_settings),
) -> LoadOfferDetailsUseCase | None:
    if (
        not settings.talentsoft_front_client_id
        or not settings.talentsoft_front_client_secret
        or not settings.talentsoft_front_base_url
    ):
        return None

    base_url = settings.talentsoft_front_base_url
    client_id = settings.talentsoft_front_client_id
    client_secret = settings.talentsoft_front_client_secret

    def _make_client() -> TalentsoftFrontClient:
        config = TalentsoftConfig(
            base_url=base_url,
            client_id=client_id,
            client_secret=client_secret,
        )
        return TalentsoftFrontClient(config=config, logger=logger)

    client = _state_setdefault(
        request.app.state,
        "talentsoft_front_client",
        _make_client,
    )
    return LoadOfferDetailsUseCase(talentsoft_client=client)


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
    web_base_url: str | None = Depends(Provide[Container.config.web_base_url]),
    web_api_key: str | None = Depends(Provide[Container.config.web_api_key]),
    use_case: ArchiveOfferUseCase = Depends(Provide[Container.archive_offer_use_case]),
    registry: ISourcesRepository = Depends(Provide[Container.sources_repository]),
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
        if not web_base_url or not web_api_key:
            raise HTTPException(status_code=500, detail="Web service not configured")
        return await _handle_archive(payload, client_id, use_case, registry)

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
    registry: ISourcesRepository,
) -> dict:
    source = registry.get_by_client_id_back(client_id)
    if source is None:
        logger.error(
            "No source found for client_id %s, cannot archive offer %s",
            client_id,
            payload.reference,
        )
        raise HTTPException(
            status_code=422,
            detail=f"Unknown client_id: {client_id}",
        )

    await use_case.execute(reference=payload.reference, source_id=source.source_id)
    logger.info(
        "Handled event type %s for reference %s",
        payload.event_type,
        payload.reference,
        extra={"client_id": client_id, "source_id": source.source_id},
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
