from ddd.usecase_interface import IUseCase
from referentiel.entities.offer import Offer
from referentiel.repositories.offers_repository_interface import IOffersRepository

from application.ingestion.interfaces.get_offer_by_reference_input import (
    GetOfferByReferenceInput,
)


class GetOfferByReferenceUseCase(IUseCase[GetOfferByReferenceInput, Offer]):
    def __init__(
        self,
        offers_repository: IOffersRepository,
    ):
        self.offers_repository = offers_repository

    def execute(self, input_data: GetOfferByReferenceInput) -> Offer:
        return self.offers_repository.get_by_reference(input_data.reference)
