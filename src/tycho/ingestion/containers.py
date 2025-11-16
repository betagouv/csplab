"""Ingestion dependency injection container."""

from dependency_injector import containers, providers

from core.interfaces.http_client_interface import IHttpClient
from core.interfaces.logger_interface import ILoggerService
from ingestion.services.sourcing.corps_sourcer import CorpsSourcer
from ingestion.services.sourcing.piste_client import PisteClient


class IngestionContainer(containers.DeclarativeContainer):
    """Ingestion services container."""

    # External dependencies (injected by parent container)
    logger_service: ILoggerService = providers.Dependency()
    http_client: IHttpClient = providers.Dependency()

    # Ingestion services
    piste_client = providers.Factory(
        PisteClient, logger_service=logger_service, http_client=http_client
    )

    corps_sourcer = providers.Factory(
        CorpsSourcer, client=piste_client, logger_service=logger_service
    )
