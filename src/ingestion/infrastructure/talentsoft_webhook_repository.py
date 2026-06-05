import asyncio
from datetime import datetime, timezone

from sqlalchemy import Engine
from sqlmodel import Session

from domain.entities.talentsoft_webhook import TalentsoftWebhook
from domain.repositories.talentsoft_webhook_repository import (
    ITalentsoftWebhookRepository,
)
from infrastructure.models.talentsoft_webhook import TalentsoftWebhookModel


class TalentsoftWebhookRepository(ITalentsoftWebhookRepository):
    def __init__(self, engine: Engine) -> None:
        self._engine = engine

    async def insert(self, webhook: TalentsoftWebhook) -> None:
        await asyncio.to_thread(self._insert_sync, webhook)

    def _insert_sync(self, webhook: TalentsoftWebhook) -> None:
        now = datetime.now(tz=timezone.utc)
        with Session(self._engine) as session:
            model = TalentsoftWebhookModel(
                id=webhook.id,
                created_at=now,
                updated_at=now,
                source_id=webhook.source_id,
                event_type=webhook.event_type,
                reference=webhook.reference,
                status_id=webhook.status_id,
                payload=webhook.payload,
            )
            session.add(model)
            session.commit()
