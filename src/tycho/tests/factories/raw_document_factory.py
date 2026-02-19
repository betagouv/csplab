"""Factory for generating test RawDocument instances."""

from datetime import datetime, timezone
from typing import Any, Dict, Optional

from domain.entities.document import Document, DocumentType
from infrastructure.django_apps.ingestion.models.raw_document import RawDocument


class RawDocumentFactory:
    """Factory for creating RawDocument test instances."""

    @staticmethod
    def create(
        external_id: Optional[str] = None,
        document_type: DocumentType = DocumentType.OFFERS,
        raw_data: Optional[Dict[str, Any]] = None,
    ) -> RawDocument:
        """Create a RawDocument instance."""
        if external_id is None:
            external_id = (
                f"test_{document_type.value.lower()}_"
                f"{datetime.now(timezone.utc).timestamp()}"
            )
        if raw_data is None:
            raw_data = {
                "id": external_id,
                "name": f"Test {document_type.value}",
                "description": f"Test document of type {document_type.value}",
            }

        document_entity = Document(
            external_id=external_id,
            raw_data=raw_data,
            type=document_type,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            processed_at=None,
        )

        raw_document = RawDocument.from_entity(document_entity)
        raw_document.save()

        return raw_document

    @staticmethod
    def create_batch(
        count: int,
        document_type: DocumentType = DocumentType.OFFERS,
        **kwargs,
    ) -> list[RawDocument]:
        """Create multiple RawDocument instances."""
        documents = []
        for i in range(count):
            external_id = kwargs.get(
                "external_id", f"{document_type.value.lower()}_{i}"
            )
            if "external_id" in kwargs:
                external_id = f"{kwargs['external_id']}_{i}"

            raw_data = kwargs.get("raw_data", {}).copy()
            raw_data["id"] = i
            raw_data["name"] = raw_data.get("name", f"{document_type.value} {i}")

            doc = RawDocumentFactory.create(
                external_id=external_id,
                document_type=document_type,
                raw_data=raw_data,
            )
            documents.append(doc)

        return documents
