import asyncio
import logging
import time
from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING, Any
from uuid import UUID

import httpx
import sentry_sdk

from domain.entities.webhook import Webhook
from infrastructure.celery_app import celery_app
from infrastructure.di.bootstrap import get_container
from infrastructure.exceptions.exceptions import (
    ExternalApiError,
    TalentsoftOfferNotFound,
)

if TYPE_CHECKING:
    from infrastructure.di.container import Container

logger = logging.getLogger(__name__)

_MAX_RETRIES = 3
_SERVER_ERROR_STATUS = 500
_TASK_TIMEOUT_SECONDS = 15

_Handler = Callable[["Container", Webhook], Awaitable[None]]


def _is_transient(exc: Exception) -> bool:
    if isinstance(exc, (httpx.TransportError, TimeoutError)):
        return True
    if isinstance(exc, httpx.HTTPStatusError):
        return exc.response.status_code >= _SERVER_ERROR_STATUS
    if isinstance(exc, ExternalApiError) and exc.status_code is not None:
        return exc.status_code >= _SERVER_ERROR_STATUS
    return False


async def _run_with_timeout(coro) -> None:
    async with asyncio.timeout(_TASK_TIMEOUT_SECONDS):
        await coro


def _retry_on_transient(task, exc: Exception) -> None:
    if _is_transient(exc):
        raise task.retry(exc=exc, countdown=2**task.request.retries) from exc
    raise exc


def _set_context(context: dict[str, Any], **values: Any) -> None:
    context.update(values)
    sentry_sdk.set_tags({k: v for k, v in values.items() if v is not None})


def _process(task, webhook_id: str, handler: _Handler) -> None:
    context: dict[str, Any] = {}
    _set_context(
        context,
        webhook_id=webhook_id,
        celery_task_id=task.request.id,
        retries=task.request.retries,
    )
    started_at = time.monotonic()
    container = get_container()

    async def _run() -> None:
        webhook = await container.webhook_repository().get_by_id(UUID(webhook_id))
        _set_context(
            context,
            reference=webhook.reference,
            source_id=webhook.source_id,
            action_type=webhook.action_type,
        )
        await handler(container, webhook)

    try:
        asyncio.run(_run_with_timeout(_run()))
    except Exception as exc:
        _retry_on_transient(task, exc)

    logger.info(
        "Webhook processed",
        extra={
            **context,
            "duration_ms": round((time.monotonic() - started_at) * 1000),
        },
    )


async def _archive_offer(container: "Container", webhook: Webhook) -> None:
    await container.archive_offer_usecase().execute(
        reference=webhook.reference, source_id=webhook.source_id
    )


async def _save_raw_offer(container: "Container", webhook: Webhook) -> None:
    source = container.sources_repository().get_by_source_id(UUID(webhook.source_id))
    if source is None:
        raise ValueError(
            f"Source {webhook.source_id} not found, cannot process webhook {webhook.id}"
        )

    client = container.talentsoft_client_repository().get(source.client_id_front)
    if client is None:
        raise ValueError(
            f"TalentSoft client not found for source {webhook.source_id}, "
            f"cannot process webhook {webhook.id}"
        )

    pipeline = container.ingest_offer_pipeline(
        save_raw_offer=container.save_raw_offer_usecase(offers_gateway=client),
    )
    await pipeline.execute(reference=webhook.reference, source_id=webhook.source_id)


@celery_app.task(bind=True, max_retries=_MAX_RETRIES)
def archive_offer_webhook(self, webhook_id: str) -> None:
    _process(self, webhook_id, _archive_offer)


@celery_app.task(bind=True, max_retries=_MAX_RETRIES, throws=(TalentsoftOfferNotFound,))
def save_raw_offer_webhook(self, webhook_id: str) -> None:
    _process(self, webhook_id, _save_raw_offer)
