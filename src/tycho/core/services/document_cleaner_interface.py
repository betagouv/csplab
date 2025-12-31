"""Document cleaner interface definitions."""

from typing import Generic, List, Protocol, Sequence, TypeVar

from core.interfaces.entity_interface import IEntity
from domain.entities.document import Document

T_co = TypeVar("T_co", bound=IEntity, covariant=True)


class IDocumentCleaner(Protocol, Generic[T_co]):
    """Interface for document cleaners."""

    def clean(self, raw_documents: List[Document]) -> Sequence[T_co]:
        """Clean raw documents and return typed entities that implement IEntity."""
        ...
