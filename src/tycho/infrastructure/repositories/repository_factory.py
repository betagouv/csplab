"""Repository factory implementation for entity persistence."""

from typing import Union

from domain.entities.document import DocumentType
from domain.exceptions.document_error import UnsupportedDocumentTypeError
from domain.repositories.concours_repository_interface import IConcoursRepository
from domain.repositories.corps_repository_interface import ICorpsRepository
from domain.repositories.repository_factory_interface import IRepositoryFactory


class RepositoryFactory(IRepositoryFactory):
    """Factory that provides appropriate repositories by entity type."""

    def __init__(
        self,
        corps_repository: ICorpsRepository,
        concours_repository: IConcoursRepository,
    ):
        """Initialize with repository dependencies."""
        self.corps_repository = corps_repository
        self.concours_repository = concours_repository

    def get_repository(
        self, document_type: DocumentType
    ) -> Union[ICorpsRepository, IConcoursRepository]:
        """Get the appropriate repository for the given document type."""
        match document_type:
            case DocumentType.CORPS:
                return self.corps_repository
            case DocumentType.CONCOURS:
                return self.concours_repository

        raise UnsupportedDocumentTypeError(
            f"No repository available for document type: {document_type}"
        )
