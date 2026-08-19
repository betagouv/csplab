import logging
from datetime import datetime, timezone

from domain.entities.raw_organisme import RawOrganisme
from domain.gateways.organisme_gateway import IOrganismeGateway
from domain.repositories.raw_organisme_repository import IRawOrganismeRepository

logger = logging.getLogger(__name__)

BATCH_SIZE = 500


class ImportOrganismesUseCase:
    def __init__(
        self,
        organisme_gateway: IOrganismeGateway,
        raw_organisme_repository: IRawOrganismeRepository,
    ) -> None:
        self._organisme_gateway = organisme_gateway
        self._raw_organisme_repository = raw_organisme_repository

    async def execute(self) -> None:
        resource = self._organisme_gateway.find_resource()
        millesime = resource.millesime.isoformat()
        loaded_at = datetime.now(tz=timezone.utc)

        total = 0
        referentiel: str | None = None
        batch: list[RawOrganisme] = []
        for organisme_data in self._organisme_gateway.stream_organismes(resource):
            referentiel = organisme_data.referentiel
            batch.append(
                RawOrganisme(
                    referentiel=organisme_data.referentiel,
                    millesime=millesime,
                    external_id=organisme_data.external_id,
                    data=organisme_data.data,
                    loaded_at=loaded_at,
                )
            )
            if len(batch) >= BATCH_SIZE:
                await self._raw_organisme_repository.upsert_batch(batch)
                total += len(batch)
                batch = []

        if batch:
            await self._raw_organisme_repository.upsert_batch(batch)
            total += len(batch)

        logger.info("Imported %d organismes for millesime %s", total, millesime)

        if referentiel is not None:
            deleted = await self._raw_organisme_repository.delete_missing(
                referentiel, loaded_at
            )
            logger.info(
                "Deleted %d organismes missing from latest import for referentiel %s",
                deleted,
                referentiel,
            )
