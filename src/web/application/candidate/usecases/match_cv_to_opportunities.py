from typing import List, Optional, Tuple

from asgiref.sync import async_to_sync
from ddd.services.logger_interface import ILogger
from ddd.usecase_interface import IUseCase
from referentiel.entities.concours import Concours
from referentiel.entities.metier import Metier
from referentiel.entities.offer import Offer
from referentiel.repositories.concours_repository_interface import IConcoursRepository
from referentiel.repositories.metier_repository_interface import IMetierRepository
from referentiel.repositories.offers_repository_interface import IOffersRepository

from domain.candidate.entities.cv_metadata import CVMetadata
from domain.candidate.exceptions.cv_errors import CVProcessingFailedError
from domain.candidate.repositories.cv_metadata_repository_interface import (
    ICVMetadataRepository,
)
from domain.candidate.value_objects.cv_processing_status import CVStatus
from domain.ingestion.entities.document import DocumentType
from domain.ingestion.repositories.vector_repository_interface import (
    IFilters,
    IVectorRepository,
)
from domain.ingestion.services.embedding_generator_interface import IEmbeddingGenerator


class MatchCVToOpportunitiesUsecase(
    IUseCase[CVMetadata, List[Tuple[Concours | Tuple[Offer, list[Metier]], float]]],
):
    def __init__(
        self,
        cv_metadata_repository: ICVMetadataRepository,
        embedding_generator: IEmbeddingGenerator,
        vector_repository: IVectorRepository,
        concours_repository: IConcoursRepository,
        offers_repository: IOffersRepository,
        metiers_repository: IMetierRepository,
        logger: ILogger,
    ):
        self.cv_metadata_repository = cv_metadata_repository
        self.embedding_generator = embedding_generator
        self.vector_repository = vector_repository
        self.concours_repository = concours_repository
        self.offers_repository = offers_repository
        self.metiers_repository = metiers_repository
        self.logger = logger

    def execute(
        self,
        cv_metadata: CVMetadata,
        filters: Optional[IFilters] | None = None,
        limit: int = 5,
    ) -> List[Tuple[Concours | Tuple[Offer, list[Metier]], float]]:
        self.logger.info(
            "Starting opportunity matching for cv_uuid='%s', limit=%d",
            cv_metadata.entity_id,
            limit,
        )

        if cv_metadata.status == CVStatus.FAILED or not cv_metadata.search_query:
            raise CVProcessingFailedError(
                str(cv_metadata.entity_id), "CV processing failed"
            )

        query_embedding = async_to_sync(self.embedding_generator.generate_embedding)(
            cv_metadata.search_query
        )

        similarity_results = self.vector_repository.semantic_search(
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

        opportunities: List[Tuple[Concours | Tuple[Offer, list[Metier]], float]] = []

        concours_ids = [
            result.document.entity_id for result in concours_similarity_results
        ]
        concours_list = self.concours_repository.get_by_ids(concours_ids)
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
        offers_list = self.offers_repository.get_by_ids(offers_ids)
        offers_scores_by_id = {
            result.document.entity_id: result.score
            for result in offers_similarity_results
        }
        for offer in offers_list:
            metiers = self.metiers_repository.get_for_offer(offer)
            opportunities.append(((offer, metiers), offers_scores_by_id[offer.id]))

        self.logger.info("Returning %d opportunities", len(opportunities))

        sorted_opportunities = sorted(opportunities, key=lambda x: x[1], reverse=True)
        return sorted_opportunities
