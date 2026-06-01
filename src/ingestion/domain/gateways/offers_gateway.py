from typing import Protocol

from domain.raw_offer import RawOffer


class IOffersGateway(Protocol):
    async def get_detail(self, reference: str) -> RawOffer: ...
