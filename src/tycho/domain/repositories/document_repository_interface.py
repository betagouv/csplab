"""Document repository interface for local persistence."""

from typing import Any, List, Protocol, Tuple, TypedDict

from domain.entities.document import Document, DocumentType


class IUpsertError(TypedDict):
    """Details of an upsert error."""

    entity_id: Any
    error: str
    exception: Exception


class IUpsertResult(TypedDict):
    """Result of upsert batch operation."""

    created: int
    updated: int
    errors: List[IUpsertError]


class IDocumentRepository(Protocol):
    def find_by_type(
        self, document_type: DocumentType, start: int, batch_size: int = 1000
    ) -> Tuple[List[Document], bool]: ...

    def upsert_batch(
        self, documents: List[Document], document_type: DocumentType
    ) -> IUpsertResult: ...
