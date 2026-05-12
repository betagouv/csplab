from domain.interfaces.usecase_interface import IUseCase
from domain.repositories.offers_repository_interface import IOffersRepository


class ArchiveOfferByReferenceUseCase(IUseCase[str, None]):
    def __init__(self, offers_repository: IOffersRepository) -> None:
        self.offers_repository = offers_repository

    def execute(self, reference: str) -> None:
        offer = self.offers_repository.get_by_reference(reference)
        self.offers_repository.mark_as_archived([offer])
