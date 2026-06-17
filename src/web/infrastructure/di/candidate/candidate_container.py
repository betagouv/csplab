from dependency_injector import containers, providers

from application.candidate.usecases.get_opportunity_details import (
    GetOpportunityDetailsUsecase,
)
from application.candidate.usecases.initialize_cv_metadata import (
    InitializeCVMetadataUsecase,
)
from application.candidate.usecases.match_cv_to_opportunities import (
    MatchCVToOpportunitiesUsecase,
)
from application.candidate.usecases.process_uploaded_cv import ProcessUploadedCVUsecase
from application.candidate.usecases.submit_application import SubmitApplicationUsecase
from domain.audit.services.audit_log_writer import AuditLogWriter
from domain.candidate.services.candidature_actors_validator import (
    CandidatureActorsValidator,
)
from infrastructure.external_gateways.albert_text_formatter import AlbertTextFormatter
from infrastructure.external_gateways.ocr_extractor import OCRExtractor
from infrastructure.gateways.candidate.query_builder import QueryBuilder
from infrastructure.gateways.shared.async_http_client import AsyncHttpClient
from infrastructure.repositories.audit.postgres_audit_log_repository import (
    PostgresAuditLogRepository,
)
from infrastructure.repositories.candidate.async_postgres_cv_metadata_repository import (  # noqa E501
    AsyncPostgresCVMetadataRepository,
)
from infrastructure.repositories.candidate.postgres_candidature_repository import (
    PostgresCandidatureRepository,
)
from infrastructure.repositories.candidate.postgres_cv_metadata_repository import (
    PostgresCVMetadataRepository,
)
from infrastructure.repositories.identite.postgres_candidat_repository import (
    PostgresCandidatRepository,
)


class CandidateContainer(containers.DeclarativeContainer):
    app_config: providers.Dependency = providers.Dependency()
    logger_service: providers.Dependency = providers.Dependency()

    shared_container = providers.DependenciesContainer()

    corps_repository = shared_container.corps_repository
    concours_repository = shared_container.concours_repository
    offers_repository = shared_container.offers_repository
    metiers_repository = shared_container.metiers_repository
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
    candidature_repository = providers.Singleton(PostgresCandidatureRepository)
    candidat_repository = providers.Singleton(PostgresCandidatRepository)
    audit_log_repository = providers.Singleton(PostgresAuditLogRepository)

    actors_validator = providers.Factory(
        CandidatureActorsValidator,
        candidat_repo=candidat_repository,
        offers_repo=offers_repository,
    )

    audit_log_writer = providers.Factory(
        AuditLogWriter,
        repository=audit_log_repository,
    )

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
        cv_metadata_repository=postgres_cv_metadata_repository,
        embedding_generator=embedding_generator,
        vector_repository=vector_repository,
        concours_repository=concours_repository,
        offers_repository=offers_repository,
        metiers_repository=metiers_repository,
        logger=logger_service,
    )

    get_opportunity_details_usecase = providers.Factory(
        GetOpportunityDetailsUsecase,
        offers_repository=offers_repository,
        concours_repository=concours_repository,
        metiers_repository=metiers_repository,
        logger=logger_service,
    )

    submit_application_usecase = providers.Factory(
        SubmitApplicationUsecase,
        candidature_repository=candidature_repository,
        actors_validator=actors_validator,
        audit_log_writer=audit_log_writer,
        logger=logger_service,
    )
