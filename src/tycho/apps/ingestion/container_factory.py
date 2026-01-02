"""Container factory for creating isolated ingestion containers per request."""

from typing import cast

import environ
from pydantic import HttpUrl

from apps.ingestion.containers import IngestionContainer
from apps.shared.containers import SharedContainer
from infrastructure.external_services.configs.albert_config import (
    AlbertConfig,
    AlbertServiceConfig,
)
from infrastructure.external_services.configs.openai_config import (
    OpenAIConfig,
    OpenAIServiceConfig,
)
from infrastructure.external_services.configs.piste_config import (
    PisteConfig,
    PisteServiceConfig,
)
from infrastructure.external_services.logger import LoggerService


def create_ingestion_container() -> IngestionContainer:
    """Create an isolated container for each request to avoid concurrency issues."""
    env = environ.Env()

    shared_container = SharedContainer()
    openai_config = OpenAIConfig(
        api_key=cast(str, env.str("TYCHO_OPENROUTER_API_KEY")),
        base_url=cast(HttpUrl, env.str("TYCHO_OPENROUTER_BASE_URL")),
        model=cast(str, env.str("TYCHO_OPENROUTER_EMBEDDING_MODEL")),
    )
    openai_service_config = OpenAIServiceConfig(openai_config)
    shared_container.config.override(openai_service_config)

    container = IngestionContainer()
    piste_config = PisteConfig(
        oauth_base_url=cast(HttpUrl, env.str("TYCHO_PISTE_OAUTH_BASE_URL")),
        ingres_base_url=cast(HttpUrl, env.str("TYCHO_INGRES_BASE_URL")),
        client_id=cast(str, env.str("TYCHO_INGRES_CLIENT_ID")),
        client_secret=cast(str, env.str("TYCHO_INGRES_CLIENT_SECRET")),
    )
    piste_service_config = PisteServiceConfig(piste_config)
    container.config.override(piste_service_config)

    logger_service = LoggerService("ingestion")
    container.logger_service.override(logger_service)

    container.shared_container.override(shared_container)

    return container
