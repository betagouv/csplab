"""Repository factory implementation for entity persistence."""

from core.entities.document import DocumentType
from core.repositories.corps_repository_interface import ICorpsRepository
from core.repositories.repository_factory_interface import IRepositoryFactory


class RepositoryFactory(IRepositoryFactory):
    """Factory that provides appropriate repositories by entity type."""

    def __init__(self, corps_repository: ICorpsRepository):
        """Initialize with repository dependencies."""
        self.corps_repository = corps_repository

    def get_repository(self, document_type: DocumentType) -> ICorpsRepository:
        """Get the appropriate repository for the given document type."""
        if document_type == DocumentType.CORPS:
            return self.corps_repository

        raise ValueError(f"No repository available for document type: {document_type}")
