from ddd.services.logger_interface import ILogger
from ddd.usecase_interface import IUseCase
from referentiel.repositories.offers_repository_interface import IOffersRepository
from referentiel.types import IUpsertResult

from application.ingestion.interfaces.upsert_offers_input import (
    UpsertOffersInput,
)


class UpsertOffersUseCase(IUseCase[UpsertOffersInput, IUpsertResult]):
    def __init__(self, offers_repository: IOffersRepository, logger: ILogger):
        self.offers_repository = offers_repository
        self.logger = logger

    def execute(self, input_data: UpsertOffersInput) -> IUpsertResult:
        self.logger.info("UpsertOffers: upserting %d offers", len(input_data.offers))
        result = self.offers_repository.upsert_batch(input_data.offers)
        self.logger.info(
            "UpsertOffers: created=%d updated=%d errors=%d",
            result["created"],
            result["updated"],
            len(result["errors"]),
        )
        return result
