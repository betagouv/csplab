"""Ingestion dependency injection container."""

from dependency_injector import containers, providers

from apps.ingestion.infrastructure.adapters.external import (
    ingres_corps_repository,
    piste_client,
)
from apps.ingestion.infrastructure.adapters.persistence.repositories import (
    django_document_repository,
    in_memory_document_repository,
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

    # Ingestion services
    piste_client = providers.Factory(
        piste_client.PisteClient, logger_service=logger_service, http_client=http_client
    )

    # Ingestion repositories
    corps_repository = providers.Singleton(
        ingres_corps_repository.IngresCorpsRepository,
        client=piste_client,
        logger_service=logger_service,
    )

    # Document repository with conditional selection
    document_repository = providers.Selector(
        in_memory_mode,
        in_memory=providers.Singleton(
            in_memory_document_repository.InMemoryDocumentRepository
        ),
        django=providers.Singleton(django_document_repository.DjangoDocumentRepository),
    )
