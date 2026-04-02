from datetime import datetime
from typing import Dict, List, Tuple

from django.db import DatabaseError, transaction
from django.db.models import F, Q
from django.utils import timezone

from domain.entities.document import Document, DocumentType
from domain.repositories.document_repository_interface import (
    IDocumentRepository,
    IUpsertResult,
)
from infrastructure.django_apps.ingestion.models.raw_document import RawDocument


class PostgresDocumentRepository(IDocumentRepository):
    def find_by_type(
        self, document_type: DocumentType, start: int, batch_size: int = 1000
    ) -> Tuple[List[Document], bool]:
        offset = start * batch_size

        if start < 0 or batch_size <= 0:
            raise ValueError("Invalid start or batch_size values")

        qs = RawDocument.objects.filter(document_type=document_type.value)
        raw_documents_to_return = list(
            qs.order_by("created_at")[offset : offset + batch_size]
        )
        has_more = qs.count() > offset + batch_size

        return [raw_doc.to_entity() for raw_doc in raw_documents_to_return], has_more

    def find_by_external_ids(
        self, document_type: DocumentType, documents: List[Document]
    ) -> List[Document]:
        external_ids = [doc.external_id for doc in documents]
        qs = RawDocument.objects.filter(
            document_type=document_type.value, external_id__in=external_ids
        )
        return [raw_doc.to_entity() for raw_doc in qs]

    def get_documents_to_upsert(
        self,
        document_type: DocumentType,
        fetched_documents: List[Document],
        existing_documents: List[Document],
    ) -> List[Document]:
        fetched_documents_map = {doc.external_id: doc for doc in fetched_documents}
        fetched_document_external_ids = set(fetched_documents_map.keys())

        existing_documents_map = {doc.external_id: doc for doc in existing_documents}
        existing_document_external_ids = set(existing_documents_map.keys())

        # new documents
        new_document_external_ids = (
            fetched_document_external_ids - existing_document_external_ids
        )
        new_documents = [
            fetched_documents_map[ext_id] for ext_id in new_document_external_ids
        ]

        # updated documents
        updated_documents = []
        for ext_id in existing_document_external_ids:
            fetched = fetched_documents_map[ext_id]
            stored = existing_documents_map[ext_id]
            if (
                "modificationDate" not in fetched.raw_data
                or fetched.raw_data["modificationDate"]
                > stored.raw_data["modificationDate"]
            ):
                updated_documents.append(fetched_documents_map[ext_id])

        return new_documents + updated_documents

    def upsert_batch(
        self, documents: List[Document], document_type: DocumentType
    ) -> IUpsertResult:
        if not documents:
            return {"created": 0, "updated": 0, "errors": []}

        try:
            with transaction.atomic():
                existing_documents = list(
                    RawDocument.objects.filter(
                        external_id__in=[doc.external_id for doc in documents]
                    ).select_for_update(of=("self",))
                )

                existing_documents_map = {
                    obj.external_id: obj for obj in existing_documents
                }
                existing_external_ids = set(existing_documents_map.keys())

                partitioned: Dict[str, List[Document]] = {"new": [], "existing": []}
                for doc in documents:
                    if doc.external_id in existing_external_ids:
                        partitioned["existing"].append(doc)
                    else:
                        partitioned["new"].append(doc)

                created = 0
                updated = 0

                if partitioned["new"]:
                    new_documents = [
                        RawDocument.from_entity(doc) for doc in partitioned["new"]
                    ]
                    RawDocument.objects.bulk_create(
                        new_documents, ignore_conflicts=True
                    )
                    created = len(new_documents)

                if partitioned["existing"]:
                    obj_to_update = []
                    for doc in partitioned["existing"]:
                        existing_obj = existing_documents_map[doc.external_id]
                        updated_obj = RawDocument.from_entity(doc)
                        updated_obj.id = existing_obj.id
                        updated_obj.raw_data = doc.raw_data
                        updated_obj.updated_at = timezone.make_aware(datetime.now())
                        obj_to_update.append(updated_obj)

                    updated = RawDocument.objects.bulk_update(
                        obj_to_update,
                        fields=[
                            "document_type",
                            "raw_data",
                            "updated_at",
                        ],
                    )

            return {"created": created, "updated": updated, "errors": []}

        except Exception:
            db_error = DatabaseError("Erreur lors de l'upsert batch des documents")
            return {
                "created": 0,
                "updated": 0,
                "errors": [
                    {
                        "entity_id": None,
                        "error": "Database error during bulk upsert",
                        "exception": db_error,
                    }
                ],
            }

    @transaction.atomic
    def get_pending_processing(
        self,
        document_type: DocumentType,
        limit: int = 1000,
    ) -> List[Document]:
        qs = (
            RawDocument.objects.filter(processing=False, document_type=document_type)
            .filter(Q(processed_at__isnull=True) | Q(updated_at__gt=F("processed_at")))
            .select_for_update(of=("self",), skip_locked=True)[:limit]
        )

        for obj in qs:
            obj.processing = True
        try:
            RawDocument.objects.bulk_update(qs, ["processing"])
        except Exception as e:
            raise DatabaseError(f"Database error during update: {str(e)}") from e

        return [model.to_entity() for model in qs]

    def mark_as_processed(self, raw_documents: List[Document]) -> int:
        try:
            return RawDocument.objects.filter(
                id__in=[obj.id for obj in raw_documents]
            ).update(processed_at=timezone.now(), processing=False)
        except Exception as e:
            raise DatabaseError(f"Database error during update: {str(e)}") from e

    def mark_as_pending(self, raw_documents: List[Document]) -> int:
        try:
            return RawDocument.objects.filter(
                id__in=[obj.id for obj in raw_documents]
            ).update(processing=False)
        except Exception as e:
            raise DatabaseError(f"Database error during update: {str(e)}") from e
