from typing import Any, Dict, List, Optional

from django.db import DatabaseError
from django.db.models import Q
from pgvector.django import CosineDistance

from domain.entities.document import DocumentType
from domain.entities.vectorized_document import VectorizedDocument
from domain.repositories.document_repository_interface import IUpsertResult
from domain.repositories.vector_repository_interface import IVectorRepository
from domain.services.logger_interface import ILogger
from domain.value_objects.similarity_type import (
    SimilarityMetric,
    SimilarityResult,
    SimilarityType,
)
from infrastructure.django_apps.shared.models.vectorized_document import (
    VectorizedDocumentModel,
)


class PgVectorRepository(IVectorRepository):
    def __init__(self, logger: ILogger):
        self.logger = logger

    def semantic_search(
        self,
        query_embedding: List[float],
        limit: int = 10,
        filters: Optional[Dict[str, Any]] = None,
        similarity_type: Optional[SimilarityType] = None,
    ) -> List[SimilarityResult]:
        if similarity_type is None:
            similarity_type = SimilarityType()

        queryset = VectorizedDocumentModel.objects.all()

        if filters:
            for key, value in filters.items():
                # Check if it's a direct model field (like document_type)
                if hasattr(VectorizedDocumentModel, key):
                    if isinstance(value, list):
                        queryset = queryset.filter(**{f"{key}__in": value})
                    else:
                        queryset = queryset.filter(**{key: value})
                elif isinstance(value, list):
                    # It's a metadata field with list value
                    queryset = queryset.filter(
                        Q(**{f"metadata__{key}__overlap": value})
                    )
                else:
                    # It's a metadata field with single value
                    queryset = queryset.filter(**{f"metadata__{key}": value})

        if similarity_type.metric == SimilarityMetric.COSINE:
            queryset = queryset.annotate(
                distance=CosineDistance("embedding", query_embedding)
            ).order_by("distance")
        else:
            raise NotImplementedError(
                f"Similarity metric {similarity_type.metric} not implemented"
            )

        results = queryset[:limit]

        return [
            SimilarityResult(
                document=model.to_entity(),
                score=1.0 - model.distance,  # Convert distance to relevance score
            )
            for model in results
        ]

    def upsert_batch(
        self,
        vectorized_documents: List[VectorizedDocument],
        document_type: DocumentType,
    ) -> IUpsertResult:
        try:
            existing_models = list(
                VectorizedDocumentModel.objects.filter(
                    document_type=document_type,
                    entity_id__in=[doc.entity_id for doc in vectorized_documents],
                ).select_for_update(of=("self",))
            )

            existing_models_map = {model.entity_id: model for model in existing_models}
            existing_ids = set(existing_models_map.keys())

            # Partition vectorized docs into new and existing
            partitioned: Dict[str, List[VectorizedDocument]] = {
                "new": [],
                "existing": [],
            }
            for doc in vectorized_documents:
                if doc.entity_id in existing_ids:
                    partitioned["existing"].append(doc)
                else:
                    partitioned["new"].append(doc)

            created = 0
            updated = 0

            if partitioned["new"]:
                new_models = []
                for doc in partitioned["new"]:
                    model = VectorizedDocumentModel.from_entity(doc)
                    new_models.append(model)

                # Use bulk_create with update_fields to get the generated IDs back
                created_models = VectorizedDocumentModel.objects.bulk_create(
                    new_models, ignore_conflicts=True
                )
                created = len(created_models)

            if partitioned["existing"]:
                models_to_update = []
                for doc in partitioned["existing"]:
                    if doc.entity_id in existing_models_map:
                        existing_model = existing_models_map[doc.entity_id]
                        updated_model = VectorizedDocumentModel.from_entity(doc)
                        # Keep the existing PostgreSQL ID and timestamps
                        updated_model.id = existing_model.id
                        updated_model.created_at = existing_model.created_at
                        models_to_update.append(updated_model)

                if models_to_update:
                    updated = VectorizedDocumentModel.objects.bulk_update(
                        models_to_update,
                        fields=[
                            "entity_id",
                            "document_type",
                            "content",
                            "embedding",
                            "metadata",
                        ],
                    )

            return {"created": created, "updated": updated, "errors": []}

        except Exception as e:
            self.logger.error("Database error during bulk upsert: %s", str(e))
            db_error = DatabaseError(
                f"Erreur lors de l'upsert batch des documents vectorisés: {str(e)}"
            )
            return {
                "created": 0,
                "updated": 0,
                "errors": [
                    {
                        "entity_id": None,
                        "error": f"Database error during bulk upsert: {str(e)}",
                        "exception": db_error,
                    }
                ],
            }
