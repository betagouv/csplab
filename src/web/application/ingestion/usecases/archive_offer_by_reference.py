from domain.interfaces.usecase_interface import IUseCase
from domain.repositories.offers_repository_interface import IOffersRepository
from domain.repositories.vector_repository_interface import IVectorRepository


class ArchiveOfferByReferenceUseCase(IUseCase[str, None]):
    def __init__(
        self,
        offers_repository: IOffersRepository,
        vector_repository: IVectorRepository,
    ) -> None:
        self.offers_repository = offers_repository
        self.vector_repository = vector_repository

    def execute(self, reference: str) -> None:
        offer = self.offers_repository.get_by_reference(reference)
        self.vector_repository.delete_vectorized_documents([offer.id])
        self.offers_repository.mark_as_archived([offer])
