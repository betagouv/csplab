"""Ingestion dependency injection container."""

from dependency_injector import containers, providers

from apps.ingestion.application.usecases.load_documents import LoadDocumentsUsecase
from apps.ingestion.infrastructure.adapters.external import (
    document_fetcher,
    piste_client,
)
from apps.ingestion.infrastructure.adapters.persistence.repositories import (
    django_document_repository as django_repo,
)
from apps.ingestion.infrastructure.adapters.persistence.repositories import (
    in_memory_document_repository as inmemory_repo,
)
from core.entities.document import DocumentType
from core.interfaces.usecase_interface import IUseCase
from core.repositories.document_repository_interface import (
    CompositeDocumentRepository,
    IUpsertResult,
)


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

    # Use cases - with type annotation to enforce IUseCase compliance
    load_documents_usecase: providers.Provider[
        IUseCase[DocumentType, IUpsertResult]
    ] = providers.Factory(
        LoadDocumentsUsecase,
        document_repository=document_repository,
        logger=logger_service,
    )
