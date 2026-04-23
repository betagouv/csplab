from dependency_injector import containers, providers

from application.candidate.usecases.initialize_cv_metadata import (
    InitializeCVMetadataUsecase,
)
from application.candidate.usecases.match_cv_to_opportunities import (
    MatchCVToOpportunitiesUsecase,
)
from application.candidate.usecases.process_uploaded_cv import ProcessUploadedCVUsecase
from infrastructure.external_gateways.albert_text_formatter import AlbertTextFormatter
from infrastructure.external_gateways.ocr_extractor import OCRExtractor
from infrastructure.gateways.candidate.query_builder import QueryBuilder
from infrastructure.gateways.shared.async_http_client import AsyncHttpClient
from infrastructure.repositories.candidate.async_postgres_cv_metadata_repository import (  # noqa E501
    AsyncPostgresCVMetadataRepository,
)
from infrastructure.repositories.candidate.postgres_cv_metadata_repository import (
    PostgresCVMetadataRepository,
)


class CandidateContainer(containers.DeclarativeContainer):
    app_config: providers.Dependency = providers.Dependency()
    logger_service: providers.Dependency = providers.Dependency()

    shared_container = providers.DependenciesContainer()

    corps_repository = shared_container.corps_repository
    concours_repository = shared_container.concours_repository
    offers_repository = shared_container.offers_repository
    embedding_generator = shared_container.embedding_generator
    vector_repository = shared_container.vector_repository

    # HTTP client for async operations
    async_http_client = providers.Factory(AsyncHttpClient)

    ocr_text_extractor = providers.Factory(
        OCRExtractor,
        config=providers.Callable(lambda cfg: cfg.ocr, app_config),
        http_client=async_http_client,
    )
    pdf_text_extractor = providers.Factory(
        AlbertTextFormatter,
        config=providers.Callable(lambda cfg: cfg.albert, app_config),
        http_client=async_http_client,
    )

    query_builder = providers.Factory(QueryBuilder)
    async_cv_metadata_repository = providers.Singleton(
        AsyncPostgresCVMetadataRepository
    )
    postgres_cv_metadata_repository = providers.Singleton(PostgresCVMetadataRepository)

    initialize_cv_metadata_usecase = providers.Factory(
        InitializeCVMetadataUsecase,
        cv_metadata_repository=postgres_cv_metadata_repository,
    )

    process_uploaded_cv_usecase = providers.Factory(
        ProcessUploadedCVUsecase,
        ocr=ocr_text_extractor,
        text_formatter=pdf_text_extractor,
        query_builder=query_builder,
        async_cv_metadata_repository=async_cv_metadata_repository,
        logger=logger_service,
    )

    match_cv_to_opportunities_usecase = providers.Factory(
        MatchCVToOpportunitiesUsecase,
        postgres_cv_metadata_repository=postgres_cv_metadata_repository,
        embedding_generator=embedding_generator,
        vector_repository=vector_repository,
        concours_repository=concours_repository,
        offers_repository=offers_repository,
        logger=logger_service,
    )
