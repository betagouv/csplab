"""In-memory vector repository implementation for testing."""

import math
from typing import Any, Dict, List, Optional
from uuid import UUID

from domain.entities.vectorized_document import VectorizedDocument
from domain.repositories.vector_repository_interface import IVectorRepository
from domain.value_objects.similarity_type import (
    SimilarityMetric,
    SimilarityResult,
    SimilarityType,
)


class InMemoryVectorRepository(IVectorRepository):
    """In-memory implementation of vector repository for testing."""

    def __init__(self):
        """Initialize with empty storage."""
        self._documents: Dict[UUID, VectorizedDocument] = {}

    def store_embedding(self, vectorized_doc: VectorizedDocument):
        """Store a vectorized document in memory."""
        # Handle upsert based on entity_id
        existing = None
        for doc in self._documents.values():
            if doc.entity_id == vectorized_doc.entity_id:
                existing = doc
                break

        if existing:
            # Update existing record
            updated_doc = VectorizedDocument(
                id=existing.id,
                entity_id=vectorized_doc.entity_id,
                document_type=vectorized_doc.document_type,
                content=vectorized_doc.content,
                embedding=vectorized_doc.embedding,
                metadata=vectorized_doc.metadata,
            )
            self._documents[existing.id] = updated_doc
            return updated_doc
        else:
            # Create new record - VectorizedDocument generates its own UUID
            new_doc = VectorizedDocument(
                entity_id=vectorized_doc.entity_id,
                document_type=vectorized_doc.document_type,
                content=vectorized_doc.content,
                embedding=vectorized_doc.embedding,
                metadata=vectorized_doc.metadata,
            )
            self._documents[new_doc.id] = new_doc
            return new_doc

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

        # Filter documents if provided
        candidates = list(self._documents.values())
        if filters:
            candidates = self._filter_documents(candidates, filters)

        # Calculate similarities
        scored_docs = []
        for doc in candidates:
            if similarity_type.metric == SimilarityMetric.COSINE:
                score = self._cosine_similarity(query_embedding, doc.embedding)
            elif similarity_type.metric == SimilarityMetric.EUCLIDEAN:
                score = self._euclidean_distance(query_embedding, doc.embedding)
            else:
                raise NotImplementedError(
                    f"Similarity metric {similarity_type.metric} not implemented"
                )
            scored_docs.append((score, doc))

        # Sort by similarity score (descending for cosine, ascending for euclidean)
        if similarity_type.metric == SimilarityMetric.COSINE:
            scored_docs.sort(key=lambda x: x[0], reverse=True)
        else:  # EUCLIDEAN
            scored_docs.sort(key=lambda x: x[0])

        # Return top results as SimilarityResult objects
        return [
            SimilarityResult(document=doc, score=score)
            for score, doc in scored_docs[:limit]
        ]

    def similarity_search(
        self,
        entity_id: UUID,
        threshold: float = 0.8,
        limit: int = 10,
        similarity_type: Optional[SimilarityType] = None,
    ) -> List[SimilarityResult]:
        """Find documents similar to a specific entity."""
        if similarity_type is None:
            similarity_type = SimilarityType()

        reference_doc = None
        for doc in self._documents.values():
            if doc.entity_id == entity_id:
                reference_doc = doc
                break

        if not reference_doc:
            return []

        results = self.semantic_search(
            query_embedding=reference_doc.embedding,
            limit=limit + 1,  # +1 to exclude the reference document itself
            similarity_type=similarity_type,
        )

        return [result for result in results if result.document.entity_id != entity_id][
            :limit
        ]

    def _filter_documents(
        self, documents: List[VectorizedDocument], filters: Dict[str, Any]
    ) -> List[VectorizedDocument]:
        """Filter documents by direct fields and metadata criteria."""
        return [doc for doc in documents if self._matches_filters(doc, filters)]

    def _matches_filters(
        self, doc: VectorizedDocument, filters: Dict[str, Any]
    ) -> bool:
        """Check if document matches all filter criteria."""
        for key, value in filters.items():
            if not self._matches_single_filter(doc, key, value):
                return False
        return True

    def _matches_single_filter(
        self, doc: VectorizedDocument, key: str, value: Any
    ) -> bool:
        """Check if document matches a single filter criterion."""
        # Check if it's a direct field of VectorizedDocument
        if hasattr(doc, key):
            return self._matches_direct_field(doc, key, value)

        # It's a metadata field
        if key not in doc.metadata:
            return False

        return self._matches_metadata_field(doc, key, value)

    def _matches_direct_field(
        self, doc: VectorizedDocument, key: str, value: Any
    ) -> bool:
        """Check if document's direct field matches the filter value."""
        doc_value = getattr(doc, key)
        # Handle enum values
        if hasattr(doc_value, "value"):
            doc_value = doc_value.value

        if isinstance(value, list):
            return doc_value in value
        return doc_value == value

    def _matches_metadata_field(
        self, doc: VectorizedDocument, key: str, value: Any
    ) -> bool:
        """Check if document's metadata field matches the filter value."""
        doc_value = doc.metadata[key]

        if isinstance(value, list):
            if isinstance(doc_value, list):
                return any(v in doc_value for v in value)
            return doc_value in value

        return doc_value == value

    def _filter_by_metadata(
        self, documents: List[VectorizedDocument], filters: Dict[str, Any]
    ) -> List[VectorizedDocument]:
        """Filter documents by metadata criteria."""
        filtered = []
        for doc in documents:
            match = True
            for key, value in filters.items():
                if key not in doc.metadata:
                    match = False
                    break

                if isinstance(value, list):
                    doc_value = doc.metadata[key]
                    if isinstance(doc_value, list):
                        if not any(v in doc_value for v in value):
                            match = False
                            break
                    elif doc_value not in value:
                        match = False
                        break
                elif doc.metadata[key] != value:
                    match = False
                    break

            if match:
                filtered.append(doc)

        return filtered

    def _cosine_similarity(self, a: List[float], b: List[float]) -> float:
        """Calculate cosine similarity between two vectors."""
        if len(a) != len(b):
            raise ValueError("Vectors must have the same length")

        dot_product = sum(x * y for x, y in zip(a, b, strict=True))
        norm_a = math.sqrt(sum(x * x for x in a))
        norm_b = math.sqrt(sum(x * x for x in b))

        if norm_a == 0 or norm_b == 0:
            return 0.0

        return dot_product / (norm_a * norm_b)

    def _euclidean_distance(self, a: List[float], b: List[float]) -> float:
        """Calculate Euclidean distance between two vectors."""
        if len(a) != len(b):
            raise ValueError("Vectors must have the same length")

        return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b, strict=True)))
