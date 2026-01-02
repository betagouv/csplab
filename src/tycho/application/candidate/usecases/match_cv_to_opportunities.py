"""Use case for matching opportunities (concours) to CV based on semantic similarity."""

from typing import List, Tuple
from uuid import UUID

from domain.entities.concours import Concours
from domain.entities.document import DocumentType
from domain.exceptions.cv_errors import CVNotFoundError
from domain.repositories.concours_repository_interface import IConcoursRepository
from domain.repositories.cv_metadata_repository_interface import ICVMetadataRepository
from domain.repositories.vector_repository_interface import IVectorRepository
from domain.services.embedding_generator_interface import IEmbeddingGenerator
from domain.services.logger_interface import ILogger


class MatchCVToOpportunitiesUsecase:
    """Usecase for matching opportunities to CV based on semantic similarity."""

    def __init__(
        self,
        cv_metadata_repository: ICVMetadataRepository,
        embedding_generator: IEmbeddingGenerator,
        vector_repository: IVectorRepository,
        concours_repository: IConcoursRepository,
        logger: ILogger,
    ):
        """Initialize the use case with required dependencies.

        Args:
            cv_metadata_repository: Repository for CV metadata
            embedding_generator: Service for generating embeddings
            vector_repository: Repository for vector operations
            concours_repository: Repository for Concours entities
            logger: Logger for tracing operations
        """
        self._cv_metadata_repository = cv_metadata_repository
        self._embedding_generator = embedding_generator
        self._vector_repository = vector_repository
        self._concours_repository = concours_repository
        self._logger = logger.get_logger(
            "CANDIDATE::APPLICATION::MatchOpportunitiesToCVUsecase::execute"
        )

    def execute(self, cv_id: str, limit: int = 10) -> List[Tuple[Concours, float]]:
        """Execute the matching of opportunities to CV based on semantic similarity.

        Args:
            cv_id: The CV identifier
            limit: Maximum number of results to return

        Returns:
            List of tuples (Concours, relevance_score) ordered by relevance
        """
        self._logger.info(
            f"Starting opportunity matching for cv_id='{cv_id}', limit={limit}"
        )

        cv_metadata = self._cv_metadata_repository.find_by_id(UUID(cv_id))
        if not cv_metadata:
            raise CVNotFoundError(cv_id)  # should not happen

        query_embedding = self._embedding_generator.generate_embedding(
            cv_metadata.search_query
        )

        similarity_results = self._vector_repository.semantic_search(
            query_embedding=query_embedding,
            limit=limit,
            filters={"document_type": DocumentType.CONCOURS.value},
        )

        concours_list = []
        for result in similarity_results:
            self._logger.info(
                f"Searching for concours with ID: {result.document.document_id}"
            )
            concours = self._concours_repository.find_by_id(result.document.document_id)
            if concours:
                self._logger.info(f"Found concours with ID: {concours.id}")
                concours_list.append((concours, result.score))
            else:
                self._logger.warning(
                    f"Concours with ID {result.document.document_id} not found"
                )

        self._logger.info(f"Returning {len(concours_list)} concours")
        return concours_list
