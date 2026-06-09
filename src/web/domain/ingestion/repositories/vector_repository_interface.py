from typing import Dict, List, Optional, Protocol, TypedDict
from uuid import UUID

from referentiel.types import IUpsertResult

# Import the filter types
from referentiel.value_objects.category import Category
from referentiel.value_objects.localisation import Localisation
from referentiel.value_objects.verse import Verse

from domain.candidate.value_objects.opportunity_type import OpportunityType
from domain.ingestion.entities.document import DocumentType
from domain.ingestion.entities.vectorized_document import VectorizedDocument
from domain.ingestion.value_objects.similarity_type import (
    SimilarityResult,
    SimilarityType,
)

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
