"""Shared infrastructure services container."""

from dependency_injector import containers, providers

from infrastructure.external_gateways.albert_embedding_generator import (
    AlbertEmbeddingGenerator,
)
from infrastructure.external_gateways.openai_embedding_generator import (
    OpenAIEmbeddingGenerator,
)
from infrastructure.gateways.shared.http_client import SyncHttpClient
from infrastructure.repositories.shared import (
    pgvector_repository,
    postgres_concours_repository,
    postgres_corps_repository,
    postgres_offers_repository,
)
from infrastructure.repositories.shared.qdrant_repository import QdrantRepository


def _create_vector_repository(config, logger):
    if config.vector_db_type == "QDRANT":
        return QdrantRepository(config=config.qdrant, logger=logger)
    else:
        # Default to PgVector
        return pgvector_repository.PgVectorRepository(logger=logger)


def _create_embedding_generator(app_config, http_client):
    generators = {
        "ALBERT": lambda cfg: AlbertEmbeddingGenerator(
            config=cfg.albert, http_client=http_client
        ),
        "OPENAI": lambda cfg: OpenAIEmbeddingGenerator(config=cfg.openai),
    }
    embedding_type = "ALBERT" if app_config.embedding_type == "ALBERT" else "OPENAI"
    return generators[embedding_type](app_config)


class SharedContainer(containers.DeclarativeContainer):
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

    # HTTP client for sync operations
    http_client = providers.Singleton(SyncHttpClient)

    embedding_generator = providers.Callable(
        _create_embedding_generator,
        app_config,
        http_client,
    )

    # Vector repository with feature flag (PgVector or Qdrant)
    vector_repository = providers.Factory(
        _create_vector_repository,
        config=app_config,
        logger=logger_service,
    )
