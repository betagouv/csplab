"""Document repository interface and composite implementation."""

from typing import Any, List, Protocol, TypedDict

from domain.entities.document import Document, DocumentType


class IDocumentFetcher(Protocol):
    """Interface for fetching documents from external sources."""

    def fetch_by_type(self, document_type: DocumentType) -> List[Document]:
        """Fetch documents from external source by type."""
        ...


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


class IDocumentPersister(Protocol):
    """Interface for persisting documents to local storage."""

    def upsert_batch(self, documents: List[Document]) -> IUpsertResult:
        """Insert or update multiple documents."""
        ...


class IDocumentRepository(Protocol):
    """Interface for document repository operations."""

    def fetch_by_type(self, document_type: DocumentType) -> List[Document]:
        """Fetch documents by type."""
        ...

    def upsert_batch(self, documents: List[Document]) -> IUpsertResult:
        """Insert or update multiple documents."""
        ...


class CompositeDocumentRepository(IDocumentRepository):
    """Composite repository that delegates fetch and store operations."""

    def __init__(self, fetcher: IDocumentFetcher, persister: IDocumentPersister):
        """Initialize with fetcher and persister dependencies."""
        self.fetcher = fetcher
        self.persister = persister

    def fetch_by_type(self, document_type: DocumentType) -> List[Document]:
        """Fetch documents by type using external fetcher."""
        return self.fetcher.fetch_by_type(document_type)

    def upsert_batch(self, documents: List[Document]) -> IUpsertResult:
        """Insert or update multiple documents using persister."""
        return self.persister.upsert_batch(documents)
