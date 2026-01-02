"""Container factory for creating isolated candidate containers per request."""

from typing import cast

import environ
from pydantic import HttpUrl

from apps.candidate.containers import CandidateContainer
from apps.shared.containers import SharedContainer
from infrastructure.external_services.configs.albert_config import (
    AlbertConfig,
    AlbertServiceConfig,
)
from infrastructure.external_services.configs.openai_config import (
    OpenAIConfig,
    OpenAIServiceConfig,
)
from infrastructure.external_services.logger import LoggerService


def create_candidate_container() -> CandidateContainer:
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

    albert_config = AlbertConfig(
        api_base_url=cast(HttpUrl, env.str("TYCHO_ALBERT_API_BASE_URL")),
        api_key=cast(str, env.str("TYCHO_ALBERT_API_KEY")),
        model_name=cast(str, env.str("TYCHO_ALBERT_MODEL", default="albert-large")),
        dpi=cast(int, env.int("TYCHO_ALBERT_DPI", default=200)),
    )

    albert_service_config = AlbertServiceConfig(albert_config)

    container = CandidateContainer()
    container.config.override(albert_service_config)

    logger_service = LoggerService("candidate")
    container.logger_service.override(logger_service)

    container.shared_container.override(shared_container)

    return container
