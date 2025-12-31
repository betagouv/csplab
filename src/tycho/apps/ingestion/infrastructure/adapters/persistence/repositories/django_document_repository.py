"""Django document repository implementation."""

from typing import List

from apps.ingestion.infrastructure.adapters.persistence.models.raw_document import (
    RawDocument,
)
from domain.entities.document import Document, DocumentType
from domain.repositories.document_repository_interface import (
    IDocumentRepository,
    IUpsertError,
    IUpsertResult,
)


class DjangoDocumentRepository(IDocumentRepository):
    """Complete document repository using Django ORM."""

    def fetch_by_type(self, document_type: DocumentType) -> List[Document]:
        """Fetch documents from Django database by type."""
        raw_documents = RawDocument.objects.filter(document_type=document_type.value)
        return [raw_doc.to_entity() for raw_doc in raw_documents]

    def upsert_batch(self, documents: List[Document]) -> IUpsertResult:
        """Insert or update multiple documents."""
        created_count = 0
        updated_count = 0
        errors: List[IUpsertError] = []

        for document in documents:
            try:
                if document.external_id:
                    # Upsert based on external_id + document_type
                    _, created = RawDocument.objects.update_or_create(
                        external_id=document.external_id,
                        document_type=document.type.value,
                        defaults={
                            "raw_data": document.raw_data,
                        },
                    )
                else:
                    # Create new document without external_id (fallback)
                    RawDocument.objects.create(
                        raw_data=document.raw_data,
                        document_type=document.type.value,
                        external_id=document.external_id,
                    )
                    created = True

                if created:
                    created_count += 1
                else:
                    updated_count += 1
            except Exception as e:
                error_detail: IUpsertError = {
                    "entity_id": document.id,
                    "error": str(e),
                    "exception": e,
                }
                errors.append(error_detail)

        return {
            "created": created_count,
            "updated": updated_count,
            "errors": errors,
        }
