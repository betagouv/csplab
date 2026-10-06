from dataclasses import replace
from datetime import datetime
from zoneinfo import ZoneInfo

from ddd.services.logger_interface import ILogger
from ddd.usecase_interface import IUsecase
from referentiel.entities.offer import Offer

from application.ingestion.interfaces.upsert_offers_input import UpsertOffersInput
from domain.identite.repositories.utilisateur_repository_interface import (
    IUtilisateurRepository,
)
from domain.ingestion.exceptions.source_authorization_error import (
    SourceAuthorizationError,
)
from domain.ingestion.repositories.ingestion_offers_repository_interface import (
    IIngestionOffersRepository,
    IOffersUpsertResult,
)
from domain.ingestion.repositories.user_source_repository_interface import (
    IUserSourceRepository,
)
from infrastructure.django_apps.referentiel.models.offer_reference_sequence import (
    OfferReferenceSequenceModel,
)

AUTO_REFERENCE = "auto"
TIMEZONE = ZoneInfo("Europe/Paris")


class UpsertOffersUsecase(IUsecase[UpsertOffersInput, IOffersUpsertResult]):
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

    def execute(self, input_data: UpsertOffersInput) -> IOffersUpsertResult:
        if input_data.utilisateur_username is not None:
            utilisateur = self.utilisateur_repository.get_by_username(
                input_data.utilisateur_username
            )
            source_ids = {input_data.source_id}
            allowed = self.user_source_repository.get_allowed_source_ids(
                utilisateur, source_ids
            )
            if allowed != source_ids:
                raise SourceAuthorizationError(source_ids - allowed)

        offers = self._generate_auto_references(input_data.offers)

        self.logger.info("UpsertOffers: upserting %d offers", len(offers))
        result = self.offers_repository.upsert_batch(offers)
        self.logger.info(
            "UpsertOffers: created=%d updated=%d errors=%d",
            result["created"],
            result["updated"],
            len(result["errors"]),
        )
        return result

    def _generate_auto_references(self, offers: list[Offer]) -> list[Offer]:
        auto_count = sum(1 for offer in offers if offer.reference == AUTO_REFERENCE)
        if not auto_count:
            return offers

        references = iter(
            OfferReferenceSequenceModel.objects.next_references(
                year=datetime.now(TIMEZONE).year, count=auto_count
            )
        )
        return [
            replace(offer, reference=next(references))
            if offer.reference == AUTO_REFERENCE
            else offer
            for offer in offers
        ]
