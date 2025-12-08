"""Singleton container for ingestion services with auto-configuration."""

from apps.candidate.containers import CandidateContainer
from apps.shared.container_singleton import SharedContainerSingleton
from apps.shared.infrastructure.adapters.external.logger import LoggerService


class CandidateContainerSingleton:
    """Singleton wrapper for IngestionContainer with auto-configuration."""

    _container = None

    @classmethod
    def get_container(cls) -> CandidateContainer:
        """Get configured container instance."""
        if cls._container is None:
            cls._container = cls._create_configured_container()
        return cls._container

    @classmethod
    def _create_configured_container(cls) -> CandidateContainer:
        """Create and configure the ingestion container."""
        container = CandidateContainer()

        logger_service = LoggerService()
        container.logger_service.override(logger_service)

        # Inject shared container singleton
        shared_container = SharedContainerSingleton.get_container()
        container.shared_container.override(shared_container)

        return container
