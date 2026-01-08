"""Container factory for creating isolated candidate containers per request."""

from typing import cast

import environ
from pydantic import HttpUrl

from domain.value_objects.pdf_extractor_type import PDFExtractorType
from infrastructure.di.candidate.candidate_container import CandidateContainer
from infrastructure.di.shared.shared_container import SharedContainer
from infrastructure.external_gateways.configs.albert_config import (
    AlbertConfig,
)
from infrastructure.external_gateways.configs.openai_config import (
    OpenAIConfig,
    OpenAIGatewayConfig,
)
from infrastructure.external_gateways.configs.pdf_extractor_config import (
    PDFExtractorConfig,
)
from infrastructure.gateways.shared.logger import LoggerService


def create_candidate_container() -> CandidateContainer:
    """Create an isolated container for each request to avoid concurrency issues."""
    env = environ.Env()

    shared_container = SharedContainer()
    openai_config = OpenAIConfig(
        api_key=cast(str, env.str("TYCHO_OPENROUTER_API_KEY")),
        base_url=cast(HttpUrl, env.str("TYCHO_OPENROUTER_BASE_URL")),
        model=cast(str, env.str("TYCHO_OPENROUTER_EMBEDDING_MODEL")),
    )
    openai_gateway_config = OpenAIGatewayConfig(openai_config)
    shared_container.config.override(openai_gateway_config)

    albert_config = AlbertConfig(
        api_base_url=cast(HttpUrl, env.str("TYCHO_ALBERT_API_BASE_URL")),
        api_key=cast(str, env.str("TYCHO_ALBERT_API_KEY")),
        model_name=cast(str, env.str("TYCHO_ALBERT_MODEL", default="albert-large")),
        dpi=cast(int, env.int("TYCHO_ALBERT_DPI", default=200)),
    )

    openai_ocr_config = OpenAIConfig(
        api_key=cast(str, env.str("TYCHO_OPENROUTER_API_KEY")),
        base_url=cast(HttpUrl, env.str("TYCHO_OPENROUTER_BASE_URL")),
        model=cast(str, env.str("TYCHO_OPENROUTER_OCR_MODEL")),
    )

    # Feature flag for PDF extractor type from environment
    ocr_type = env.str("TYCHO_OCR_TYPE", default="ALBERT").upper()
    pdf_extractor_type = (
        PDFExtractorType.ALBERT if ocr_type == "ALBERT" else PDFExtractorType.OPENAI
    )

    pdf_extractor_config = PDFExtractorConfig(
        pdf_extractor_type=pdf_extractor_type,
        albert_config=albert_config,
        openai_config=openai_ocr_config,
    )

    container = CandidateContainer()
    container.config.override(pdf_extractor_config)

    logger_service = LoggerService("candidate")
    container.logger_service.override(logger_service)

    container.shared_container.override(shared_container)

    return container
