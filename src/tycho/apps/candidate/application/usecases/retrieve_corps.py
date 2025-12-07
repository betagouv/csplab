"""Use case for retrieving Corps based on semantic similarity."""

from typing import List

from core.entities.corps import Corps
from core.repositories.corps_repository_interface import ICorpsRepository
from core.repositories.vector_repository_interface import IVectorRepository
from core.services.embedding_generator_interface import IEmbeddingGenerator
from core.services.logger_interface import ILogger


class RetrieveCorpsUsecase:
    """Usecase for retrieving Corps entities based on semantic similarity to a query."""

    def __init__(
        self,
        vector_repository: IVectorRepository,
        embedding_generator: IEmbeddingGenerator,
        corps_repository: ICorpsRepository,
        logger: ILogger,
    ):
        """Initialize the use case with required dependencies.

        Args:
            vector_repository: Repository for vector operations
            embedding_generator: Service for generating embeddings
            corps_repository: Repository for Corps entities
            logger: Logger for tracing operations
        """
        self._vector_repository = vector_repository
        self._embedding_generator = embedding_generator
        self._corps_repository = corps_repository
        self._logger = logger

    def execute(self, query: str, limit: int = 10) -> List[Corps]:
        """Execute the retrieval of Corps based on semantic similarity.

        Args:
            query: The search query string
            limit: Maximum number of results to return

        Returns:
            List of Corps entities ordered by relevance
        """
        if not query.strip():
            return []

        query_embedding = self._embedding_generator.generate_embedding(query)
        similarity_results = self._vector_repository.semantic_search(
            query_embedding=query_embedding,
            limit=limit,
            filters={"document_type": "CORPS"},
        )

        corps_list = []
        for result in similarity_results:
            corps = self._corps_repository.find_by_id(result.document.document_id)
            if corps:
                self._logger.info(
                    f"Corps {corps.id} ({corps.label.value}): score={result.score:.4f}"
                )
                corps_list.append(corps)

        return corps_list
