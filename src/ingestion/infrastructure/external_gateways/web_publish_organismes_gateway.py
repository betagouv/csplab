import logging
from collections.abc import Mapping
from uuid import UUID

from referentiel.entities.organisme import Organisme

from domain.gateways.publish_organismes_gateway import IPublishOrganismesGateway
from infrastructure.external_gateways.base_web_gateway import BaseWebGateway
from infrastructure.external_gateways.dtos.organisme_upsert_payload import (
    OrganismeUpsertPayload,
)

logger = logging.getLogger(__name__)


class WebPublishOrganismesGateway(BaseWebGateway, IPublishOrganismesGateway):
    async def publish(
        self, organismes: list[Organisme], external_ids: Mapping[UUID, str | None]
    ) -> None:
        response = await self._post(
            "/organismes/creer_modifier",
            json={"organismes": [self._serialize(o, external_ids) for o in organismes]},
        )
        errors = response.json().get("errors") if response.content else None
        if errors:
            logger.error(
                "WebPublishOrganismesGateway: publish failed for %d organismes: %s",
                len(errors),
                errors,
            )

    def _serialize(
        self, organisme: Organisme, external_ids: Mapping[UUID, str | None]
    ) -> dict:
        parent_external_id = (
            external_ids.get(organisme.parent_id) if organisme.parent_id else None
        )
        return OrganismeUpsertPayload.from_organisme(
            organisme, parent_external_id
        ).model_dump(mode="json")
