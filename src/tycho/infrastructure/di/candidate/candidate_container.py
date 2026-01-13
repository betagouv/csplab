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
from infrastructure.gateways.shared.async_http_client import AsyncHttpClient
from infrastructure.repositories.candidate.postgres_cv_metadata_repository import (
    PostgresCVMetadataRepository,
)


def _create_pdf_extractor(config, http_client):
    """Create PDF extractor based on configuration using a more readable approach."""
    extractors = {
        "albert": lambda cfg: AlbertPDFExtractor(
            config=cfg.albert, http_client=http_client
        ),
        "openai": lambda cfg: OpenAIPDFExtractor(config=cfg.openai),
    }
    return extractors[config.pdf_extractor_type.value](config)


class CandidateContainer(containers.DeclarativeContainer):
    """Candidate services container."""

    config: providers.Dependency = providers.Dependency()
    logger_service: providers.Dependency = providers.Dependency()

    shared_container = providers.DependenciesContainer()

    corps_repository = shared_container.corps_repository
    concours_repository = shared_container.concours_repository
    embedding_generator = shared_container.embedding_generator
    vector_repository = shared_container.vector_repository

    # HTTP client for async operations
    async_http_client = providers.Factory(AsyncHttpClient)

    pdf_text_extractor = providers.Callable(
        lambda cfg, http_client: _create_pdf_extractor(cfg, http_client),
        config,
        async_http_client,
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
