"""Django implementation of document repository."""

from typing import List

from core.entities.document import Document, DocumentType
from core.interfaces.document_repository_interface import (
    IDocumentRepository,
    IUpsertResult,
)


class DjangoDocumentRepository(IDocumentRepository):
    """Django implementation of document repository."""

    def fetch_by_type(self, document_type: DocumentType) -> List[Document]:
        """Fetch documents by type."""
        # TODO: Implement with Django ORM
        return []

    def upsert(self, document: Document) -> Document:
        """Insert or update a document."""
        # TODO: Implement with Django ORM
        return document

    def upsert_batch(self, documents: List[Document]) -> IUpsertResult:
        """Insert or update multiple documents."""
        # TODO: Implement with Django ORM
        return IUpsertResult(created=0, updated=0)
