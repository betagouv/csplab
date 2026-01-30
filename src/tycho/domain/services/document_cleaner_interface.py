"""Document cleaner interface definitions."""

from dataclasses import dataclass
from typing import Dict, Generic, List, Protocol, TypeVar

from domain.entities.document import Document
from domain.interfaces.entity_interface import IEntity

T_co = TypeVar("T_co", bound=IEntity, covariant=True)


@dataclass
class CleaningResult(Generic[T_co]):
    """Result of document cleaning operation."""

    entities: List[T_co]
    cleaning_errors: List[Dict[str, str]]


class IDocumentCleaner(Protocol, Generic[T_co]):
    """Interface for document cleaners."""

    def clean(self, raw_documents: List[Document]) -> CleaningResult[T_co]:
        """Clean raw documents and return cleaning result with entities and errors."""
        ...
