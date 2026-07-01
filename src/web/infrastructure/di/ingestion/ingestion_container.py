from ddd.async_usecase_interface import IAsyncUseCase
from ddd.entity import Entity
from dependency_injector import containers, providers
from referentiel.types import IUpsertResult

from application.commons.usecases.calculate_daily_stats import (
    CalculateDailyStatsUseCase,
)
from application.ingestion.interfaces.load_documents_input import LoadDocumentsInput
from application.ingestion.usecases.archive_offer_by_reference import (
    ArchiveOfferByReferenceUseCase,
)
from application.ingestion.usecases.archive_offers import ArchiveOffersUsecase
from application.ingestion.usecases.clean_documents import CleanDocumentsUsecase
from application.ingestion.usecases.get_offers_by_source import (
    GetOffersBySourceUseCase,
)
from application.ingestion.usecases.list_metiers import ListMetiersUseCase
from application.ingestion.usecases.list_offers import ListOffersUseCase
from application.ingestion.usecases.list_sources import ListSourcesUseCase
from application.ingestion.usecases.load_documents import LoadDocumentsUsecase
from application.ingestion.usecases.load_offers import LoadOffersUsecase
from application.ingestion.usecases.upsert_offers import UpsertOffersUseCase
from application.ingestion.usecases.vectorize_documents import VectorizeDocumentsUsecase
from domain.ingestion.services.document_cleaner_interface import IDocumentCleaner
from infrastructure.external_gateways import (
    external_document_gateway,
    piste_client,
    talentsoft_client,
)
from infrastructure.gateways.ingestion import (
    load_documents_strategy_factory as load_strategy,
)
from infrastructure.gateways.ingestion.document_cleaner import DocumentCleaner
from infrastructure.gateways.ingestion.text_extractor import TextExtractor
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

    talentsoft_front_client = providers.Singleton(
        talentsoft_client.TalentsoftFrontClient,
        config=providers.Callable(lambda cfg: cfg.talentsoft, app_config),
        logger_service=logger_service,
    )

    talentsoft_back_client = providers.Singleton(
        talentsoft_client.TalentsoftBackClient,
        config=providers.Callable(lambda cfg: cfg.talentsoft_back, app_config),
        logger_service=logger_service,
    )

    document_gateway = providers.Singleton(
        external_document_gateway.ExternalDocumentGateway,
        piste_client=piste_client,
        talentsoft_front_client=talentsoft_front_client,
        talentsoft_back_client=talentsoft_back_client,
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
            offers_repository=offers_repository,
            metiers_repository=metiers_repository,
            source_repository=source_repository,
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
        IAsyncUseCase[LoadDocumentsInput, IUpsertResult]
    ] = providers.Factory(
        LoadDocumentsUsecase,
        strategy_factory=load_documents_strategy_factory,
        document_repository=document_repository,
        logger=logger_service,
    )

    load_offers_usecase: providers.Provider[
        IAsyncUseCase[LoadDocumentsInput, IUpsertResult]
    ] = providers.Factory(
        LoadOffersUsecase,
        document_repository=document_repository,
        document_gateway=document_gateway,
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

    archive_offers_usecase = providers.Factory(
        ArchiveOffersUsecase,
        offers_repository=offers_repository,
        document_gateway=document_gateway,
        vector_repository=vector_repository,
        logger=logger_service,
    )

    list_offers_usecase = providers.Factory(
        ListOffersUseCase,
        offers_repository=offers_repository,
        logger=logger_service,
    )

    list_metiers_usecase = providers.Factory(
        ListMetiersUseCase,
        metiers_repository=metiers_repository,
        logger=logger_service,
    )

    archive_offer_by_reference_usecase = providers.Factory(
        ArchiveOfferByReferenceUseCase,
        offers_repository=offers_repository,
        vector_repository=vector_repository,
        user_source_repository=user_source_repository,
        utilisateur_repository=utilisateur_repository,
    )

    upsert_offers_usecase = providers.Factory(
        UpsertOffersUseCase,
        offers_repository=offers_repository,
        logger=logger_service,
        user_source_repository=user_source_repository,
        utilisateur_repository=utilisateur_repository,
    )

    list_sources_usecase = providers.Factory(
        ListSourcesUseCase,
        source_repository=source_repository,
    )

    get_offers_by_source_usecase = providers.Factory(
        GetOffersBySourceUseCase,
        offers_repository=offers_repository,
        user_source_repository=user_source_repository,
        utilisateur_repository=utilisateur_repository,
    )

    calculate_daily_stats_usecase = providers.Factory(
        CalculateDailyStatsUseCase,
        offer_stats_query_service=offers_repository,
        stat_snapshot_writer=shared_container.stat_snapshot_writer,
    )
