"""Shared infrastructure services container."""

from dependency_injector import containers, providers

from infrastructure.external_gateways.openai_embedding_generator import (
    OpenAIEmbeddingGenerator,
)
from infrastructure.repositories.shared import (
    pgvector_repository,
    postgres_concours_repository,
    postgres_corps_repository,
    postgres_offers_repository,
)


class SharedContainer(containers.DeclarativeContainer):
    """Container for shared infrastructure services."""

    app_config: providers.Dependency = providers.Dependency()
    logger_service: providers.Dependency = providers.Dependency()

    corps_repository = providers.Singleton(
        postgres_corps_repository.PostgresCorpsRepository,
        logger=logger_service,
    )

    concours_repository = providers.Singleton(
        postgres_concours_repository.PostgresConcoursRepository,
        logger=logger_service,
    )

    offers_repository = providers.Singleton(
        postgres_offers_repository.PostgresOffersRepository,
        logger=logger_service,
    )

    embedding_generator = providers.Singleton(
        OpenAIEmbeddingGenerator,
        config=providers.Callable(lambda cfg: cfg.openai, app_config),
    )

    vector_repository = providers.Singleton(
        pgvector_repository.PgVectorRepository,
        logger=logger_service,
    )
