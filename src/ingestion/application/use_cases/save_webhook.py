from typing import Any

from domain.entities.webhook import Webhook
from domain.repositories.webhook_repository import IWebhookRepository
from domain.value_objects.source import Source
from domain.value_objects.webhook_event import WebhookEvent
from domain.value_objects.webhook_type import WebhookType


class SaveWebhookUseCase:
    def __init__(self, repository: IWebhookRepository) -> None:
        self._repository = repository

    async def execute(
        self,
        event: WebhookEvent,
        source: Source,
        payload: dict[str, Any],
        webhook_type: WebhookType,
    ) -> None:
        webhook = Webhook(
            source_id=source.source_id,
            webhook_type=webhook_type,
            event_type=event.event_type,
            reference=event.reference,
            status_id=event.status,
            payload=payload,
        )
        await self._repository.insert(webhook)
