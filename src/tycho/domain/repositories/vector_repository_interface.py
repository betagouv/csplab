from typing import Any, Dict, List, Optional, Protocol

from domain.entities.document import DocumentType
from domain.entities.vectorized_document import VectorizedDocument
from domain.repositories.document_repository_interface import IUpsertResult
from domain.value_objects.similarity_type import SimilarityResult, SimilarityType


class IVectorRepository(Protocol):
    def semantic_search(
        self,
        query_embedding: List[float],
        limit: int = 10,
        filters: Optional[Dict[str, Any]] = None,
        similarity_type: Optional[SimilarityType] = None,
    ) -> List[SimilarityResult]: ...

    def upsert_batch(
        self,
        vectorized_documents: List[VectorizedDocument],
        document_type: DocumentType,
    ) -> IUpsertResult: ...

    def delete_by_entity_ids_and_document_type(
        self, entity_ids: List[str], document_type: DocumentType
    ) -> int: ...
