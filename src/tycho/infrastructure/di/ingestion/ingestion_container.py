"""Ingestion dependency injection container."""

from dependency_injector import containers, providers

from application.ingestion.interfaces.load_documents_input import LoadDocumentsInput
from application.ingestion.usecases.clean_documents import CleanDocumentsUsecase
from application.ingestion.usecases.load_documents import LoadDocumentsUsecase
from application.ingestion.usecases.vectorize_documents import VectorizeDocumentsUsecase
from domain.entities.document import DocumentType
from domain.interfaces.entity_interface import IEntity
from domain.interfaces.usecase_interface import IUseCase
from domain.repositories.document_repository_interface import (
    CompositeDocumentRepository,
    IUpsertResult,
)
from domain.services.document_cleaner_interface import IDocumentCleaner
from infrastructure.external_gateways import (
    document_fetcher,
    piste_client,
    talentsoft_client,
)
from infrastructure.gateways.ingestion import (
    load_documents_strategy_factory as load_strategy,
)
from infrastructure.gateways.ingestion.document_cleaner import DocumentCleaner
from infrastructure.gateways.ingestion.text_extractor import TextExtractor
from infrastructure.repositories.ingestion import postgres_document_repository
from infrastructure.repositories.repository_factory import RepositoryFactory


class IngestionContainer(containers.DeclarativeContainer):
    """Ingestion services container."""

    logger_service: providers.Dependency = providers.Dependency()
    http_client: providers.Dependency = providers.Dependency()
    config: providers.Dependency = providers.Dependency()
    talentsoft_gateway_config: providers.Dependency = providers.Dependency()

    shared_container = providers.DependenciesContainer()

    # Wire the logger_service to the shared_container
    shared_container.logger_service.override(logger_service)

    corps_repository = shared_container.corps_repository
    concours_repository = shared_container.concours_repository
    offers_repository = shared_container.offers_repository
    embedding_generator = shared_container.embedding_generator
    vector_repository = shared_container.vector_repository

    piste_client = providers.Singleton(
        piste_client.PisteClient,
        config=providers.Callable(lambda cfg: cfg.piste, config),
        logger_service=logger_service,
    )

    talentsoft_front_client = providers.Singleton(
        talentsoft_client.TalentsoftFrontClient,
        config=talentsoft_gateway_config,
        logger_service=logger_service,
    )

    document_fetcher = providers.Singleton(
        document_fetcher.ExternalDocumentFetcher,
        piste_client=piste_client,
        talentsoft_front_client=talentsoft_front_client,
        logger_service=logger_service,
    )

    document_persister = providers.Singleton(
        postgres_document_repository.PostgresDocumentRepository,
    )

    document_repository = providers.Singleton(
        CompositeDocumentRepository,
        fetcher=document_fetcher,
        persister=document_persister,
    )

    repository_factory = providers.Singleton(
        RepositoryFactory,
        corps_repository=corps_repository,
        concours_repository=concours_repository,
        offers_repository=offers_repository,
    )

    document_cleaner: providers.Provider[IDocumentCleaner[IEntity]] = (
        providers.Singleton(
            DocumentCleaner,
            logger=logger_service,
            corps_repository=corps_repository,
            concours_repository=concours_repository,
            offers_repository=offers_repository,
        )
    )

    text_extractor = providers.Singleton(
        TextExtractor,
    )

    load_documents_strategy_factory = providers.Singleton(
        load_strategy.LoadDocumentsStrategyFactory,
        document_fetcher=document_fetcher,
    )

    load_documents_usecase: providers.Provider[
        IUseCase[LoadDocumentsInput, IUpsertResult]
    ] = providers.Factory(
        LoadDocumentsUsecase,
        strategy_factory=load_documents_strategy_factory,
        document_repository=document_repository,
        logger=logger_service,
    )

    clean_documents_usecase: providers.Provider[IUseCase[DocumentType, dict]] = (
        providers.Factory(
            CleanDocumentsUsecase,
            document_repository=document_persister,
            document_cleaner=document_cleaner,
            repository_factory=repository_factory,
            logger=logger_service,
        )
    )

    vectorize_documents_usecase = providers.Factory(
        VectorizeDocumentsUsecase,
        vector_repository=vector_repository,
        text_extractor=text_extractor,
        embedding_generator=embedding_generator,
        logger=logger_service,
    )
