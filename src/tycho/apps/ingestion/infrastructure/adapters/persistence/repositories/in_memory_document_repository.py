"""In-memory implementation of document repository for testing."""

from datetime import datetime
from typing import List

from core.entities.document import Document, DocumentType
from core.repositories.document_repository_interface import (
    IDocumentRepository,
    IUpsertResult,
)


class InMemoryDocumentRepository(IDocumentRepository):
    """In-memory implementation of document repository for testing."""

    def __init__(self) -> None:
        """Initialize with empty document storage."""
        self._documents: List[Document] = []
        self._next_id = 1

    def fetch_by_type(self, document_type: DocumentType) -> List[Document]:
        """Get documents by type."""
        return [doc for doc in self._documents if doc.type == document_type]

    def upsert(self, document: Document) -> Document:
        """Insert or update a document."""
        for i, existing_doc in enumerate(self._documents):
            if existing_doc.id == document.id:
                updated_doc = Document(
                    id=document.id,
                    raw_data=document.raw_data,
                    type=document.type,
                    created_at=existing_doc.created_at,
                    updated_at=datetime.now(),
                )
                self._documents[i] = updated_doc
                return updated_doc

        if document.id is None:
            document.id = self._next_id
            self._next_id += 1

        new_doc = Document(
            id=document.id,
            raw_data=document.raw_data,
            type=document.type,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        self._documents.append(new_doc)
        return new_doc

    def upsert_batch(self, documents: List[Document]) -> IUpsertResult:
        """Insert or update multiple documents."""
        created = 0
        updated = 0

        for document in documents:
            # Check if document exists
            exists = any(
                doc.id == document.id
                for doc in self._documents
                if document.id is not None
            )

            self.upsert(document)

            if exists:
                updated += 1
            else:
                created += 1

        return IUpsertResult(
            created=created,
            updated=updated,
        )

    def clear(self) -> None:
        """Clear all documents for testing."""
        self._documents.clear()
        self._next_id = 1
