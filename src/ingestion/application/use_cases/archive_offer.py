from datetime import datetime, timezone

from domain.gateways.archive_gateway import IArchiveGateway
from domain.repositories.raw_offer_repository import IRawOfferRepository


class ArchiveOfferUseCase:
    def __init__(
        self,
        archive_gateway: IArchiveGateway,
        raw_offer_repository: IRawOfferRepository,
    ) -> None:
        self._archive_gateway = archive_gateway
        self._raw_offer_repository = raw_offer_repository

    async def execute(self, reference: str, source_id: str) -> None:
        await self._archive_gateway.archive(reference=reference, source_id=source_id)
        await self._raw_offer_repository.mark_as_archived(
            reference=reference,
            source_id=source_id,
            archived_at=datetime.now(tz=timezone.utc),
        )
