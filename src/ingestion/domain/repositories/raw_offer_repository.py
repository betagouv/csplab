from typing import Protocol

from domain.raw_offer import RawOffer


class IRawOfferRepository(Protocol):
    async def upsert(self, offer: RawOffer) -> None: ...
