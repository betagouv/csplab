from typing import Any, List, Protocol, Tuple, TypedDict

from domain.entities.document import Document, DocumentType


class IUpsertError(TypedDict):
    entity_id: Any
    error: str
    exception: Exception


class IUpsertResult(TypedDict):
    created: int
    updated: int
    errors: List[IUpsertError]
    external_ids: List[str | None]


class IDocumentRepository(Protocol):
    def find_by_type(
        self, document_type: DocumentType, start: int, batch_size: int = 1000
    ) -> Tuple[List[Document], bool]: ...

    def upsert_batch(
        self, documents: List[Document], document_type: DocumentType
    ) -> IUpsertResult: ...
