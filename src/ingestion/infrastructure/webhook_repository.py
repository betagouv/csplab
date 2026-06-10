import asyncio
from datetime import datetime, timezone

from sqlalchemy import Engine
from sqlmodel import Session

from domain.entities.webhook import Webhook
from domain.repositories.webhook_repository import IWebhookRepository
from infrastructure.models.webhook import WebhookModel


class WebhookRepository(IWebhookRepository):
    def __init__(self, engine: Engine) -> None:
        self._engine = engine

    async def insert(self, webhook: Webhook) -> None:
        await asyncio.to_thread(self._insert_sync, webhook)

    def _insert_sync(self, webhook: Webhook) -> None:
        now = datetime.now(tz=timezone.utc)
        with Session(self._engine) as session:
            model = WebhookModel(
                id=webhook.id,
                created_at=now,
                updated_at=now,
                source_id=webhook.source_id,
                webhook_type=webhook.webhook_type,
                event_type=webhook.event_type,
                reference=webhook.reference,
                status_id=webhook.status_id,
                payload=webhook.payload,
            )
            session.add(model)
            session.commit()
