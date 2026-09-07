import logging
from dataclasses import dataclass
from datetime import datetime, timezone

from ddd.async_usecase_interface import IAsyncUsecase
from referentiel.entities.organisme import Organisme

from domain.gateways.publish_organismes_gateway import IPublishOrganismesGateway
from domain.repositories.raw_organisme_repository import IRawOrganismeRepository

logger = logging.getLogger(__name__)

BATCH_SIZE = 100


@dataclass(frozen=True)
class PublishOrganismesCommand:
    organismes: list[Organisme]


class PublishOrganismesUsecase(IAsyncUsecase[PublishOrganismesCommand, None]):
    def __init__(
        self,
        publish_organismes_gateway: IPublishOrganismesGateway,
        raw_organisme_repository: IRawOrganismeRepository,
    ) -> None:
        self._gateway = publish_organismes_gateway
        self._raw_organisme_repository = raw_organisme_repository

    async def execute(self, command: PublishOrganismesCommand) -> None:
        organismes = command.organismes
        total = 0
        for start in range(0, len(organismes), BATCH_SIZE):
            batch = organismes[start : start + BATCH_SIZE]
            await self._gateway.publish(batch)
            await self._raw_organisme_repository.mark_as_upserted_batch(
                [(organisme.referentiel, organisme.external_id) for organisme in batch],
                datetime.now(tz=timezone.utc),
            )
            total += len(batch)

        logger.info("Published %d organismes", total)
