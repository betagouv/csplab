from domain.entities.offer import Offer
from domain.gateways.publish_offer_gateway import IPublishOfferGateway
from domain.gateways.publish_offer_input import PublishOfferInput


class PublishOfferUseCase:
    def __init__(self, publish_offer_gateway: IPublishOfferGateway) -> None:
        self._gateway = publish_offer_gateway

    async def execute(self, offer: Offer) -> None:
        await self._gateway.publish(
            PublishOfferInput(source_id=offer.source_id, offer=offer)
        )
