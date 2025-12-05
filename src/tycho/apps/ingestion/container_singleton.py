"""Singleton container for ingestion services with auto-configuration."""

from typing import cast

import environ
from pydantic import HttpUrl

from apps.ingestion.config import IngestionConfig, PisteConfig
from apps.ingestion.containers import IngestionContainer
from apps.ingestion.infrastructure.adapters.external.http_client import HttpClient
from apps.ingestion.infrastructure.adapters.external.logger import LoggerService
from apps.shared.container_singleton import get_shared_container


class IngestionContainerSingleton:
    """Singleton wrapper for IngestionContainer with auto-configuration."""

    _instance = None
    _container = None

    def __new__(cls):
        """Ensure only one instance exists."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def get_container(self) -> IngestionContainer:
        """Get configured container instance."""
        if self._container is None:
            self._container = self._create_configured_container()
        return self._container

    def _create_configured_container(self) -> IngestionContainer:
        """Create and configure the ingestion container."""
        container = IngestionContainer()

        logger_service = LoggerService()
        container.logger_service.override(logger_service)

        http_client = HttpClient()
        container.http_client.override(http_client)

        env = environ.Env()

        piste_config = PisteConfig(
            oauth_base_url=cast(HttpUrl, env.str("TYCHO_PISTE_OAUTH_BASE_URL")),
            ingres_base_url=cast(HttpUrl, env.str("TYCHO_INGRES_BASE_URL")),
            client_id=cast(str, env.str("TYCHO_INGRES_CLIENT_ID")),
            client_secret=cast(str, env.str("TYCHO_INGRES_CLIENT_SECRET")),
        )

        ingestion_config = IngestionConfig(piste_config=piste_config)
        container.config.override(ingestion_config)

        # Inject shared container singleton
        shared_container = get_shared_container()
        container.shared_container.override(shared_container)

        return container


_ingestion_singleton = IngestionContainerSingleton()


def get_ingestion_container() -> IngestionContainer:
    """Get the configured ingestion container singleton."""
    return _ingestion_singleton.get_container()
