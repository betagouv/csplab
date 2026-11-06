from typing import Protocol
from uuid import UUID

from domain.entities.webhook import Webhook
from domain.value_objects.webhook_event import WebhookProcessingStatus


class IWebhookRepository(Protocol):
    async def insert(self, webhook: Webhook) -> None: ...
    async def get_by_id(self, webhook_id: UUID) -> Webhook: ...
    async def mark_processing(self, webhook_id: UUID) -> None: ...
    async def mark_processed(
        self,
        webhook_id: UUID,
        status: WebhookProcessingStatus,
        error: str | None = None,
    ) -> None: ...
