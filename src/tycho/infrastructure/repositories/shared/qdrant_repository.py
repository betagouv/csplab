from typing import Any, Dict, List, Optional, cast
from uuid import UUID

from qdrant_client import QdrantClient
from qdrant_client.http.exceptions import UnexpectedResponse
from qdrant_client.http.models import (
    FieldCondition,
    Filter,
    MatchValue,
    PointStruct,
    SparseVector,
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
    def __init__(self, config: QdrantConfig, logger: ILogger):
        self.config = config
        self.logger = logger
        self.client = QdrantClient(
            url=config.url,
            api_key=config.api_key if config.api_key else None,
            timeout=config.timeout,
            prefer_grpc=config.prefer_grpc,
        )
        self.collection_name = "fonction-publique"

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
                using="semantic",
                query_filter=qdrant_filter,
                limit=limit,
                # score_threshold=0.7,
            )

            results = []
            for point in query_response.points:
                payload = point.payload or {}

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

    def store_embedding(self, vectorized_doc: VectorizedDocument) -> VectorizedDocument:
        """Store a single vectorized document."""
        try:
            payload = {
                "content": vectorized_doc.content,
                "document_type": vectorized_doc.document_type.value,
                **vectorized_doc.metadata,  # Flatten metadata for easier filtering
            }

            point = PointStruct(
                id=str(vectorized_doc.entity_id),
                vector={
                    "semantic": vectorized_doc.embedding,
                    "keywords": SparseVector(indices=[], values=[]),
                },
                payload=payload,
            )

            self.client.upsert(
                collection_name=self.collection_name,
                points=[point],
            )

            return vectorized_doc

        except UnexpectedResponse as e:
            self.logger.error(f"Qdrant API error during store: {str(e)}")
            raise ExternalApiError(f"Vector store failed: {str(e)}") from e
        except Exception as e:
            self.logger.error(f"Unexpected error during store: {str(e)}")
            raise ExternalApiError(f"Vector store failed: {str(e)}") from e

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
                    vector={
                        "semantic": doc.embedding,
                        "keywords": SparseVector(indices=[], values=[]),
                    },
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

        except UnexpectedResponse as e:
            self.logger.error(f"Qdrant API error during upsert: {str(e)}")
            return {
                "created": 0,
                "updated": 0,
                "errors": [
                    {
                        "entity_id": None,
                        "error": f"Qdrant upsert failed: {str(e)}",
                        "exception": ExternalApiError(str(e)),
                    }
                ],
            }
        except Exception as e:
            self.logger.error(f"Unexpected error during upsert: {str(e)}")
            return {
                "created": 0,
                "updated": 0,
                "errors": [
                    {
                        "entity_id": None,
                        "error": f"Upsert failed: {str(e)}",
                        "exception": ExternalApiError(str(e)),
                    }
                ],
            }

    def _build_filter(self, filters: Optional[Dict[str, Any]]) -> Optional[Filter]:
        if not filters:
            return None

        must_conditions = []
        for key, value in filters.items():
            if isinstance(value, list):
                for item in value:
                    must_conditions.append(
                        FieldCondition(key=key, match=MatchValue(value=item))
                    )
            else:
                must_conditions.append(
                    FieldCondition(key=key, match=MatchValue(value=value))
                )
        return Filter(must=cast(list, must_conditions)) if must_conditions else None
