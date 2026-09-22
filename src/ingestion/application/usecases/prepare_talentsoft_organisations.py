import logging
from uuid import UUID

from application.usecases._talentsoft_source import resolve_source_and_client
from domain.repositories.sources_repository import ISourcesRepository
from infrastructure.exceptions.exceptions import ExternalApiError
from infrastructure.external_gateways.dtos.talentsoft_dtos import (
    TalentsoftOrganisationPayload,
)
from infrastructure.talentsoft_client_repository import TalentsoftClientRepository

logger = logging.getLogger(__name__)

BATCH_SIZE = 100


class PrepareTalentsoftOrganisationsUsecase:
    def __init__(
        self,
        sources_repository: ISourcesRepository,
        talentsoft_client_repository: TalentsoftClientRepository,
        dgafp_source_id: UUID | None,
    ) -> None:
        self._sources_repository = sources_repository
        self._talentsoft_client_repository = talentsoft_client_repository
        self._dgafp_source_id = dgafp_source_id

    async def execute(self) -> list[list[TalentsoftOrganisationPayload]]:
        if self._dgafp_source_id is None:
            raise ValueError("TALENTSOFT_DGAFP_SOURCE_ID is not configured")

        source, client = resolve_source_and_client(
            self._dgafp_source_id,
            self._sources_repository,
            self._talentsoft_client_repository,
        )

        if not source.is_dgafp(self._dgafp_source_id):
            raise ValueError(
                f"Source {self._dgafp_source_id} is not the DGAFP Talentsoft source"
            )

        referentiel = await client.get_organisations_referentiel()

        payloads: list[TalentsoftOrganisationPayload] = []
        for item in referentiel:
            try:
                detail = await client.get_organisation_detail(item.code)
            except ExternalApiError:
                logger.exception(
                    "Failed to fetch Talentsoft organisation detail for code %s",
                    item.code,
                )
                continue
            payloads.append(
                TalentsoftOrganisationPayload.from_referentiel_and_detail(item, detail)
            )

        batches = [
            payloads[start : start + BATCH_SIZE]
            for start in range(0, len(payloads), BATCH_SIZE)
        ]

        logger.info(
            "Prepared %d Talentsoft organisations in %d batches for source %s",
            len(payloads),
            len(batches),
            self._dgafp_source_id,
        )

        return batches
