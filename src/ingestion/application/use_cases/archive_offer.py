from domain.gateways.archive_gateway import IArchiveGateway


class ArchiveOfferUseCase:
    def __init__(self, archive_gateway: IArchiveGateway) -> None:
        self._archive_gateway = archive_gateway

    async def execute(self, reference: str, source_id: str) -> None:
        await self._archive_gateway.archive(reference=reference, source_id=source_id)
