import logging

from domain.gateways.publish_talentsoft_organismes_gateway import (
    IPublishTalentsoftOrganismesGateway,
)
from infrastructure.external_gateways.base_web_gateway import BaseWebGateway
from infrastructure.external_gateways.dtos.talentsoft_dtos import (
    TalentsoftOrganisationPayload,
)
from infrastructure.external_gateways.dtos.talentsoft_organisme_upsert_payload import (
    TalentsoftOrganismeUpsertPayload,
)

logger = logging.getLogger(__name__)


class WebPublishTalentsoftOrganismesGateway(
    BaseWebGateway, IPublishTalentsoftOrganismesGateway
):
    async def publish(self, organisations: list[TalentsoftOrganisationPayload]) -> None:
        response = await self._post(
            "/talentsoft_organisme/creer_modifier",
            json={"talentsoft_organismes": [self._serialize(o) for o in organisations]},
        )
        errors = response.json().get("errors") if response.content else None
        if errors:
            logger.error(
                "WebPublishTalentsoftOrganismesGateway: publish failed for "
                "%d organismes: %s",
                len(errors),
                errors,
            )

    def _serialize(self, organisation: TalentsoftOrganisationPayload) -> dict:
        return TalentsoftOrganismeUpsertPayload.from_organisation_payload(
            organisation
        ).model_dump(mode="json", exclude_none=True)
