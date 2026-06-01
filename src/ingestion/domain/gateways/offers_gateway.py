from typing import Protocol

from domain.entities.raw_offer import RawOffer


class IOffersGateway(Protocol):
    async def get_detail(self, reference: str) -> RawOffer: ...
