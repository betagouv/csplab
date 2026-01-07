"""Candidate dependency injection container."""

from dependency_injector import containers, providers

from application.candidate.usecases.match_cv_to_opportunities import (
    MatchCVToOpportunitiesUsecase,
)
from application.candidate.usecases.process_uploaded_cv import ProcessUploadedCVUsecase
from application.candidate.usecases.retrieve_corps import RetrieveCorpsUsecase
from infrastructure.external_gateways.albert_pdf_extractor import AlbertPDFExtractor
from infrastructure.external_gateways.openai_pdf_extractor import OpenAIPDFExtractor
from infrastructure.gateways.candidate.query_builder import QueryBuilder
from infrastructure.repositories.candidate.postgres_cv_metadata_repository import (
    PostgresCVMetadataRepository,
)


class CandidateContainer(containers.DeclarativeContainer):
    """Candidate services container."""

    config: providers.Dependency = providers.Dependency()
    logger_service: providers.Dependency = providers.Dependency()

    shared_container = providers.DependenciesContainer()

    corps_repository = shared_container.corps_repository
    concours_repository = shared_container.concours_repository
    embedding_generator = shared_container.embedding_generator
    vector_repository = shared_container.vector_repository

    pdf_text_extractor = providers.Selector(
        providers.Callable(lambda cfg: cfg.pdf_extractor_type.value, config),
        albert=providers.Factory(
            AlbertPDFExtractor,
            config=providers.Callable(lambda cfg: cfg.albert, config),
        ),
        openai=providers.Factory(
            OpenAIPDFExtractor,
            config=providers.Callable(lambda cfg: cfg.openai, config),
        ),
    )
    query_builder = providers.Factory(QueryBuilder)
    postgres_cv_metadata_repository = providers.Singleton(PostgresCVMetadataRepository)

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
        postgres_cv_metadata_repository=postgres_cv_metadata_repository,
        logger=logger_service,
    )

    match_cv_to_opportunities_usecase = providers.Factory(
        MatchCVToOpportunitiesUsecase,
        postgres_cv_metadata_repository=postgres_cv_metadata_repository,
        embedding_generator=embedding_generator,
        vector_repository=vector_repository,
        concours_repository=concours_repository,
        logger=logger_service,
    )
