from typing import Optional

from config.app_config import AppConfig
from config.logger_names import LoggerName
from infrastructure.di.identite.identite_container import IdentiteContainer
from infrastructure.gateways.shared.logger import LoggerService


def create_identite_container(
    app_config: Optional[AppConfig] = None,
) -> IdentiteContainer:
    config = app_config or AppConfig.from_django_settings()

    logger_service = LoggerService(LoggerName.IDENTITE.value)

    # Create candidate container
    container = IdentiteContainer()
    container.app_config.override(config)
    container.logger_service.override(logger_service)

    return container
