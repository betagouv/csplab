from typing import Protocol
from uuid import UUID

from domain.entities.webhook import Webhook


class IWebhookRepository(Protocol):
    async def insert(self, webhook: Webhook) -> None: ...
    async def get_by_id(self, webhook_id: UUID) -> Webhook: ...
