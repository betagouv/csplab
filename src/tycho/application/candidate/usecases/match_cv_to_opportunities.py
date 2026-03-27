from typing import List, Optional, Tuple

from domain.entities.concours import Concours
from domain.entities.cv_metadata import CVMetadata
from domain.entities.document import DocumentType
from domain.entities.offer import Offer
from domain.exceptions.cv_errors import CVProcessingFailedError
from domain.interfaces.usecase_interface import IUseCase
from domain.repositories.concours_repository_interface import IConcoursRepository
from domain.repositories.cv_metadata_repository_interface import ICVMetadataRepository
from domain.repositories.offers_repository_interface import IOffersRepository
from domain.repositories.vector_repository_interface import IFilters, IVectorRepository
from domain.services.embedding_generator_interface import IEmbeddingGenerator
from domain.services.logger_interface import ILogger
from domain.value_objects.cv_processing_status import CVStatus


class MatchCVToOpportunitiesUsecase(
    IUseCase[CVMetadata, List[Tuple[Concours | Offer, float]]],
):
    def __init__(  # noqa: PLR0913
        self,
        postgres_cv_metadata_repository: ICVMetadataRepository,
        embedding_generator: IEmbeddingGenerator,
        vector_repository: IVectorRepository,
        concours_repository: IConcoursRepository,
        offers_repository: IOffersRepository,
        logger: ILogger,
    ):
        self._postgres_cv_metadata_repository = postgres_cv_metadata_repository
        self._embedding_generator = embedding_generator
        self._vector_repository = vector_repository
        self._concours_repository = concours_repository
        self._offers_repository = offers_repository
        self._logger = logger

    def execute(
        self,
        cv_metadata: CVMetadata,
        filters: Optional[IFilters] | None = None,
        limit: int = 5,
    ) -> List[Tuple[Concours | Offer, float]]:
        self._logger.info(
            f"Starting opportunity matching for cv_uuid='{cv_metadata.id}',"
            f"limit={limit}"
        )

        if cv_metadata.status == CVStatus.FAILED or not cv_metadata.search_query:
            raise CVProcessingFailedError(str(cv_metadata.id), "CV processing failed")

        query_embedding = self._embedding_generator.generate_embedding(
            cv_metadata.search_query
        )

        similarity_results = self._vector_repository.semantic_search(
            query_embedding=query_embedding,
            limit=limit,
            filters=filters,
        )

        concours_similarity_results = [
            result
            for result in similarity_results
            if result.document.document_type == DocumentType.CONCOURS
        ]
        offers_similarity_results = [
            result
            for result in similarity_results
            if result.document.document_type == DocumentType.OFFERS
        ]

        opportunities: List[Tuple[Concours | Offer, float]] = []

        concours_ids = [
            result.document.entity_id for result in concours_similarity_results
        ]
        concours_list = self._concours_repository.find_by_ids(concours_ids)
        concours_scores_by_id = {
            result.document.entity_id: result.score
            for result in concours_similarity_results
        }
        opportunities.extend(
            [
                (concours, concours_scores_by_id[concours.id])
                for concours in concours_list
            ]
        )

        offers_ids = [result.document.entity_id for result in offers_similarity_results]
        offers_list = self._offers_repository.find_by_ids(offers_ids)
        offers_scores_by_id = {
            result.document.entity_id: result.score
            for result in offers_similarity_results
        }
        opportunities.extend(
            [(offer, offers_scores_by_id[offer.id]) for offer in offers_list]
        )

        self._logger.info(f"Returning {len(opportunities)} opportunities")

        sorted_opportunities = sorted(opportunities, key=lambda x: x[1], reverse=True)
        return sorted_opportunities
