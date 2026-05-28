from typing import Protocol

from infrastructure.models.raw_offer import RawOffer


class IRawOfferRepository(Protocol):
    async def upsert(self, offer: RawOffer) -> None: ...
