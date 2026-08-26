import logging
from dataclasses import dataclass

from ddd.async_usecase_interface import IAsyncUsecase
from referentiel.entities.organisme import Organisme

from domain.gateways.publish_organismes_gateway import IPublishOrganismesGateway

logger = logging.getLogger(__name__)

BATCH_SIZE = 100


@dataclass(frozen=True)
class PublishOrganismesCommand:
    organismes: list[Organisme]


class PublishOrganismesUsecase(IAsyncUsecase[PublishOrganismesCommand, None]):
    def __init__(self, publish_organismes_gateway: IPublishOrganismesGateway) -> None:
        self._gateway = publish_organismes_gateway

    async def execute(self, command: PublishOrganismesCommand) -> None:
        organismes = command.organismes
        total = 0
        for start in range(0, len(organismes), BATCH_SIZE):
            batch = organismes[start : start + BATCH_SIZE]
            await self._gateway.publish(batch)
            total += len(batch)

        logger.info("Published %d organismes", total)
