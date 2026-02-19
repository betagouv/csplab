"""PgVector repository implementation for vector operations."""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from django.db.models import Q
from pgvector.django import CosineDistance

from domain.entities.vectorized_document import VectorizedDocument
from domain.repositories.vector_repository_interface import IVectorRepository
from domain.value_objects.similarity_type import (
    SimilarityMetric,
    SimilarityResult,
    SimilarityType,
)
from infrastructure.django_apps.shared.models import vectorized_document


class PgVectorRepository(IVectorRepository):
    """Repository for vector operations using PostgreSQL with pgvector extension."""

    def store_embedding(self, vectorized_doc: VectorizedDocument) -> VectorizedDocument:
        """Store a vectorized document with its embedding."""
        model = vectorized_document.VectorizedDocumentModel.from_entity(vectorized_doc)

        existing = vectorized_document.VectorizedDocumentModel.objects.filter(
            entity_id=vectorized_doc.entity_id, document_type=model.document_type
        ).first()

        if existing:
            existing.content = model.content
            existing.embedding = model.embedding
            existing.metadata = model.metadata
            existing.updated_at = datetime.now(timezone.utc)
            existing.save()
            return existing.to_entity()
        else:
            # Create new record
            model.save()
            return model.to_entity()

    def semantic_search(
        self,
        query_embedding: List[float],
        limit: int = 10,
        filters: Optional[Dict[str, Any]] = None,
        similarity_type: Optional[SimilarityType] = None,
    ) -> List[SimilarityResult]:
        """Search for documents semantically similar to the query embedding."""
        if similarity_type is None:
            similarity_type = SimilarityType()

        ## TODO : filter queryset if document_type is given
        queryset = vectorized_document.VectorizedDocumentModel.objects.all()

        if filters:
            for key, value in filters.items():
                # Check if it's a direct model field (like document_type)
                if hasattr(vectorized_document.VectorizedDocumentModel, key):
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
