from dependency_injector import containers, providers

from infrastructure.external_gateways.albert_embedding_generator import (
    AlbertEmbeddingGenerator,
)
from infrastructure.gateways.shared.async_http_client import AsyncHttpClient
from infrastructure.mappers.metier_mapper import MetierMapper
from infrastructure.mappers.offer_mapper import OfferMapper
from infrastructure.repositories.commons.postgres_offer_stats_query_service import (
    PostgresOfferStatsQueryService,
)
from infrastructure.repositories.commons.postgres_stat_snapshot_writer import (
    PostgresStatSnapshotWriter,
)
from infrastructure.repositories.shared import (
    postgres_concours_repository,
    postgres_corps_repository,
    postgres_metier_repository,
    postgres_offers_repository,
)
from infrastructure.repositories.shared.postgres_api_log_daily_agg_repository import (
    PostgresApiLogDailyAggregationRepository,
)
from infrastructure.repositories.shared.postgres_api_log_repository import (
    PostgresApiLogRepository,
)
from infrastructure.repositories.shared.qdrant_repository import QdrantRepository


class SharedContainer(containers.DeclarativeContainer):
    app_config: providers.Dependency = providers.Dependency()
    logger_service: providers.Dependency = providers.Dependency()

    api_log_repository = providers.Singleton(PostgresApiLogRepository)

    api_log_daily_aggregation_repository = providers.Singleton(
        PostgresApiLogDailyAggregationRepository
    )

    offer_stats_query_service = providers.Singleton(PostgresOfferStatsQueryService)

    stat_snapshot_writer = providers.Singleton(PostgresStatSnapshotWriter)

    corps_repository = providers.Singleton(
        postgres_corps_repository.PostgresCorpsRepository,
        logger=logger_service,
    )

    concours_repository = providers.Singleton(
        postgres_concours_repository.PostgresConcoursRepository,
        logger=logger_service,
    )

    offers_mapper = OfferMapper()

    offers_repository = providers.Singleton(
        postgres_offers_repository.PostgresOffersRepository,
        mapper=offers_mapper,
        logger=logger_service,
    )

    metiers_mapper = MetierMapper()

    metiers_repository = providers.Singleton(
        postgres_metier_repository.PostgresMetierRepository,
        mapper=metiers_mapper,
        logger=logger_service,
    )

    http_client = providers.Singleton(AsyncHttpClient)

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
