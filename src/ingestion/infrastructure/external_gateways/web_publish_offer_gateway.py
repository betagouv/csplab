import logging

import httpx

from domain.entities.offer import Offer
from domain.gateways.publish_offer_gateway import IPublishOfferGateway
from domain.gateways.publish_offer_input import PublishOfferInput
from domain.repositories.metiers_multi_domaines_repository import (
    IMetiersMultiDomainesRepository,
)
from infrastructure.exceptions.exceptions import ExternalApiError
from infrastructure.external_gateways.base_web_gateway import (
    BaseWebGateway,
    WebGatewayCredentials,
)
from infrastructure.external_gateways.dtos.offer_upsert_payload import (
    OfferUpsertPayload,
)

logger = logging.getLogger(__name__)


class WebPublishOfferGateway(BaseWebGateway, IPublishOfferGateway):
    def __init__(
        self,
        client: httpx.AsyncClient,
        credentials: WebGatewayCredentials,
        metiers_multi_domaines_repository: IMetiersMultiDomainesRepository,
    ) -> None:
        super().__init__(client, credentials)
        self._metiers_multi_domaines = metiers_multi_domaines_repository

    async def publish(self, input: PublishOfferInput) -> None:
        response = await self._post(
            "/offres/creer_modifier",
            json={
                "source_id": str(input.source_id),
                "offres": [self._serialize(input.offer)],
            },
        )
        errors = response.json().get("errors") if response.content else None
        if errors:
            logger.error(
                "WebPublishOfferGateway: publish failed for offer %s: %s",
                input.offer.reference,
                errors,
            )
            raise ExternalApiError(
                f"Failed to publish offer {input.offer.reference}: {errors}",
                api_name="web",
                details={"errors": errors},
            )

    def _serialize(self, offer: Offer) -> dict:
        return OfferUpsertPayload.from_offer(
            offer, self._metiers_multi_domaines
        ).model_dump(mode="json")
