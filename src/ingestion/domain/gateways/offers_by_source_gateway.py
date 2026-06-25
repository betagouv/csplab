from typing import Protocol
from uuid import UUID


class IOffersBySourceGateway(Protocol):
    async def fetch_references(self, source_id: UUID) -> list[str]: ...
