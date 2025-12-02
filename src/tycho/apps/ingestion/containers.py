"""Ingestion dependency injection container."""

from dependency_injector import containers, providers

from apps.ingestion.application.usecases.clean_documents import CleanDocumentsUsecase
from apps.ingestion.application.usecases.load_documents import LoadDocumentsUsecase
from apps.ingestion.infrastructure.adapters.external import (
    document_fetcher,
    piste_client,
)
from apps.ingestion.infrastructure.adapters.persistence.repositories import (
    django_corps_repository,
    in_memory_corps_repository,
)
from apps.ingestion.infrastructure.adapters.persistence.repositories import (
    django_document_repository as django_repo,
)
from apps.ingestion.infrastructure.adapters.persistence.repositories import (
    in_memory_document_repository as inmemory_repo,
)
from apps.ingestion.infrastructure.adapters.persistence.repository_factory import (
    RepositoryFactory,
)
from apps.ingestion.infrastructure.adapters.services.document_cleaner import (
    DocumentCleaner,
)
from core.entities.document import DocumentType
from core.interfaces.entity_interface import IEntity
from core.interfaces.usecase_interface import IUseCase
from core.repositories.document_repository_interface import (
    CompositeDocumentRepository,
    IUpsertResult,
)
from core.services.document_cleaner_interface import IDocumentCleaner


class IngestionContainer(containers.DeclarativeContainer):
    """Ingestion services container."""

    # Configuration for in-memory mode
    in_memory_mode = providers.Configuration()

    # External dependencies (injected by parent container)
    logger_service: providers.Dependency = providers.Dependency()
    http_client: providers.Dependency = providers.Dependency()

    config: providers.Dependency = providers.Dependency()

    # PISTE client for authenticated API calls
    piste_client = providers.Singleton(
        piste_client.PisteClient,
        config=providers.Callable(lambda cfg: cfg.piste, config),
        logger_service=logger_service,
    )

    # Document adapters
    document_fetcher = providers.Singleton(
        document_fetcher.ExternalDocumentFetcher,
        piste_client=piste_client,
        logger_service=logger_service,
    )

    document_persister = providers.Singleton(
        django_repo.DjangoDocumentRepository,
    )

    # Document repository with conditional selection
    document_repository = providers.Selector(
        in_memory_mode,
        in_memory=providers.Singleton(inmemory_repo.InMemoryDocumentRepository),
        external=providers.Singleton(
            CompositeDocumentRepository,
            fetcher=document_fetcher,
            persister=document_persister,
        ),
    )

    # Corps repository
    corps_repository = providers.Selector(
        in_memory_mode,
        in_memory=providers.Singleton(
            in_memory_corps_repository.InMemoryCorpsRepository
        ),
        external=providers.Singleton(django_corps_repository.DjangoCorpsRepository),
    )

    # Repository factory
    repository_factory = providers.Singleton(
        RepositoryFactory,
        corps_repository=corps_repository,
    )

    # Document cleaner factory
    document_cleaner: providers.Provider[IDocumentCleaner[IEntity]] = (
        providers.Singleton(
            DocumentCleaner,
            logger=logger_service,
        )
    )

    # Use cases - with type annotation to enforce IUseCase compliance
    load_documents_usecase: providers.Provider[
        IUseCase[DocumentType, IUpsertResult]
    ] = providers.Factory(
        LoadDocumentsUsecase,
        document_repository=document_repository,
        logger=logger_service,
    )

    clean_documents_usecase: providers.Provider[IUseCase[DocumentType, dict]] = (
        providers.Factory(
            CleanDocumentsUsecase,
            document_repository=document_repository,
            document_cleaner=document_cleaner,
            repository_factory=repository_factory,
            logger=logger_service,
        )
    )
