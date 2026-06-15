from typing import Protocol

from domain.gateways.publish_offer_input import PublishOfferInput


class IPublishOfferGateway(Protocol):
    async def publish(self, input: PublishOfferInput) -> None: ...
