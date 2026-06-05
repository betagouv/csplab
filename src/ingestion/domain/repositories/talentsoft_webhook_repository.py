from typing import Protocol

from domain.entities.talentsoft_webhook import TalentsoftWebhook


class ITalentsoftWebhookRepository(Protocol):
    async def insert(self, webhook: TalentsoftWebhook) -> None: ...
