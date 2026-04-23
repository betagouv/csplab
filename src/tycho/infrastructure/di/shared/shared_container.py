from dependency_injector import containers, providers

from infrastructure.external_gateways.albert_embedding_generator import (
    AlbertEmbeddingGenerator,
)
from infrastructure.gateways.shared.http_client import SyncHttpClient
from infrastructure.repositories.shared import (
    postgres_concours_repository,
    postgres_corps_repository,
    postgres_metier_repository,
    postgres_offers_repository,
)
from infrastructure.repositories.shared.qdrant_repository import QdrantRepository


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

    metiers_repository = providers.Singleton(
        postgres_metier_repository.PostgresMetierRepository,
        logger=logger_service,
    )

    # HTTP client for sync operations
    http_client = providers.Singleton(SyncHttpClient)

    embedding_generator = providers.Singleton(
        AlbertEmbeddingGenerator,
        config=app_config.provided.albert,
        http_client=http_client,
    )

    vector_repository = providers.Singleton(
        QdrantRepository,
        config=app_config.provided.qdrant,
        logger=logger_service,
    )
