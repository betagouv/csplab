"""Repository factory interface for entity persistence."""

from typing import Protocol, TypeVar, Union

from core.entities.document import DocumentType
from core.repositories.concours_repository_interface import IConcoursRepository
from core.repositories.corps_repository_interface import ICorpsRepository

TRepository = TypeVar("TRepository")


class IRepositoryFactory(Protocol):
    """Interface for repository factory.

    It provides appropriate repositories by entity type.
    """

    def get_repository(
        self, document_type: DocumentType
    ) -> Union[ICorpsRepository, IConcoursRepository]:
        """Get the appropriate repository for the given document type."""
        ...
