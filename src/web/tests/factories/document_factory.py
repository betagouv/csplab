from datetime import datetime
from typing import Any, Dict, Optional

from django.utils import timezone

from domain.ingestion.entities.document import Document, DocumentType
from infrastructure.django_apps.ingestion.models.raw_document import RawDocument
from tests.factories.concours_row_factory import ConcoursRowFactory
from tests.factories.ingres_corps_factories import IngresCorpsDocumentFactory
from tests.factories.ingres_metiers_factories import IngresMetiersDocumentFactory
from tests.factories.talentsoft_factories import TalentsoftDetailOfferFactory


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
        elif document_type == DocumentType.OFFERS:
            offer_dto = TalentsoftDetailOfferFactory.build()
            raw_data = offer_dto.model_dump()
            if external_id is None:
                salary_range_code = (
                    raw_data["salaryRange"]["clientCode"]
                    if raw_data.get("salaryRange")
                    else "UNK"
                )
                external_id = f"{salary_range_code}-{raw_data['reference']}"
        elif document_type == DocumentType.CONCOURS:
            concours_dto = ConcoursRowFactory.build()
            raw_data = concours_dto.model_dump()
            if external_id is None:
                external_id = f"concours_{concours_dto.nor}"
        else:
            if external_id is None:
                timestamp = datetime.now().timestamp()
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
            timestamp = datetime.now().timestamp()
            external_id = f"test_{document_type.value.lower()}_{timestamp}"

        if processed_at:
            processed_at = timezone.make_aware(processed_at)

        return Document(
            external_id=external_id,
            raw_data=raw_data,
            type=document_type,
            created_at=timezone.make_aware(datetime.now()),
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

    @staticmethod
    def create_model(
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
    def create_model_batch(
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

            doc = DocumentFactory.create_model(
                external_id=external_id,
                document_type=document_type,
                raw_data=raw_data,
            )
            documents.append(doc)

        return documents
