import asyncio
import logging
from uuid import UUID

import httpx

from domain.value_objects.webhook_event import (
    OfferStatus,
    WebhookEvent,
    should_archive,
    should_save_raw_offer,
)
from infrastructure.celery_app import celery_app, get_container
from infrastructure.exceptions.exceptions import ExternalApiError

logger = logging.getLogger(__name__)

_MAX_RETRIES = 3
_SERVER_ERROR_STATUS = 500


def _is_transient(exc: Exception) -> bool:
    if isinstance(exc, httpx.TransportError):
        return True
    if isinstance(exc, ExternalApiError) and exc.status_code is not None:
        return exc.status_code >= _SERVER_ERROR_STATUS
    return False


@celery_app.task(bind=True, max_retries=_MAX_RETRIES)
def process_webhook(self, webhook_id: str) -> None:
    container = get_container()

    async def _run() -> None:
        webhook = await container.webhook_repository().get_by_id(UUID(webhook_id))

        event = WebhookEvent(
            event_type=webhook.event_type,
            reference=webhook.reference,
            status=OfferStatus(webhook.status_id) if webhook.status_id else None,
        )

        if should_archive(event):
            await container.archive_offer_use_case().execute(
                reference=webhook.reference, source_id=webhook.source_id
            )
            logger.info("Archived offer %s (webhook %s)", webhook.reference, webhook_id)

        elif should_save_raw_offer(event):
            sources_repository = container.sources_repository()
            source = sources_repository.get_by_source_id(webhook.source_id)
            if source is None:
                raise ValueError(
                    f"Source {webhook.source_id} not found, "
                    f"cannot process webhook {webhook_id}"
                )

            client = container.talentsoft_client_repository().get(
                source.client_id_front
            )
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
            await pipeline.execute(
                reference=webhook.reference, source_id=webhook.source_id
            )
            logger.info("Ingested offer %s (webhook %s)", webhook.reference, webhook_id)

        else:
            logger.info(
                "No action needed for webhook %s (event_type=%s)",
                webhook_id,
                webhook.event_type,
            )

    try:
        asyncio.run(_run())
    except Exception as exc:
        if _is_transient(exc):
            raise self.retry(exc=exc, countdown=2**self.request.retries) from exc
        raise
