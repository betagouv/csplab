from datetime import datetime
from typing import Any, Dict, Optional

from django.utils import timezone

from domain.ingestion.entities.document import Document, DocumentType
from infrastructure.factories.datetime_utils import as_aware
from infrastructure.factories.ingestion.ingres_corps_factories import (
    IngresCorpsDocumentFactory,
)
from infrastructure.factories.ingestion.ingres_metiers_factories import (
    IngresMetiersDocumentFactory,
)
from infrastructure.factories.referentiel.concours_row_factory import ConcoursRowFactory


class DocumentFactory:
    @staticmethod
    def _generate_raw_data_and_external_id(
        document_type: DocumentType, external_id: Optional[str]
    ) -> tuple[Dict[str, Any], str]:
        if document_type == DocumentType.METIERS:
            metier_dto = IngresMetiersDocumentFactory.build()
            raw_data = metier_dto.model_dump()
            if external_id is None:
                external_id = f"metier_{metier_dto.identifiant}"
        elif document_type == DocumentType.CORPS:
            corps_dto = IngresCorpsDocumentFactory.build()
            raw_data = corps_dto.model_dump()
            if external_id is None:
                external_id = f"corps_{corps_dto.identifiant}"
        elif document_type == DocumentType.CONCOURS:
            concours_dto = ConcoursRowFactory.build()
            raw_data = concours_dto.model_dump()
            if external_id is None:
                external_id = f"concours_{concours_dto.nor}"
        else:
            if external_id is None:
                timestamp = timezone.now().timestamp()
                external_id = f"test_{document_type.value.lower()}_{timestamp}"
            raw_data = {
                "id": external_id,
                "name": f"Test {document_type.value}",
                "description": f"Test document of type {document_type.value}",
            }

        return raw_data, external_id

    @staticmethod
    def create_entity(
        external_id: Optional[str] = None,
        document_type: DocumentType = DocumentType.OFFERS,
        raw_data: Optional[Dict[str, Any]] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        processing: bool = False,
        processed_at: Optional[datetime] = None,
    ) -> Document:
        if raw_data is None:
            raw_data, external_id = DocumentFactory._generate_raw_data_and_external_id(
                document_type, external_id
            )

        if external_id is None:
            timestamp = timezone.now().timestamp()
            external_id = f"test_{document_type.value.lower()}_{timestamp}"

        if processed_at:
            processed_at = as_aware(processed_at)

        return Document(
            external_id=external_id,
            raw_data=raw_data,
            type=document_type,
            created_at=timezone.now(),
            processing=processing,
            processed_at=processed_at,
        )

    @staticmethod
    def create_entity_batch(
        count: int,
        document_type: DocumentType = DocumentType.OFFERS,
        **kwargs,
    ) -> list[Document]:
        documents = []
        for _ in range(count):
            doc = DocumentFactory.create_entity(
                document_type=document_type,
                **kwargs,
            )
            documents.append(doc)

        return documents
