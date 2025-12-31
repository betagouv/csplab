"""Container factory for creating isolated ingestion containers per request."""

from typing import cast

import environ
from pydantic import HttpUrl

from apps.ingestion.config import IngestionConfig, PisteConfig, TalentSoftConfig
from apps.ingestion.containers import IngestionContainer
from apps.shared.config import OpenAIConfig, SharedConfig
from apps.shared.containers import SharedContainer
from apps.shared.infrastructure.adapters.external.logger import LoggerService


def create_ingestion_container() -> IngestionContainer:
    """Create an isolated container for each request to avoid concurrency issues."""
    env = environ.Env()

    shared_container = SharedContainer()
    openai_config = OpenAIConfig(
        api_key=cast(str, env.str("TYCHO_OPENROUTER_API_KEY")),
        base_url=cast(HttpUrl, env.str("TYCHO_OPENROUTER_BASE_URL")),
        model=cast(str, env.str("TYCHO_OPENROUTER_EMBEDDING_MODEL")),
    )
    shared_config = SharedConfig(openai_config)
    shared_container.config.override(shared_config)

    container = IngestionContainer()
    piste_config = PisteConfig(
        oauth_base_url=cast(HttpUrl, env.str("TYCHO_PISTE_OAUTH_BASE_URL")),
        ingres_base_url=cast(HttpUrl, env.str("TYCHO_INGRES_BASE_URL")),
        client_id=cast(str, env.str("TYCHO_INGRES_CLIENT_ID")),
        client_secret=cast(str, env.str("TYCHO_INGRES_CLIENT_SECRET")),
    )
    talentsoft_config = TalentSoftConfig(
        base_url=cast(HttpUrl, env.str("TYCHO_TALENTSOFT_BASE_URL")),
        api_key=cast(str, env.str("TYCHO_TALENTSOFT_API_KEY")),
    )

    ingestion_config = IngestionConfig(piste_config, talentsoft_config)
    container.config.override(ingestion_config)

    logger_service = LoggerService("ingestion")
    container.logger_service.override(logger_service)

    container.shared_container.override(shared_container)

    return container
