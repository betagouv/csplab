from typing import List, Optional
from uuid import UUID

from referentiel.types import IUpsertResult

from domain.ingestion.entities.document import DocumentType
from domain.ingestion.entities.vectorized_document import VectorizedDocument
from domain.ingestion.repositories.vector_repository_interface import (
    IDeleteResult,
    IFilters,
    IVectorRepository,
)
from domain.ingestion.value_objects.similarity_type import (
    SimilarityResult,
    SimilarityType,
)


class NullVectorRepository(IVectorRepository):
    def semantic_search(
        self,
        query_embedding: List[float],
        limit: int = 10,
        filters: Optional[IFilters] = None,
        similarity_type: Optional[SimilarityType] = None,
    ) -> List[SimilarityResult]:
        return []

    def upsert_batch(
        self,
        vectorized_documents: List[VectorizedDocument],
        document_type: DocumentType,
    ) -> IUpsertResult:
        return {"created": 0, "updated": 0, "errors": []}

    def delete_vectorized_documents(self, list_ids: List[UUID]) -> IDeleteResult:
        return {"deleted": 0, "errors": []}
