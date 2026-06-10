from typing import Protocol

from domain.entities.webhook import Webhook


class IWebhookRepository(Protocol):
    async def insert(self, webhook: Webhook) -> None: ...
