from datetime import datetime
from typing import Any, Dict, Optional

from django.utils import timezone

from domain.entities.document import Document, DocumentType
from infrastructure.django_apps.ingestion.models.raw_document import RawDocument


class RawDocumentFactory:
    @staticmethod
    def create(
        external_id: Optional[str] = None,
        document_type: DocumentType = DocumentType.OFFERS,
        raw_data: Optional[Dict[str, Any]] = None,
        updated_at: Optional[datetime] = None,
        processing: bool = False,
        processed_at: Optional[datetime] = None,
        save_in_db: Optional[bool] = True,
    ) -> RawDocument:
        if external_id is None:
            external_id = (
                f"test_{document_type.value.lower()}_{datetime.now().timestamp()}"
            )
        if raw_data is None:
            raw_data = {
                "id": external_id,
                "name": f"Test {document_type.value}",
                "description": f"Test document of type {document_type.value}",
            }

        if processed_at:
            processed_at = timezone.make_aware(processed_at)

        document_entity = Document(
            external_id=external_id,
            raw_data=raw_data,
            type=document_type,
            created_at=timezone.make_aware(datetime.now()),
            processing=processing,
            processed_at=processed_at,
        )

        raw_document = RawDocument.from_entity(document_entity)
        if save_in_db:
            raw_document.save()

            if updated_at:
                RawDocument.objects.filter(id=raw_document.id).update(
                    updated_at=timezone.make_aware(updated_at)
                )
                raw_document.refresh_from_db()

        return raw_document

    @staticmethod
    def create_batch(
        count: int,
        document_type: DocumentType = DocumentType.OFFERS,
        **kwargs,
    ) -> list[RawDocument]:
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
