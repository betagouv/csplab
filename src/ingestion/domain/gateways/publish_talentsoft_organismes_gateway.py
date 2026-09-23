from typing import Protocol

from infrastructure.external_gateways.dtos.talentsoft_dtos import (
    TalentsoftOrganisationPayload,
)


class IPublishTalentsoftOrganismesGateway(Protocol):
    async def publish(
        self, organisations: list[TalentsoftOrganisationPayload]
    ) -> None: ...
