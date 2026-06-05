from domain.entities.offer import Offer
from domain.gateways.publish_offer_gateway import IPublishOfferGateway
from infrastructure.external_gateways.base_web_gateway import BaseWebGateway
from infrastructure.external_gateways.dtos.offer_upsert_payload import (
    OfferUpsertPayload,
)


class WebPublishOfferGateway(BaseWebGateway, IPublishOfferGateway):
    async def publish(self, offer: Offer) -> None:
        await self._post(
            "/offres/creer_modifier/",
            json={"offres": [self._serialize(offer)]},
        )

    def _serialize(self, offer: Offer) -> dict:
        return OfferUpsertPayload.from_offer(offer).model_dump(mode="json")
