"""Ingestion dependency injection container."""

from dependency_injector import containers, providers

from application.ingestion.interfaces.load_documents_input import (
    LoadDocumentsInput,
)
from application.ingestion.services import (
    load_documents_strategy_factory as load_strategy,
)
from application.ingestion.services.document_cleaner import (
    DocumentCleaner,
)
from application.ingestion.services.text_extractor import (
    TextExtractor,
)
from application.ingestion.usecases.clean_documents import CleanDocumentsUsecase
from application.ingestion.usecases.load_documents import LoadDocumentsUsecase
from application.ingestion.usecases.vectorize_documents import (
    VectorizeDocumentsUsecase,
)
from apps.ingestion.infrastructure.adapters.external import (
    document_fetcher,
    piste_client,
)
from apps.ingestion.infrastructure.adapters.persistence.repositories import (
    django_document_repository as django_repo,
)
from apps.ingestion.infrastructure.adapters.persistence.repository_factory import (
    RepositoryFactory,
)
from domain.entities.document import DocumentType
from domain.interfaces.entity_interface import IEntity
from domain.interfaces.usecase_interface import IUseCase
from domain.repositories.document_repository_interface import (
    CompositeDocumentRepository,
    IUpsertResult,
)
from domain.services.document_cleaner_interface import IDocumentCleaner


class IngestionContainer(containers.DeclarativeContainer):
    """Ingestion services container."""

    logger_service: providers.Dependency = providers.Dependency()
    http_client: providers.Dependency = providers.Dependency()
    config: providers.Dependency = providers.Dependency()

    shared_container = providers.DependenciesContainer()

    corps_repository = shared_container.corps_repository
    concours_repository = shared_container.concours_repository
    embedding_generator = shared_container.embedding_generator
    vector_repository = shared_container.vector_repository

    piste_client = providers.Singleton(
        piste_client.PisteClient,
        config=providers.Callable(lambda cfg: cfg.piste, config),
        logger_service=logger_service,
    )

    document_fetcher = providers.Singleton(
        document_fetcher.ExternalDocumentFetcher,
        piste_client=piste_client,
        logger_service=logger_service,
    )

    document_persister = providers.Singleton(
        django_repo.DjangoDocumentRepository,
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
    )

    document_cleaner: providers.Provider[IDocumentCleaner[IEntity]] = (
        providers.Singleton(
            DocumentCleaner,
            logger=logger_service,
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
