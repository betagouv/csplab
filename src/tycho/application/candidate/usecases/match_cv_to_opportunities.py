"""Use case for matching opportunities (concours) to CV based on semantic similarity."""

import time
from typing import List, Tuple
from uuid import UUID

from domain.entities.concours import Concours
from domain.entities.cv_metadata import CVMetadata
from domain.entities.document import DocumentType
from domain.exceptions.cv_errors import (
    CVNotFoundError,
    CVProcessingFailedError,
    CVProcessingTimeoutError,
)
from domain.repositories.concours_repository_interface import IConcoursRepository
from domain.repositories.cv_metadata_repository_interface import ICVMetadataRepository
from domain.repositories.vector_repository_interface import IVectorRepository
from domain.services.embedding_generator_interface import IEmbeddingGenerator
from domain.services.logger_interface import ILogger
from domain.value_objects.cv_processing_status import CVStatus


class MatchCVToOpportunitiesUsecase:
    """Usecase for matching opportunities to CV based on semantic similarity."""

    def __init__(
        self,
        postgres_cv_metadata_repository: ICVMetadataRepository,
        embedding_generator: IEmbeddingGenerator,
        vector_repository: IVectorRepository,
        concours_repository: IConcoursRepository,
        logger: ILogger,
    ):
        """Initialize the use case with required dependencies.

        Args:
            postgres_cv_metadata_repository: Repository for CV metadata
            embedding_generator: Service for generating embeddings
            vector_repository: Repository for vector operations
            concours_repository: Repository for Concours entities
            logger: Logger for tracing operations
        """
        self._postgres_cv_metadata_repository = postgres_cv_metadata_repository
        self._embedding_generator = embedding_generator
        self._vector_repository = vector_repository
        self._concours_repository = concours_repository
        self._logger = logger.get_logger(
            "CANDIDATE::APPLICATION::MatchOpportunitiesToCVUsecase::execute"
        )

    def execute(
        self,
        cv_id: str,
        limit: int = 5,
        wait_for_completion: bool = False,
        timeout: int = 40,
    ) -> List[Tuple[Concours, float]]:
        """Execute the matching of opportunities to CV based on semantic similarity.

        Args:
            cv_id: The CV identifier
            limit: Maximum number of results to return
            wait_for_completion: If True, wait for CV processing to complete
            timeout: Maximum time to wait for completion (seconds)

        Returns:
            List of tuples (Concours, relevance_score) ordered by relevance

        Raises:
            CVNotFoundError: If CV metadata is not found
            CVProcessingTimeoutError: If waiting for completion times out
            CVProcessingFailedError: If CV processing failed
        """
        self._logger.info(
            f"Starting opportunity matching for cv_id='{cv_id}', limit={limit}, "
            f"wait_for_completion={wait_for_completion}, timeout={timeout}"
        )

        cv_metadata = self._postgres_cv_metadata_repository.find_by_id(UUID(cv_id))
        if not cv_metadata:
            raise CVNotFoundError(cv_id)

        if wait_for_completion:
            self._wait_for_cv_completion(cv_metadata, timeout)

        # Check if processing failed
        if cv_metadata.status == CVStatus.FAILED or not cv_metadata.search_query:
            raise CVProcessingFailedError(str(cv_metadata.id), "CV processing failed")

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
            self._logger.info(f"Found concours with ID: {concours.id}")
            concours_list.append((concours, result.score))

        self._logger.info(f"Returning {len(concours_list)} concours")
        return concours_list

    def _wait_for_cv_completion(self, cv_metadata: CVMetadata, timeout: int) -> None:
        """Wait for CV processing to complete.

        Args:
            cv_metadata: The CV metadata object
            timeout: Maximum time to wait (seconds)

        Raises:
            CVProcessingTimeoutError: If timeout is reached
            CVProcessingFailedError: If processing failed
        """
        start_time = time.time()
        poll_interval = 3  # Poll every second

        self._logger.info(
            f"Waiting for CV {cv_metadata.id} completion (timeout: {timeout}s)"
        )

        while time.time() - start_time < timeout:
            if cv_metadata.status == CVStatus.COMPLETED:
                self._logger.info(f"CV {cv_metadata.id} processing completed")
                return

            if cv_metadata.status == CVStatus.FAILED:
                raise CVProcessingFailedError(
                    str(cv_metadata.id), "CV processing failed"
                )

            self._logger.debug(
                f"CV {cv_metadata.id} still processing (status: {cv_metadata.status}), "
                f"waiting {poll_interval}s..."
            )
            time.sleep(poll_interval)

        # Timeout reached
        raise CVProcessingTimeoutError(str(cv_metadata.id), timeout)
