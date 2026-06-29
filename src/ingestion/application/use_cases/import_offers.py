import logging
from typing import Callable
from uuid import UUID

from application.use_cases._talentsoft_source import resolve_source_and_client
from domain.entities.webhook import Webhook
from domain.repositories.sources_repository import ISourcesRepository
from domain.repositories.webhook_repository import IWebhookRepository
from domain.value_objects.webhook_event import EventType, WebhookEvent
from domain.value_objects.webhook_type import WebhookType
from infrastructure.talentsoft_client_repository import TalentsoftClientRepository

logger = logging.getLogger(__name__)

_BATCH_SIZE = 1_000


class ImportOffersUseCase:
    def __init__(
        self,
        sources_repository: ISourcesRepository,
        talentsoft_client_repository: TalentsoftClientRepository,
        webhook_repository: IWebhookRepository,
        dispatch_process_webhook: Callable[[str], None],
    ) -> None:
        self._sources_repository = sources_repository
        self._talentsoft_client_repository = talentsoft_client_repository
        self._webhook_repository = webhook_repository
        self._dispatch_process_webhook = dispatch_process_webhook

    async def execute(self, source_id: UUID) -> None:
        _, client = resolve_source_and_client(
            source_id, self._sources_repository, self._talentsoft_client_repository
        )

        start = 1
        has_more = True
        total = 0

        while has_more:
            offers, has_more = await client.get_all(count=_BATCH_SIZE, start=start)
            for offer in offers:
                event = WebhookEvent(
                    event_type=EventType.CREE, reference=offer.reference
                )
                webhook = Webhook(
                    source_id=str(source_id),
                    webhook_type=WebhookType.OFFER,
                    event_type=event.event_type,
                    reference=event.reference,
                    status_id=None,
                    action_type=event.get_action_type(),
                    payload={},
                )
                await self._webhook_repository.insert(webhook)
                self._dispatch_process_webhook(str(webhook.id))
                total += 1
            start += 1

        logger.info("Imported %d offers for source %s", total, source_id)
