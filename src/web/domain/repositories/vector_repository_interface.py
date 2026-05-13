from typing import Dict, List, Optional, Protocol, TypedDict
from uuid import UUID

from domain.entities.document import DocumentType
from domain.entities.vectorized_document import VectorizedDocument
from domain.repositories.document_repository_interface import IUpsertResult

# Import the filter types
from domain.value_objects.category import Category
from domain.value_objects.localisation import Localisation
from domain.value_objects.opportunity_type import OpportunityType
from domain.value_objects.similarity_type import SimilarityResult, SimilarityType
from domain.value_objects.verse import Verse

IFilters = Dict[str, List[Localisation | OpportunityType | Verse | Category]]


class IDeleteError(TypedDict):
    entity_id: UUID
    error: str
    exception: Exception


class IDeleteResult(TypedDict):
    deleted: int
    errors: List[IDeleteError]


class IVectorRepository(Protocol):
    def semantic_search(
        self,
        query_embedding: List[float],
        limit: int = 10,
        filters: Optional[IFilters] = None,
        similarity_type: Optional[SimilarityType] = None,
    ) -> List[SimilarityResult]: ...

    def upsert_batch(
        self,
        vectorized_documents: List[VectorizedDocument],
        document_type: DocumentType,
    ) -> IUpsertResult: ...

    def delete_vectorized_documents(self, list_ids: List[UUID]) -> IDeleteResult: ...
