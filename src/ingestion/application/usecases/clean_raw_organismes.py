import logging
from datetime import datetime, timezone
from itertools import chain
from typing import Optional
from uuid import UUID

from pydantic import ValidationError
from referentiel.entities.organisme import Organisme

from domain.entities.raw_organisme import RawOrganisme
from domain.gateways.organismes_cleaner import IOrganismesCleaner
from domain.gateways.siret_lookup_gateway import ISiretLookupGateway
from domain.repositories.raw_organisme_repository import IRawOrganismeRepository

logger = logging.getLogger(__name__)

BATCH_SIZE = 500


class CleanRawOrganismesUsecase:
    def __init__(
        self,
        organismes_cleaner: IOrganismesCleaner,
        raw_organisme_repository: IRawOrganismeRepository,
        siret_lookup_gateway: Optional[ISiretLookupGateway] = None,
    ) -> None:
        self._organismes_cleaner = organismes_cleaner
        self._raw_organisme_repository = raw_organisme_repository
        self._siret_lookup_gateway = siret_lookup_gateway

    async def execute(self, referentiel: str) -> list[Organisme]:
        total_raw = 0
        total_cleaned = 0
        deduped_organismes: list[Organisme] = []

        while True:
            raw_batch = await self._raw_organisme_repository.find_uncleaned(
                referentiel, BATCH_SIZE
            )
            if not raw_batch:
                break

            await self._resolve_missing_dila_sirets(raw_batch)

            cleaned_ids = []
            cleaned_batch: list[Organisme] = []
            for raw_organisme in raw_batch:
                cleaned_ids.append(raw_organisme.id)
                try:
                    organisme = self._organismes_cleaner.clean(raw_organisme)
                except ValidationError as e:
                    logger.warning(
                        "Invalid data for raw organisme %s: %s",
                        raw_organisme.external_id,
                        e,
                    )
                    continue
                except Exception:
                    logger.exception(
                        "Unexpected error cleaning raw organisme %s",
                        raw_organisme.external_id,
                    )
                    continue
                if organisme is not None:
                    cleaned_batch.append(organisme)

            await self._raw_organisme_repository.mark_as_cleaned_batch(
                cleaned_ids, datetime.now(tz=timezone.utc)
            )
            total_raw += len(raw_batch)
            total_cleaned += len(cleaned_batch)

            # Dedupe per batch: bounds memory by unique SIRETs, not raw count.
            deduped_organismes = self._organismes_cleaner.dedupe_by_siret(
                chain(deduped_organismes, cleaned_batch)
            )

            if len(raw_batch) < BATCH_SIZE:
                break

        logger.info(
            "Cleaned %d raw organismes into %d organismes (%d after SIRET dedup) "
            "for referentiel %s",
            total_raw,
            total_cleaned,
            len(deduped_organismes),
            referentiel,
        )
        return deduped_organismes

    async def _resolve_missing_dila_sirets(self, raw_batch: list[RawOrganisme]) -> None:
        if self._siret_lookup_gateway is None:
            return

        found_at = datetime.now(tz=timezone.utc)
        updates: list[tuple[UUID, Optional[str], datetime]] = []
        for raw_organisme in raw_batch:
            nom = self._organismes_cleaner.nom_for_dila_siret_lookup(raw_organisme)
            if nom is None:
                continue
            siret = self._siret_lookup_gateway.find_siret(nom) or ""
            raw_organisme.dila_siret_found = siret
            raw_organisme.dila_siret_found_at = found_at
            updates.append((raw_organisme.id, siret, found_at))

        await self._raw_organisme_repository.mark_dila_siret_found_batch(updates)
