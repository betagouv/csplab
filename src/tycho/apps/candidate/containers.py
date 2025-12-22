"""Candidate dependency injection container."""

from dependency_injector import containers, providers

from apps.candidate.application.usecases.match_cv_to_opportunities import (
    MatchCVToOpportunitiesUsecase,
)
from apps.candidate.application.usecases.process_uploaded_cv import (
    ProcessUploadedCVUsecase,
)
from apps.candidate.application.usecases.retrieve_corps import RetrieveCorpsUsecase
from apps.candidate.infrastructure.adapters.repositories.cv_metadata_repository import (
    PostgresCVMetadataRepository,
)
from apps.candidate.infrastructure.adapters.services.albert_pdf_extractor import (
    AlbertPDFExtractor,
)
from apps.candidate.infrastructure.adapters.services.query_builder import QueryBuilder


class CandidateContainer(containers.DeclarativeContainer):
    """Candidate services container."""

    config: providers.Dependency = providers.Dependency()
    logger_service: providers.Dependency = providers.Dependency()

    shared_container = providers.DependenciesContainer()

    corps_repository = shared_container.corps_repository
    concours_repository = shared_container.concours_repository
    embedding_generator = shared_container.embedding_generator
    vector_repository = shared_container.vector_repository

    pdf_text_extractor = providers.Factory(
        AlbertPDFExtractor,
        config=providers.Callable(lambda cfg: cfg.albert, config),
    )
    query_builder = providers.Factory(QueryBuilder)
    cv_metadata_repository = providers.Singleton(PostgresCVMetadataRepository)

    retrieve_corps_usecase = providers.Factory(
        RetrieveCorpsUsecase,
        vector_repository=vector_repository,
        embedding_generator=embedding_generator,
        corps_repository=corps_repository,
        logger=logger_service,
    )

    process_uploaded_cv_usecase = providers.Factory(
        ProcessUploadedCVUsecase,
        pdf_text_extractor=pdf_text_extractor,
        query_builder=query_builder,
        cv_metadata_repository=cv_metadata_repository,
        logger=logger_service,
    )

    match_cv_to_opportunities_usecase = providers.Factory(
        MatchCVToOpportunitiesUsecase,
        cv_metadata_repository=cv_metadata_repository,
        embedding_generator=embedding_generator,
        vector_repository=vector_repository,
        concours_repository=concours_repository,
        logger=logger_service,
    )
