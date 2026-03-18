from typing import Any, Dict, List, Optional, cast
from uuid import UUID

from qdrant_client import QdrantClient
from qdrant_client.http.exceptions import UnexpectedResponse
from qdrant_client.http.models import (
    FieldCondition,
    Filter,
    MatchValue,
    PointStruct,
)

from config.app_config import QdrantConfig
from domain.entities.document import DocumentType
from domain.entities.vectorized_document import VectorizedDocument
from domain.repositories.vector_repository_interface import IVectorRepository
from domain.services.logger_interface import ILogger
from domain.value_objects.similarity_type import (
    SimilarityMetric,
    SimilarityResult,
    SimilarityType,
)
from infrastructure.exceptions.exceptions import ExternalApiError


class QdrantRepository(IVectorRepository):
    def __init__(
        self,
        config: QdrantConfig,
        logger: ILogger,
        collection_name: str = "fonction_publique",
    ):
        self.config = config
        self.logger = logger
        self.collection_name = collection_name
        self.client = QdrantClient(
            url=config.url,
            api_key=config.api_key if config.api_key else None,
            timeout=config.timeout,
            prefer_grpc=config.prefer_grpc,
        )

    def semantic_search(
        self,
        query_embedding: List[float],
        limit: int = 10,
        filters: Optional[Dict[str, Any]] = None,
        similarity_type: Optional[SimilarityType] = None,
    ) -> List[SimilarityResult]:
        if similarity_type is None:
            similarity_type = SimilarityType()

        if similarity_type.metric != SimilarityMetric.COSINE:
            raise NotImplementedError(
                f"Similarity metric {similarity_type.metric} not implemented"
            )

        try:
            qdrant_filter = self._build_filter(filters)

            query_response = self.client.query_points(
                collection_name=self.collection_name,
                query=query_embedding,
                query_filter=qdrant_filter,
                limit=limit,
                # score_threshold=0.7,
            )

            results = []
            for point in query_response.points:
                payload = point.payload or {}

                # default value OFFERS if document_type is missing
                doc_type_str = payload.get("document_type", DocumentType.OFFERS.value)
                doc_type = DocumentType(doc_type_str)

                entity_id = UUID(str(point.id))

                metadata = {
                    k: v
                    for k, v in payload.items()
                    if k not in ["content", "document_type"]
                }

                vectorized_doc = VectorizedDocument(
                    entity_id=entity_id,
                    document_type=doc_type,
                    content=payload.get("content", ""),
                    embedding=query_embedding,
                    metadata=metadata,
                )

                similarity_result = SimilarityResult(
                    document=vectorized_doc,
                    score=float(point.score),
                )
                results.append(similarity_result)
            return results

        except UnexpectedResponse as e:
            self.logger.error(f"Qdrant API error during search: {str(e)}")
            raise ExternalApiError(f"Vector search failed: {str(e)}") from e
        except Exception as e:
            self.logger.error(f"Unexpected error during search: {str(e)}")
            raise ExternalApiError(f"Vector search failed: {str(e)}") from e

    def upsert_batch(
        self,
        vectorized_documents: List[VectorizedDocument],
        document_type: DocumentType,
    ):
        if not vectorized_documents:
            return {"created": 0, "updated": 0, "errors": []}

        try:
            points = []
            for doc in vectorized_documents:
                payload = {
                    "content": doc.content,
                    "document_type": document_type.value,
                    **doc.metadata,
                }

                point = PointStruct(
                    id=str(doc.entity_id),
                    vector=doc.embedding,  # Use simple vector
                    payload=payload,
                )
                points.append(point)

            # Perform upsert
            self.client.upsert(
                collection_name=self.collection_name,
                points=points,
            )

            # Qdrant upsert is always successful if no exception
            return {
                "created": len(vectorized_documents),
                "updated": 0,
                "errors": [],
            }
        except Exception as e:
            self.logger.error(f"Unexpected error during upsert: {str(e)}")
            raise ExternalApiError(str(e)) from e

    def _build_filter(self, filters: Optional[Dict[str, Any]]) -> Optional[Filter]:
        # - `must=[]` : conditions AND
        # - `should=[]` : conditions OR
        # - `must_not=[]` : conditions NOT
        if not filters:
            return None

        must_conditions = []
        for key, value in filters.items():
            if isinstance(value, list):
                # For a list: create an OR condition
                should_conditions = [
                    FieldCondition(key=key, match=MatchValue(value=item))
                    for item in value
                ]
                must_conditions.append(Filter(should=cast(list, should_conditions)))
            else:
                must_conditions.append(
                    Filter(
                        must=[FieldCondition(key=key, match=MatchValue(value=value))]
                    )
                )
        return Filter(must=cast(list, must_conditions)) if must_conditions else None
