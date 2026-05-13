"""Container factory for creating isolated ingestion containers per request."""

from typing import Optional

from config.app_config import AppConfig
from infrastructure.di.ingestion.ingestion_container import IngestionContainer
from infrastructure.di.shared.shared_container import SharedContainer
from infrastructure.gateways.shared.logger import LoggerService


def create_ingestion_container(
    app_config: Optional[AppConfig] = None,
) -> IngestionContainer:
    """Create an isolated container for each request to avoid concurrency issues."""
    config = app_config or AppConfig.from_django_settings()

    logger_service = LoggerService("ingestion")

    # Create shared container
    shared_container = SharedContainer()
    shared_container.app_config.override(config)
    shared_container.logger_service.override(logger_service)

    # Create ingestion container
    container = IngestionContainer()
    container.app_config.override(config)
    container.logger_service.override(logger_service)
    container.shared_container.override(shared_container)

    return container
