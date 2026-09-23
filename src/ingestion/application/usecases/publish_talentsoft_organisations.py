import logging
from dataclasses import dataclass

from ddd.async_usecase_interface import IAsyncUsecase

from domain.gateways.publish_talentsoft_organismes_gateway import (
    IPublishTalentsoftOrganismesGateway,
)
from infrastructure.external_gateways.dtos.talentsoft_dtos import (
    TalentsoftOrganisationPayload,
)

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class PublishTalentsoftOrganisationsCommand:
    batches: list[list[TalentsoftOrganisationPayload]]


class PublishTalentsoftOrganisationsUsecase(
    IAsyncUsecase[PublishTalentsoftOrganisationsCommand, None]
):
    def __init__(
        self,
        publish_talentsoft_organismes_gateway: IPublishTalentsoftOrganismesGateway,
    ) -> None:
        self._gateway = publish_talentsoft_organismes_gateway

    async def execute(self, command: PublishTalentsoftOrganisationsCommand) -> None:
        total = 0
        for batch in command.batches:
            await self._gateway.publish(batch)
            total += len(batch)

        logger.info("Published %d Talentsoft organisations", total)
