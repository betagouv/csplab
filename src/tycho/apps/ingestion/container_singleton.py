"""Singleton container for ingestion services with auto-configuration."""

from typing import cast

import environ
from pydantic import HttpUrl

from apps.ingestion.config import IngestionConfig, PisteConfig
from apps.ingestion.containers import IngestionContainer
from apps.ingestion.infrastructure.adapters.external.http_client import HttpClient
from apps.shared.container_singleton import SharedContainerSingleton
from apps.shared.infrastructure.adapters.external.logger import LoggerService


class IngestionContainerSingleton:
    """Singleton wrapper for IngestionContainer with auto-configuration."""

    _container = None

    @classmethod
    def get_container(cls) -> IngestionContainer:
        """Get configured container instance."""
        if cls._container is None:
            cls._container = cls._create_configured_container()
        return cls._container

    @classmethod
    def _create_configured_container(cls) -> IngestionContainer:
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
        shared_container = SharedContainerSingleton.get_container()
        container.shared_container.override(shared_container)

        return container
