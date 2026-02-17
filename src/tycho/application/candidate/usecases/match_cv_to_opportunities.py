"""Use case for matching opportunities (concours) to CV based on semantic similarity."""

from typing import List, Tuple

from domain.entities.concours import Concours
from domain.entities.cv_metadata import CVMetadata
from domain.entities.document import DocumentType
from domain.entities.offer import Offer
from domain.exceptions.cv_errors import CVProcessingFailedError
from domain.repositories.concours_repository_interface import IConcoursRepository
from domain.repositories.cv_metadata_repository_interface import ICVMetadataRepository
from domain.repositories.offers_repository_interface import IOffersRepository
from domain.repositories.vector_repository_interface import IVectorRepository
from domain.services.embedding_generator_interface import IEmbeddingGenerator
from domain.services.logger_interface import ILogger
from domain.value_objects.cv_processing_status import CVStatus


class MatchCVToOpportunitiesUsecase:
    """Usecase for matching opportunities to CV based on semantic similarity."""

    def __init__(  # noqa: PLR0913
        self,
        postgres_cv_metadata_repository: ICVMetadataRepository,
        embedding_generator: IEmbeddingGenerator,
        vector_repository: IVectorRepository,
        concours_repository: IConcoursRepository,
        offers_repository: IOffersRepository,
        logger: ILogger,
    ):
        """Initialize the use case with required dependencies."""
        self._postgres_cv_metadata_repository = postgres_cv_metadata_repository
        self._embedding_generator = embedding_generator
        self._vector_repository = vector_repository
        self._concours_repository = concours_repository
        self._offers_repository = offers_repository
        self._logger = logger

    def execute(
        self,
        cv_metadata: CVMetadata,
        limit: int = 5,
    ) -> List[Tuple[Concours | Offer, float]]:
        """Execute the matching of opportunities to CV based on semantic similarity."""
        self._logger.info(
            f"Starting opportunity matching for cv_uuid='{cv_metadata.id}',"
            f"limit={limit}"
        )

        if cv_metadata.status == CVStatus.FAILED or not cv_metadata.search_query:
            raise CVProcessingFailedError(str(cv_metadata.id), "CV processing failed")

        query_embedding = self._embedding_generator.generate_embedding(
            cv_metadata.search_query
        )

        concours_similarity_results = self._vector_repository.semantic_search(
            query_embedding=query_embedding,
            limit=limit,
            filters={"document_type": DocumentType.CONCOURS.value},
        )
        offers_similarity_results = self._vector_repository.semantic_search(
            query_embedding=query_embedding,
            limit=limit,
            filters={"document_type": DocumentType.OFFERS.value},
        )

        opportunities: List[Tuple[Concours | Offer, float]] = []

        for result in concours_similarity_results:
            self._logger.info(
                f"Searching for concours with ID: {result.document.entity_id}"
            )
            concours = self._concours_repository.find_by_id(result.document.entity_id)
            self._logger.info(f"Found concours with ID: {concours.id}")
            opportunities.append((concours, result.score))

        for result in offers_similarity_results:
            self._logger.info(
                f"Searching for offer with ID: {result.document.entity_id}"
            )
            offer = self._offers_repository.find_by_id(result.document.entity_id)
            self._logger.info(f"Found offer with ID: {offer.id}")
            opportunities.append((offer, result.score))

        self._logger.info(f"Returning {len(opportunities)} opportunities")

        sorted_opportunities = sorted(opportunities, key=lambda x: x[1], reverse=True)
        return sorted_opportunities[:limit]
