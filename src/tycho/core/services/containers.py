"""Core dependency injection container."""

from dependency_injector import containers, providers

from .http_client import HttpClient
from .logger import LoggerService


class CoreContainer(containers.DeclarativeContainer):
    """Core services container."""

    # Configuration
    config = providers.Configuration()

    # Core services
    logger_service = providers.Singleton(LoggerService)
    http_client = providers.Factory(HttpClient, timeout=30)
