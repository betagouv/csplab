from ddd.usecase_interface import IUseCase

from application.ingestion.interfaces.archive_offer_by_reference_input import (
    ArchiveOfferByReferenceInput,
)
from domain.repositories.offers_repository_interface import IOffersRepository
from domain.repositories.vector_repository_interface import IVectorRepository


class ArchiveOfferByReferenceUseCase(IUseCase[ArchiveOfferByReferenceInput, None]):
    def __init__(
        self,
        offers_repository: IOffersRepository,
        vector_repository: IVectorRepository,
    ) -> None:
        self.offers_repository = offers_repository
        self.vector_repository = vector_repository

    def execute(self, input_data: ArchiveOfferByReferenceInput) -> None:
        offer = self.offers_repository.get_by_reference_and_source_id(
            input_data.reference, input_data.source_id
        )
        self.vector_repository.delete_vectorized_documents([offer.id])
        self.offers_repository.mark_as_archived([offer])
