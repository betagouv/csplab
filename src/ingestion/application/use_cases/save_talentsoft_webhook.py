from typing import Any

from domain.entities.talentsoft_webhook import TalentsoftWebhook
from domain.repositories.talentsoft_webhook_repository import (
    ITalentsoftWebhookRepository,
)
from domain.value_objects.source import Source
from domain.value_objects.webhook_event import WebhookEvent


class SaveTalentsoftWebhookUseCase:
    def __init__(self, repository: ITalentsoftWebhookRepository) -> None:
        self._repository = repository

    async def execute(
        self, event: WebhookEvent, source: Source, payload: dict[str, Any]
    ) -> None:
        webhook = TalentsoftWebhook(
            source_id=source.source_id,
            event_type=event.event_type,
            reference=event.reference,
            status_id=event.status,
            payload=payload,
        )
        await self._repository.insert(webhook)
