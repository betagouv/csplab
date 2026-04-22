"""Repository factory implementation for entity persistence."""

from typing import Union

from domain.entities.document import DocumentType
from domain.exceptions.document_error import UnsupportedDocumentTypeError
from domain.repositories.concours_repository_interface import IConcoursRepository
from domain.repositories.corps_repository_interface import ICorpsRepository
from domain.repositories.metier_repository_interface import IMetierRepository
from domain.repositories.offers_repository_interface import IOffersRepository
from domain.repositories.repository_factory_interface import IRepositoryFactory


class RepositoryFactory(IRepositoryFactory):
    def __init__(
        self,
        corps_repository: ICorpsRepository,
        concours_repository: IConcoursRepository,
        offers_repository: IOffersRepository,
        metiers_repository: IMetierRepository,
    ):
        self.corps_repository = corps_repository
        self.concours_repository = concours_repository
        self.offers_repository = offers_repository
        self.metiers_repository = metiers_repository

    def get_repository(
        self, document_type: DocumentType
    ) -> Union[
        ICorpsRepository, IConcoursRepository, IOffersRepository, IMetierRepository
    ]:
        match document_type:
            case DocumentType.CORPS:
                return self.corps_repository
            case DocumentType.CONCOURS:
                return self.concours_repository
            case DocumentType.OFFERS:
                return self.offers_repository
            case DocumentType.METIERS:
                return self.metiers_repository

        raise UnsupportedDocumentTypeError(
            f"No repository available for document type: {document_type}"
        )
