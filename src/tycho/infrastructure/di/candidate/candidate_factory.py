"""Container factory for creating isolated candidate containers per request."""

from typing import Optional

from config.app_config import AppConfig
from infrastructure.di.candidate.candidate_container import CandidateContainer
from infrastructure.di.shared.shared_container import SharedContainer
from infrastructure.gateways.shared.logger import LoggerService


def create_candidate_container(
    app_config: Optional[AppConfig] = None,
) -> CandidateContainer:
    """Create an isolated container for each request to avoid concurrency issues."""
    config = app_config or AppConfig.from_django_settings()

    # Create shared container
    shared_container = SharedContainer()
    shared_container.app_config.override(config)

    logger_service = LoggerService("candidate")
    shared_container.logger_service.override(logger_service)

    # Create candidate container
    container = CandidateContainer()
    container.app_config.override(config)
    container.logger_service.override(logger_service)
    container.shared_container.override(shared_container)

    return container
