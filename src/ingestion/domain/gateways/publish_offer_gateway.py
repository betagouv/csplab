from typing import Protocol

from domain.entities.offer import Offer


class IPublishOfferGateway(Protocol):
    async def publish(self, offer: Offer) -> None: ...
