"""Container factory for creating isolated ingestion containers per request."""

from django.conf import settings

from infrastructure.di.ingestion.ingestion_container import IngestionContainer
from infrastructure.di.shared.shared_container import SharedContainer
from infrastructure.external_gateways.configs.openai_config import (
    OpenAIConfig,
    OpenAIGatewayConfig,
)
from infrastructure.external_gateways.configs.piste_config import (
    PisteConfig,
    PisteGatewayConfig,
)
from infrastructure.external_gateways.configs.talentsoft_config import (
    TalentsoftGatewayConfig,
)
from infrastructure.gateways.shared.logger import LoggerService


def create_ingestion_container() -> IngestionContainer:
    """Create an isolated container for each request to avoid concurrency issues."""
    logger_service = LoggerService("ingestion")
    shared_container = SharedContainer()
    shared_container.logger_service.override(logger_service)
    openai_config = OpenAIConfig(
        api_key=settings.OPENROUTER_API_KEY,
        base_url=settings.OPENROUTER_BASE_URL,
        model=settings.OPENROUTER_EMBEDDING_MODEL,
    )
    openai_gateway_config = OpenAIGatewayConfig(openai_config)
    shared_container.config.override(openai_gateway_config)

    container = IngestionContainer()
    piste_config = PisteConfig(
        oauth_base_url=settings.PISTE_OAUTH_BASE_URL,
        ingres_base_url=settings.INGRES_BASE_URL,
        client_id=settings.INGRES_CLIENT_ID,
        client_secret=settings.INGRES_CLIENT_SECRET,
    )
    piste_gateway_config = PisteGatewayConfig(piste_config)
    container.config.override(piste_gateway_config)

    container.logger_service.override(logger_service)

    talentsoft_gateway_config = TalentsoftGatewayConfig(
        base_url=settings.TALENTSOFT_BASE_URL,
        client_id=settings.TALENTSOFT_CLIENT_ID,
        client_secret=settings.TALENTSOFT_CLIENT_SECRET,
    )
    container.talentsoft_gateway_config.override(talentsoft_gateway_config)

    container.shared_container.override(shared_container)

    return container
