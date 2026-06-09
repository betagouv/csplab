"""Document cleaner interface definitions."""

from dataclasses import dataclass
from typing import Dict, Generic, List, Protocol, TypeVar

from ddd.entity import Entity

from domain.ingestion.entities.document import Document

T_co = TypeVar("T_co", bound=Entity, covariant=True)


@dataclass
class CleaningResult(Generic[T_co]):
    entities: List[T_co]
    cleaning_errors: List[Dict[str, str]]


class IDocumentCleaner(Protocol, Generic[T_co]):
    def clean(self, raw_documents: List[Document]) -> CleaningResult[T_co]: ...
