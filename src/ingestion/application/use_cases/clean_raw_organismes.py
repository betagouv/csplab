import logging
from datetime import datetime, timezone

from domain.entities.organisme import Organisme
from domain.gateways.organismes_cleaner import IOrganismesCleaner
from domain.repositories.raw_organisme_repository import IRawOrganismeRepository

logger = logging.getLogger(__name__)

BATCH_SIZE = 500


class CleanRawOrganismesUseCase:
    def __init__(
        self,
        organismes_cleaner: IOrganismesCleaner,
        raw_organisme_repository: IRawOrganismeRepository,
    ) -> None:
        self._organismes_cleaner = organismes_cleaner
        self._raw_organisme_repository = raw_organisme_repository

    async def execute(self, referentiel: str) -> list[Organisme]:
        organismes: list[Organisme] = []
        total_raw = 0

        while True:
            raw_batch = await self._raw_organisme_repository.find_uncleaned(
                referentiel, BATCH_SIZE
            )
            if not raw_batch:
                break

            cleaned_ids = []
            for raw_organisme in raw_batch:
                cleaned_ids.append(raw_organisme.id)
                try:
                    organisme = self._organismes_cleaner.clean(raw_organisme)
                except Exception:
                    logger.exception(
                        "Failed to clean raw organisme %s", raw_organisme.external_id
                    )
                    continue
                if organisme is not None:
                    organismes.append(organisme)

            await self._raw_organisme_repository.mark_as_cleaned_batch(
                cleaned_ids, datetime.now(tz=timezone.utc)
            )
            total_raw += len(raw_batch)

            if len(raw_batch) < BATCH_SIZE:
                break

        logger.info(
            "Cleaned %d raw organismes into %d organismes for referentiel %s",
            total_raw,
            len(organismes),
            referentiel,
        )
        return organismes
