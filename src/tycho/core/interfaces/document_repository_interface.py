"""Document repository interface."""

from typing import List, Protocol, TypedDict

from core.entities.document import Document, DocumentType


class UpsertResult(TypedDict):
    """Result of upsert batch operation."""

    created: int
    updated: int


class IDocumentRepository(Protocol):
    """Interface for document repository operations."""

    def fetch_by_type(self, document_type: DocumentType) -> List[Document]:
        """Fetch documents by type."""
        ...

    def upsert(self, document: Document) -> Document:
        """Insert or update a document."""
        ...

    def upsert_batch(self, documents: List[Document]) -> UpsertResult:
        """Insert or update multiple documents.

        Returns:
            UpsertResult with counts: {'created': int, 'updated': int, 'deleted': int}
        """
        ...
