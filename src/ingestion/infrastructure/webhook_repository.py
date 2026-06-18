import asyncio
from uuid import UUID

from sqlalchemy import Engine
from sqlmodel import Session

from domain.entities.webhook import Webhook
from domain.repositories.webhook_repository import IWebhookRepository
from domain.value_objects.webhook_event import EventType, WebhookActionType
from infrastructure.models.webhook import WebhookModel
from infrastructure.value_objects.webhook_source import (
    SOURCE_TO_WEBHOOK_TYPE,
    WEBHOOK_TYPE_TO_SOURCE,
)


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
                action_type=webhook.action_type,
                payload=webhook.payload,
            )
            session.add(model)
            session.commit()

    async def get_by_id(self, webhook_id: UUID) -> Webhook:
        return await asyncio.to_thread(self._get_by_id_sync, webhook_id)

    def _get_by_id_sync(self, webhook_id: UUID) -> Webhook:
        with Session(self._engine) as session:
            model = session.get(WebhookModel, webhook_id)
            if model is None:
                raise ValueError(f"Webhook {webhook_id} not found in database")
            return Webhook(
                id=model.id,
                source_id=model.source_id,
                event_type=EventType(model.event_type),
                reference=model.reference,
                payload=model.payload,
                webhook_type=SOURCE_TO_WEBHOOK_TYPE[model.webhook_type],
                status_id=model.status_id,
                action_type=(
                    WebhookActionType(model.action_type) if model.action_type else None
                ),
            )
