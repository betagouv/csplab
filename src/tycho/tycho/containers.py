"""Main application dependency injection container."""

from dependency_injector import containers, providers

from core.containers import CoreContainer
from ingestion.containers import IngestionContainer


class ApplicationContainer(containers.DeclarativeContainer):
    """Main application container that composes all sub-containers."""

    # Configuration
    config = providers.Configuration()

    # Core services container
    core = providers.Container(CoreContainer)

    # Application containers with injected dependencies
    ingestion = providers.Container(
        IngestionContainer,
        logger_service=core.logger_service,
        http_client=core.http_client,
    )

    # Wiring configuration
    wiring_config = containers.WiringConfiguration(
        modules=[
            "ingestion.views",
            "ingestion.services.sourcing.corps_sourcer",
        ]
    )
