import logging
from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import UUID

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
        # The web resolves a parent by its external_id among the organismes
        # it already knows: parents are published before their children.
        organismes = _parents_first(command.organismes)
        external_ids = {o.entity_id: o.external_id for o in organismes}
        total = 0
        for start in range(0, len(organismes), BATCH_SIZE):
            batch = organismes[start : start + BATCH_SIZE]
            await self._gateway.publish(batch, external_ids)
            await self._raw_organisme_repository.mark_as_upserted_batch(
                [(organisme.referentiel, organisme.external_id) for organisme in batch],
                datetime.now(tz=timezone.utc),
            )
            total += len(batch)

        logger.info("Published %d organismes", total)


def _parents_first(organismes: list[Organisme]) -> list[Organisme]:
    parent_ids: dict[UUID, UUID | None] = {o.entity_id: o.parent_id for o in organismes}

    def depth(organisme: Organisme) -> int:
        seen: set[UUID] = set()
        parent_id = organisme.parent_id
        while parent_id in parent_ids and parent_id not in seen:
            seen.add(parent_id)
            parent_id = parent_ids[parent_id]
        return len(seen)

    return sorted(organismes, key=depth)
