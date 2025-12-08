"""Vector repository interface for semantic search operations."""

from typing import Any, Dict, List, Optional, Protocol

from core.entities.vectorized_document import VectorizedDocument
from core.value_objects.similarity_type import SimilarityResult, SimilarityType


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

    # def similarity_search(
    #     self,
    #     document_id: int,
    #     threshold: float = 0.8,
    #     limit: int = 10,
    #     similarity_type: Optional[SimilarityType] = None,
    # ) -> List[VectorizedDocument]:
    #     """Find documents similar to a specific document."""
    #     ...
