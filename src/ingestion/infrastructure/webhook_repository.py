import asyncio

from sqlalchemy import Engine
from sqlmodel import Session

from domain.entities.webhook import Webhook
from domain.repositories.webhook_repository import IWebhookRepository
from infrastructure.models.webhook import WebhookModel
from infrastructure.value_objects.webhook_source import WEBHOOK_TYPE_TO_SOURCE


class WebhookRepository(IWebhookRepository):
    def __init__(self, engine: Engine) -> None:
        self._engine = engine

    async def insert(self, webhook: Webhook) -> None:
        await asyncio.to_thread(self._insert_sync, webhook)

    def _insert_sync(self, webhook: Webhook) -> None:
        with Session(self._engine) as session:
            model = WebhookModel(
                id=webhook.id,
                source_id=webhook.source_id,
                webhook_type=WEBHOOK_TYPE_TO_SOURCE[webhook.webhook_type],
                event_type=webhook.event_type,
                reference=webhook.reference,
                status_id=webhook.status_id,
                payload=webhook.payload,
            )
            session.add(model)
            session.commit()
