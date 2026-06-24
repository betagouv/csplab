import asyncio
import logging
from uuid import UUID

import httpx

from infrastructure.celery_app import celery_app, get_container
from infrastructure.exceptions.exceptions import ExternalApiError

logger = logging.getLogger(__name__)

_MAX_RETRIES = 3
_SERVER_ERROR_STATUS = 500
_TASK_TIMEOUT_SECONDS = 15


def _is_transient(exc: Exception) -> bool:
    if isinstance(exc, httpx.TransportError):
        return True
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


@celery_app.task(bind=True, max_retries=_MAX_RETRIES)
def archive_offer_webhook(self, webhook_id: str) -> None:
    container = get_container()

    async def _run() -> None:
        webhook = await container.webhook_repository().get_by_id(UUID(webhook_id))
        await container.archive_offer_use_case().execute(
            reference=webhook.reference, source_id=webhook.source_id
        )
        logger.info("Archived offer %s (webhook %s)", webhook.reference, webhook_id)

    try:
        asyncio.run(_run_with_timeout(_run()))
    except Exception as exc:
        _retry_on_transient(self, exc)


@celery_app.task(bind=True, max_retries=_MAX_RETRIES)
def save_raw_offer_webhook(self, webhook_id: str) -> None:
    container = get_container()

    async def _run() -> None:
        webhook = await container.webhook_repository().get_by_id(UUID(webhook_id))

        sources_repository = container.sources_repository()
        source = sources_repository.get_by_source_id(UUID(webhook.source_id))
        if source is None:
            raise ValueError(
                f"Source {webhook.source_id} not found, "
                f"cannot process webhook {webhook_id}"
            )

        client = container.talentsoft_client_repository().get(source.client_id_front)
        if client is None:
            raise ValueError(
                f"TalentSoft client not found for source {webhook.source_id}, "
                f"cannot process webhook {webhook_id}"
            )

        pipeline = container.ingest_offer_pipeline(
            save_raw_offer=container.save_raw_offer_use_case(
                offers_gateway=client,
            ),
        )
        await pipeline.execute(reference=webhook.reference, source_id=webhook.source_id)
        logger.info("Ingested offer %s (webhook %s)", webhook.reference, webhook_id)

    try:
        asyncio.run(_run_with_timeout(_run()))
    except Exception as exc:
        _retry_on_transient(self, exc)
