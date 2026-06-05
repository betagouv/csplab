from domain.entities.offer import Offer
from domain.gateways.publish_offer_gateway import IPublishOfferGateway


class PostCleanedOfferUseCase:
    def __init__(self, publish_offer_gateway: IPublishOfferGateway) -> None:
        self._gateway = publish_offer_gateway

    async def execute(self, offer: Offer) -> None:
        await self._gateway.publish(offer)
