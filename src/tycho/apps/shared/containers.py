"""Shared infrastructure services container."""

from dependency_injector import containers, providers

from apps.shared.infrastructure.adapters.external.openai_embedding_generator import (
    OpenAIEmbeddingGenerator,
)
from apps.shared.infrastructure.adapters.persistence.repositories import (
    django_concours_repository,
    django_corps_repository,
    django_offer_repository,
    pgvector_repository,
)


class SharedContainer(containers.DeclarativeContainer):
    """Container for shared infrastructure services."""

    config: providers.Dependency = providers.Dependency()

    corps_repository = providers.Singleton(
        django_corps_repository.DjangoCorpsRepository
    )

    concours_repository = providers.Singleton(
        django_concours_repository.DjangoConcoursRepository
    )

    offer_repository = providers.Singleton(
        django_offer_repository.DjangoOfferRepository
    )

    embedding_generator = providers.Singleton(
        OpenAIEmbeddingGenerator,
        config=providers.Callable(lambda cfg: cfg.openai, config),
    )

    vector_repository = providers.Singleton(pgvector_repository.PgVectorRepository)
