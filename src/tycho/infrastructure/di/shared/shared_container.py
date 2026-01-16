"""Shared infrastructure services container."""

from dependency_injector import containers, providers

from infrastructure.external_gateways.openai_embedding_generator import (
    OpenAIEmbeddingGenerator,
)
from infrastructure.repositories.shared import (
    pgvector_repository,
    postgres_concours_repository,
    postgres_corps_repository,
)


class SharedContainer(containers.DeclarativeContainer):
    """Container for shared infrastructure services."""

    config: providers.Dependency = providers.Dependency()

    corps_repository = providers.Singleton(
        postgres_corps_repository.PostgresCorpsRepository
    )

    concours_repository = providers.Singleton(
        postgres_concours_repository.PostgresConcoursRepository
    )

    # Temporary placeholder for offers repository (for testing)
    offers_repository: providers.Dependency = providers.Dependency()

    embedding_generator = providers.Singleton(
        OpenAIEmbeddingGenerator,
        config=providers.Callable(lambda cfg: cfg.openai, config),
    )

    vector_repository = providers.Singleton(pgvector_repository.PgVectorRepository)
