from ddd.async_usecase_interface import IAsyncUsecase
from ddd.entity import Entity
from dependency_injector import containers, providers
from referentiel.types import IUpsertResult

from application.commons.usecases.calculate_daily_stats import (
    CalculateDailyStatsUsecase,
)
from application.ingestion.interfaces.load_documents_input import LoadDocumentsInput
from application.ingestion.usecases.archive_offer_by_reference import (
    ArchiveOfferByReferenceUsecase,
)
from application.ingestion.usecases.clean_documents import CleanDocumentsUsecase
from application.ingestion.usecases.get_offer_by_reference import (
    GetOfferByReferenceUsecase,
)
from application.ingestion.usecases.get_offers_by_source import (
    GetOffersBySourceUsecase,
)
from application.ingestion.usecases.list_metiers import ListMetiersUsecase
from application.ingestion.usecases.list_offers import ListOffersUsecase
from application.ingestion.usecases.list_sources import ListSourcesUsecase
from application.ingestion.usecases.load_documents import LoadDocumentsUsecase
from application.ingestion.usecases.upsert_offers import UpsertOffersUsecase
from application.ingestion.usecases.upsert_organismes import UpsertOrganismesUsecase
from application.ingestion.usecases.vectorize_documents import VectorizeDocumentsUsecase
from domain.ingestion.services.document_cleaner_interface import IDocumentCleaner
from infrastructure.external_gateways import (
    external_document_gateway,
    piste_client,
)
from infrastructure.gateways.ingestion import (
    load_documents_strategy_factory as load_strategy,
)
from infrastructure.gateways.ingestion.document_cleaner import DocumentCleaner
from infrastructure.gateways.ingestion.text_extractor import TextExtractor
from infrastructure.repositories.identite.postgres_organisme_repository import (
    PostgresOrganismeRepository,
)
from infrastructure.repositories.identite.postgres_utilisateur_repository import (
    PostgresUtilisateurRepository,
)
from infrastructure.repositories.ingestion import (
    postgres_document_repository,
    postgres_source_repository,
)
from infrastructure.repositories.ingestion.postgres_user_source_repository import (
    PostgresUserSourceRepository,
)
from infrastructure.repositories.repository_factory import RepositoryFactory


class IngestionContainer(containers.DeclarativeContainer):
    logger_service: providers.Dependency = providers.Dependency()
    app_config: providers.Dependency = providers.Dependency()

    shared_container = providers.DependenciesContainer()

    # Wire the logger_service to the shared_container
    shared_container.logger_service.override(logger_service)

    corps_repository = shared_container.corps_repository
    concours_repository = shared_container.concours_repository
    offers_repository = shared_container.offers_repository
    metiers_repository = shared_container.metiers_repository
    embedding_generator = shared_container.embedding_generator
    vector_repository = shared_container.vector_repository

    piste_client = providers.Singleton(
        piste_client.PisteClient,
        config=providers.Callable(lambda cfg: cfg.piste, app_config),
        logger_service=logger_service,
    )

    document_gateway = providers.Singleton(
        external_document_gateway.ExternalDocumentGateway,
        piste_client=piste_client,
        logger_service=logger_service,
    )

    document_repository = providers.Singleton(
        postgres_document_repository.PostgresDocumentRepository,
    )

    source_repository = providers.Singleton(
        postgres_source_repository.PostgresSourceRepository,
    )

    user_source_repository = providers.Singleton(
        PostgresUserSourceRepository,
    )

    utilisateur_repository = providers.Singleton(
        PostgresUtilisateurRepository,
    )

    organisme_repository = providers.Singleton(
        PostgresOrganismeRepository,
    )

    repository_factory = providers.Singleton(
        RepositoryFactory,
        corps_repository=corps_repository,
        concours_repository=concours_repository,
        offers_repository=offers_repository,
        metiers_repository=metiers_repository,
    )

    document_cleaner: providers.Provider[IDocumentCleaner[Entity]] = (
        providers.Singleton(
            DocumentCleaner,
            logger=logger_service,
            corps_repository=corps_repository,
            concours_repository=concours_repository,
            metiers_repository=metiers_repository,
        )
    )

    text_extractor = providers.Singleton(
        TextExtractor,
    )

    load_documents_strategy_factory = providers.Singleton(
        load_strategy.LoadDocumentsStrategyFactory,
        document_gateway=document_gateway,
    )

    load_documents_usecase: providers.Provider[
        IAsyncUsecase[LoadDocumentsInput, IUpsertResult]
    ] = providers.Factory(
        LoadDocumentsUsecase,
        strategy_factory=load_documents_strategy_factory,
        document_repository=document_repository,
        logger=logger_service,
    )

    clean_documents_usecase = providers.Factory(
        CleanDocumentsUsecase,
        document_repository=document_repository,
        document_cleaner=document_cleaner,
        repository_factory=repository_factory,
        logger=logger_service,
    )

    vectorize_documents_usecase = providers.Factory(
        VectorizeDocumentsUsecase,
        vector_repository=vector_repository,
        text_extractor=text_extractor,
        embedding_generator=embedding_generator,
        logger=logger_service,
        repository_factory=repository_factory,
    )

    list_offers_usecase = providers.Factory(
        ListOffersUsecase,
        offers_repository=offers_repository,
        logger=logger_service,
    )

    get_offer_by_reference_usecase = providers.Factory(
        GetOfferByReferenceUsecase,
        offers_repository=offers_repository,
    )

    list_metiers_usecase = providers.Factory(
        ListMetiersUsecase,
        metiers_repository=metiers_repository,
        logger=logger_service,
    )

    archive_offer_by_reference_usecase = providers.Factory(
        ArchiveOfferByReferenceUsecase,
        offers_repository=offers_repository,
        vector_repository=vector_repository,
        user_source_repository=user_source_repository,
        utilisateur_repository=utilisateur_repository,
    )

    upsert_offers_usecase = providers.Factory(
        UpsertOffersUsecase,
        offers_repository=offers_repository,
        logger=logger_service,
        user_source_repository=user_source_repository,
        utilisateur_repository=utilisateur_repository,
    )

    upsert_organismes_usecase = providers.Factory(
        UpsertOrganismesUsecase,
        organisme_repository=organisme_repository,
        logger=logger_service,
    )

    list_sources_usecase = providers.Factory(
        ListSourcesUsecase,
        source_repository=source_repository,
    )

    get_offers_by_source_usecase = providers.Factory(
        GetOffersBySourceUsecase,
        offers_repository=offers_repository,
        user_source_repository=user_source_repository,
        utilisateur_repository=utilisateur_repository,
    )

    calculate_daily_stats_usecase = providers.Factory(
        CalculateDailyStatsUsecase,
        offer_stats_query_service=shared_container.offer_stats_query_service,
        stat_snapshot_writer=shared_container.stat_snapshot_writer,
    )
