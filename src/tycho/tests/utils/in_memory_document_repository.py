"""In-memory implementation of document repository for testing."""

from datetime import datetime
from typing import List, Tuple

from domain.entities.document import Document, DocumentType
from domain.repositories.document_repository_interface import (
    IDocumentRepository,
    IUpsertError,
    IUpsertResult,
)


class InMemoryDocumentRepository(IDocumentRepository):
    """In-memory implementation of document repository for testing."""

    def __init__(self) -> None:
        """Initialize with empty document storage."""
        self._documents: List[Document] = []
        self._next_id = 1

    def fetch_by_type(
        self, document_type: DocumentType, start: int, batch_size: int = 1000
    ) -> Tuple[List[Document], bool]:
        """Get documents by type."""
        has_more = False
        return [doc for doc in self._documents if doc.type == document_type], has_more

    def upsert_batch(
        self, documents: List[Document], document_type: DocumentType
    ) -> IUpsertResult:
        """Insert or update multiple documents."""
        created = 0
        updated = 0
        errors: List[IUpsertError] = []

        for document in documents:
            try:
                # Check if document exists and update it
                updated_existing = False
                for i, existing_doc in enumerate(self._documents):
                    if existing_doc.id == document.id:
                        updated_doc = Document(
                            id=document.id,
                            external_id=document.external_id,
                            raw_data=document.raw_data,
                            type=document.type,
                            created_at=existing_doc.created_at,
                            updated_at=datetime.now(),
                        )
                        self._documents[i] = updated_doc
                        updated += 1
                        updated_existing = True
                        break

                # If not updated, create new document
                if not updated_existing:
                    doc_id = document.id
                    if doc_id is None:
                        doc_id = self._next_id
                        self._next_id += 1

                    new_doc = Document(
                        id=doc_id,
                        external_id=document.external_id,
                        raw_data=document.raw_data,
                        type=document.type,
                        created_at=datetime.now(),
                        updated_at=datetime.now(),
                    )
                    self._documents.append(new_doc)
                    created += 1

            except Exception as e:
                error_detail: IUpsertError = {
                    "entity_id": document.id,
                    "error": str(e),
                    "exception": e,
                }
                errors.append(error_detail)

        return {
            "created": created,
            "updated": updated,
            "errors": errors,
        }

    def clear(self) -> None:
        """Clear all documents for testing."""
        self._documents.clear()
        self._next_id = 1
