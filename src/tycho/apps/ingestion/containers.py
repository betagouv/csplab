"""Ingestion dependency injection container."""

from dependency_injector import containers, providers

from apps.ingestion.infrastructure.adapters.external import (
    document_fetcher,
)
from apps.ingestion.infrastructure.adapters.persistence.repositories import (
    document_persister,
    in_memory_document_repository,
)
from core.interfaces.document_repository_interface import (
    IDocumentRepository,
)
from core.interfaces.http_client_interface import IHttpClient
from core.interfaces.logger_interface import ILogger


class IngestionContainer(containers.DeclarativeContainer):
    """Ingestion services container."""

    # Configuration for in-memory mode
    in_memory_mode = providers.Configuration()

    # External dependencies (injected by parent container)
    logger_service: providers.Dependency[ILogger] = providers.Dependency()
    http_client: providers.Dependency[IHttpClient] = providers.Dependency()

    # Document adapters
    document_fetcher = providers.Singleton(
        document_fetcher.ExternalDocumentFetcher,
        http_client=http_client,
        logger_service=logger_service,
    )

    document_persister = providers.Singleton(
        document_persister.DjangoDocumentPersister,
    )

    # Document repository with conditional selection
    document_repository = providers.Selector(
        in_memory_mode,
        in_memory=providers.Singleton(
            in_memory_document_repository.InMemoryDocumentRepository
        ),
        django=providers.Singleton(
            IDocumentRepository,
            fetcher=document_fetcher,
            persister=document_persister,
        ),
    )
