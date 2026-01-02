"""PgVector repository implementation for vector operations."""

from datetime import datetime
from typing import Any, Dict, List, Optional

from django.db.models import Q
from pgvector.django import CosineDistance

from apps.shared.models import vectorized_document
from domain.entities.vectorized_document import VectorizedDocument
from domain.repositories.vector_repository_interface import IVectorRepository
from domain.value_objects.similarity_type import (
    SimilarityMetric,
    SimilarityResult,
    SimilarityType,
)


class PgVectorRepository(IVectorRepository):
    """Repository for vector operations using PostgreSQL with pgvector extension."""

    def store_embedding(self, vectorized_doc: VectorizedDocument) -> VectorizedDocument:
        """Store a vectorized document with its embedding."""
        model = vectorized_document.VectorizedDocumentModel.from_entity(vectorized_doc)

        existing = vectorized_document.VectorizedDocumentModel.objects.filter(
            document_id=vectorized_doc.document_id
        ).first()

        if existing:
            existing.content = model.content
            existing.embedding = model.embedding
            existing.metadata = model.metadata
            existing.updated_at = datetime.now()
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

    # def similarity_search(
    #     self,
    #     document_id: int,
    #     threshold: float = 0.8,
    #     limit: int = 10,
    #     similarity_type: Optional[SimilarityType] = None,
    # ) -> List[VectorizedDocument]:
    #     """Find documents similar to a specific document."""
    #     if similarity_type is None:
    #         similarity_type = SimilarityType()

    #     try:
    #         reference_doc = vectorized_document.VectorizedDocumentModel.objects.get(
    #             document_id=document_id
    #         )
    #     except vectorized_document.VectorizedDocumentModel.DoesNotExist:
    #         return []

    #     # Use the reference document's embedding for similarity search
    #     return self.semantic_search(
    #         query_embedding=list(reference_doc.embedding),
    #         limit=limit + 1,  # +1 to exclude the reference document itself
    #         similarity_type=similarity_type,
    #     )[1:]
