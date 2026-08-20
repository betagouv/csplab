import logging

from referentiel.entities.organisme import Organisme

from domain.gateways.publish_organismes_gateway import IPublishOrganismesGateway

logger = logging.getLogger(__name__)

BATCH_SIZE = 100


class PublishOrganismesUseCase:
    def __init__(self, publish_organismes_gateway: IPublishOrganismesGateway) -> None:
        self._gateway = publish_organismes_gateway

    async def execute(self, organismes: list[Organisme]) -> None:
        total = 0
        for start in range(0, len(organismes), BATCH_SIZE):
            batch = organismes[start : start + BATCH_SIZE]
            await self._gateway.publish(batch)
            total += len(batch)

        logger.info("Published %d organismes", total)
