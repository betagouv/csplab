import logging
from uuid import UUID

from application.use_cases._talentsoft_source import resolve_source_and_client
from application.use_cases.archive_offer import ArchiveOfferUseCase
from domain.gateways.offers_by_source_gateway import IOffersBySourceGateway
from domain.repositories.sources_repository import ISourcesRepository
from infrastructure.talentsoft_client_repository import TalentsoftClientRepository

logger = logging.getLogger(__name__)

_BATCH_SIZE = 1_000


class BatchArchiveOffersUseCase:
    def __init__(
        self,
        web_offers_gateway: IOffersBySourceGateway,
        sources_repository: ISourcesRepository,
        talentsoft_client_repository: TalentsoftClientRepository,
        archive_offer_use_case: ArchiveOfferUseCase,
    ) -> None:
        self._web_offers_gateway = web_offers_gateway
        self._sources_repository = sources_repository
        self._talentsoft_client_repository = talentsoft_client_repository
        self._archive_offer_use_case = archive_offer_use_case

    async def execute(self, source_id: UUID) -> None:
        _, client = resolve_source_and_client(
            source_id, self._sources_repository, self._talentsoft_client_repository
        )

        web_references = set(await self._web_offers_gateway.fetch_references(source_id))

        talentsoft_references: set[str] = set()
        start = 1
        has_more = True

        while has_more:
            offers, has_more = await client.get_all(count=_BATCH_SIZE, start=start)
            for offer in offers:
                talentsoft_references.add(offer.reference)
            start += 1

        to_archive = web_references - talentsoft_references

        if to_archive:
            logger.info("Offers to archive for source %s: %s", source_id, to_archive)

        for reference in to_archive:
            await self._archive_offer_use_case.execute(
                reference=reference, source_id=str(source_id)
            )

        logger.info("Archived %d offers for source %s", len(to_archive), source_id)
