"""Vector repository interface for semantic search operations."""

from typing import Any, Dict, List, Optional, Protocol

from domain.entities.vectorized_document import VectorizedDocument
from domain.value_objects.similarity_type import SimilarityResult, SimilarityType


class IVectorRepository(Protocol):
    """Interface for vector repository operations."""

    def store_embedding(self, vectorized_doc: VectorizedDocument) -> VectorizedDocument:
        """Store a vectorized document with its embedding."""
        ...

    def semantic_search(
        self,
        query_embedding: List[float],
        limit: int = 10,
        filters: Optional[Dict[str, Any]] = None,
        similarity_type: Optional[SimilarityType] = None,
    ) -> List[SimilarityResult]:
        """Search for documents semantically similar to the query embedding."""
        ...
