from typing import Optional

from config.app_config import AppConfig
from infrastructure.di.recruteur.recruteur_container import RecruteurContainer
from infrastructure.gateways.shared.logger import LoggerService


def recruteur_container(
    app_config: Optional[AppConfig] = None,
) -> RecruteurContainer:
    config = app_config or AppConfig.from_django_settings()

    logger_service = LoggerService("recruteur")

    container = RecruteurContainer()
    container.app_config.override(config)
    container.logger_service.override(logger_service)

    return container
