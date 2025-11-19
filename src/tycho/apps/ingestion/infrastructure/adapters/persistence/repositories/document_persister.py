"""Django document persister implementation."""

from typing import List

from apps.ingestion.infrastructure.adapters.persistence.models.raw_document import (
    RawDocument,
)
from core.entities.document import Document
from core.interfaces.document_repository_interface import (
    IDocumentPersister,
    IUpsertResult,
)


class DjangoDocumentPersister(IDocumentPersister):
    """Persists documents using Django ORM."""

    def upsert(self, document: Document) -> Document:
        """Insert or update a single document."""
        raw_document, created = RawDocument.objects.update_or_create(
            id=document.id,
            defaults={
                "raw_data": document.raw_data,
                "document_type": document.type.value,
            },
        )
        return raw_document.to_entity()

    def upsert_batch(self, documents: List[Document]) -> IUpsertResult:
        """Insert or update multiple documents."""
        created_count = 0
        updated_count = 0

        for document in documents:
            raw_document, created = RawDocument.objects.update_or_create(
                id=document.id,
                defaults={
                    "raw_data": document.raw_data,
                    "document_type": document.type.value,
                },
            )

            if created:
                created_count += 1
            else:
                updated_count += 1

        return IUpsertResult(created=created_count, updated=updated_count)
