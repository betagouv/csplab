"""Container factory for creating isolated candidate containers per request."""

from typing import cast

import environ
from pydantic import HttpUrl

from apps.candidate.application.usecases.mock_match_cv_to_opportunities import (
    MockMatchCVToOpportunitiesUsecase,
)
from apps.candidate.application.usecases.mock_process_uploaded_cv import (
    MockProcessUploadedCVUsecase,
)
from apps.candidate.config import AlbertConfig, CandidateConfig
from apps.candidate.containers import CandidateContainer
from apps.shared.config import OpenAIConfig, SharedConfig
from apps.shared.containers import SharedContainer
from apps.shared.infrastructure.adapters.external.logger import LoggerService


def create_candidate_container() -> CandidateContainer:
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

    albert_config = AlbertConfig(
        api_base_url=cast(HttpUrl, env.str("TYCHO_ALBERT_API_BASE_URL")),
        api_key=cast(str, env.str("TYCHO_ALBERT_API_KEY")),
        model_name=cast(str, env.str("TYCHO_ALBERT_MODEL", default="albert-large")),
        dpi=cast(int, env.int("TYCHO_ALBERT_DPI", default=200)),
    )

    candidate_config = CandidateConfig(albert_config)

    container = CandidateContainer()
    container.config.override(candidate_config)

    logger_service = LoggerService("candidate")
    container.logger_service.override(logger_service)

    container.shared_container.override(shared_container)

    # Override usecases with mocks if environment variables are enabled
    use_mock_albert = env.bool("TYCHO_USE_MOCK_ALBERT", default=False)
    use_mock_openrouter = env.bool("TYCHO_USE_MOCK_OPENROUTER", default=False)

    candidate_logger = logger_service.get_logger("CANDIDATE::CONTAINER_FACTORY")

    if use_mock_albert:
        candidate_logger.info("🎭 Using MOCK for Albert (CV processing without external API)")
        container.process_uploaded_cv_usecase.override(
            MockProcessUploadedCVUsecase(
                cv_metadata_repository=container.cv_metadata_repository(),
                logger=logger_service,
            )
        )

    if use_mock_openrouter:
        candidate_logger.info("🎭 Using MOCK for OpenRouter (CV matching without embeddings API)")
        container.match_cv_to_opportunities_usecase.override(
            MockMatchCVToOpportunitiesUsecase(
                cv_metadata_repository=container.cv_metadata_repository(),
                concours_repository=shared_container.concours_repository(),
                logger=logger_service,
            )
        )

    return container
