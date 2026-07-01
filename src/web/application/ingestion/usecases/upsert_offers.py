from ddd.services.logger_interface import ILogger
from ddd.usecase_interface import IUseCase
from referentiel.types import IUpsertResult

from application.ingestion.interfaces.upsert_offers_input import UpsertOffersInput
from domain.identite.repositories.utilisateur_repository_interface import (
    IUtilisateurRepository,
)
from domain.ingestion.exceptions.source_authorization_error import (
    SourceAuthorizationError,
)
from domain.ingestion.repositories.ingestion_offers_repository_interface import (
    IIngestionOffersRepository,
)
from domain.ingestion.repositories.user_source_repository_interface import (
    IUserSourceRepository,
)


class UpsertOffersUseCase(IUseCase[UpsertOffersInput, IUpsertResult]):
    def __init__(
        self,
        offers_repository: IIngestionOffersRepository,
        logger: ILogger,
        user_source_repository: IUserSourceRepository,
        utilisateur_repository: IUtilisateurRepository,
    ):
        self.offers_repository = offers_repository
        self.logger = logger
        self.user_source_repository = user_source_repository
        self.utilisateur_repository = utilisateur_repository

    def execute(self, input_data: UpsertOffersInput) -> IUpsertResult:
        if input_data.utilisateur_entity_id is not None:
            utilisateur = self.utilisateur_repository.get_by_entity_id(
                input_data.utilisateur_entity_id
            )
            source_ids = {input_data.source_id}
            allowed = self.user_source_repository.get_allowed_source_ids(
                utilisateur, source_ids
            )
            if allowed != source_ids:
                raise SourceAuthorizationError(source_ids - allowed)

        self.logger.info("UpsertOffers: upserting %d offers", len(input_data.offers))
        result = self.offers_repository.upsert_batch(input_data.offers)
        self.logger.info(
            "UpsertOffers: created=%d updated=%d errors=%d",
            result["created"],
            result["updated"],
            len(result["errors"]),
        )
        return result
