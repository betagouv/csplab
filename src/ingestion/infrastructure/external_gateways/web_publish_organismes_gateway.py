import logging

from referentiel.entities.organisme import Organisme

from domain.gateways.publish_organismes_gateway import IPublishOrganismesGateway
from infrastructure.exceptions.exceptions import ExternalApiError
from infrastructure.external_gateways.base_web_gateway import BaseWebGateway
from infrastructure.external_gateways.dtos.organisme_upsert_payload import (
    OrganismeUpsertPayload,
)

logger = logging.getLogger(__name__)


class WebPublishOrganismesGateway(BaseWebGateway, IPublishOrganismesGateway):
    async def publish(self, organismes: list[Organisme]) -> None:
        response = await self._post(
            "/organismes/creer_modifier",
            json={"organismes": [self._serialize(o) for o in organismes]},
        )
        errors = response.json().get("errors") if response.content else None
        if errors:
            logger.error(
                "WebPublishOrganismesGateway: publish failed for %d organismes: %s",
                len(organismes),
                errors,
            )
            raise ExternalApiError(
                "Failed to publish organismes",
                api_name="web",
                details={"errors": errors},
            )

    def _serialize(self, organisme: Organisme) -> dict:
        return OrganismeUpsertPayload.from_organisme(organisme).model_dump(mode="json")
