import logging
from dataclasses import dataclass
from uuid import UUID

from ddd.async_usecase_interface import IAsyncUsecase

from application.usecases._talentsoft_source import resolve_source_and_client
from domain.repositories.sources_repository import ISourcesRepository
from infrastructure.exceptions.exceptions import ExternalApiError
from infrastructure.external_gateways.dtos.talentsoft_dtos import (
    TalentsoftOrganisationPayload,
)
from infrastructure.talentsoft_client_repository import TalentsoftClientRepository

logger = logging.getLogger(__name__)

BATCH_SIZE = 100


@dataclass(frozen=True)
class PrepareTalentsoftOrganisationsCommand:
    source_id: UUID


class PrepareTalentsoftOrganisationsUsecase(
    IAsyncUsecase[
        PrepareTalentsoftOrganisationsCommand, list[list[TalentsoftOrganisationPayload]]
    ]
):
    def __init__(
        self,
        sources_repository: ISourcesRepository,
        talentsoft_client_repository: TalentsoftClientRepository,
    ) -> None:
        self._sources_repository = sources_repository
        self._talentsoft_client_repository = talentsoft_client_repository

    async def execute(
        self, command: PrepareTalentsoftOrganisationsCommand
    ) -> list[list[TalentsoftOrganisationPayload]]:
        _, client = resolve_source_and_client(
            command.source_id,
            self._sources_repository,
            self._talentsoft_client_repository,
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
            command.source_id,
        )

        return batches
