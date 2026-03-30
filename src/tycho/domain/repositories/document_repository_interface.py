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


class IDocumentRepository(Protocol):
    def find_by_type(
        self, document_type: DocumentType, start: int, batch_size: int = 1000
    ) -> Tuple[List[Document], bool]: ...

    def find_by_external_ids(
        self, document_type: DocumentType, documents: List[Document]
    ) -> List[Document]: ...

    def get_documents_to_upsert(
        self,
        document_type: DocumentType,
        fetched_documents: List[Document],
        existing_documents: List[Document],
    ) -> List[Document]: ...

    def upsert_batch(
        self, documents: List[Document], document_type: DocumentType
    ) -> IUpsertResult: ...

    def get_pending_processing(
        self,
        document_type: DocumentType,
        limit: int = 1000,
    ) -> List[Document]: ...

    def mark_as_processed(self, raw_documents: List[Document]) -> int: ...

    def mark_as_pending(self, raw_documents: List[Document]) -> int: ...
