import logging

import httpx
from dependency_injector import containers, providers
from sqlalchemy import Engine

from api.config import get_settings
from application.pipelines.ingest_offer_pipeline import IngestOfferPipeline
from application.tasks.process_webhook import save_raw_offer_webhook
from application.usecases.archive_offer import ArchiveOfferUsecase
from application.usecases.batch_archive_offers import BatchArchiveOffersUsecase
from application.usecases.clean_raw_offer import CleanRawOfferUsecase
from application.usecases.clean_raw_organismes import CleanRawOrganismesUsecase
from application.usecases.import_offers import ImportOffersUsecase
from application.usecases.import_organismes import ImportOrganismesUsecase
from application.usecases.load_sources import LoadSourcesUsecase
from application.usecases.publish_offer import PublishOfferUsecase
from application.usecases.publish_organismes import PublishOrganismesUsecase
from application.usecases.save_raw_offer import SaveRawOfferUsecase
from application.usecases.save_webhook import SaveWebhookUsecase
from domain.gateways.archive_gateway import IArchiveGateway
from domain.gateways.offers_by_source_gateway import IOffersBySourceGateway
from domain.gateways.organisme_gateway import IOrganismeGateway
from domain.gateways.organismes_cleaner import IOrganismesCleaner
from domain.gateways.publish_offer_gateway import IPublishOfferGateway
from domain.gateways.publish_organismes_gateway import IPublishOrganismesGateway
from domain.gateways.sources_gateway import ISourcesGateway
from domain.repositories.raw_offer_repository import IRawOfferRepository
from domain.repositories.raw_organisme_repository import IRawOrganismeRepository
from domain.repositories.sources_repository import ISourcesRepository
from domain.repositories.webhook_repository import IWebhookRepository
from domain.value_objects.credentials import Credentials
from domain.value_objects.talentsoft_credential import TalentsoftCredential
from infrastructure.credentials_store import CredentialsStore
from infrastructure.database import make_engine
from infrastructure.external_gateways.base_web_gateway import WebGatewayCredentials
from infrastructure.external_gateways.finess_organisme_gateway import (
    FinessOrganismeGateway,
)
from infrastructure.external_gateways.gipcdg_organisme_gateway import (
    GipcdgOrganismeGateway,
)
from infrastructure.external_gateways.talentsoft_client import (
    TalentsoftConfig,
    TalentsoftFrontClient,
)
from infrastructure.external_gateways.web_archive_gateway import WebArchiveGateway
from infrastructure.external_gateways.web_offers_by_source_gateway import (
    WebOffersBySourceGateway,
)
from infrastructure.external_gateways.web_publish_offer_gateway import (
    WebPublishOfferGateway,
)
from infrastructure.external_gateways.web_publish_organismes_gateway import (
    WebPublishOrganismesGateway,
)
from infrastructure.external_gateways.web_sources_gateway import WebSourcesGateway
from infrastructure.gateways.offers_cleaner import OffersCleaner
from infrastructure.gateways.organismes_cleaner import OrganismesCleaner
from infrastructure.raw_offer_repository import RawOfferRepository
from infrastructure.raw_organisme_repository import RawOrganismeRepository
from infrastructure.sources_repository import SourcesRepository
from infrastructure.talentsoft_client_repository import TalentsoftClientRepository
from infrastructure.webhook_repository import WebhookRepository


def _dispatch_save_raw_offer_webhook(webhook_id: str) -> None:
    save_raw_offer_webhook.delay(webhook_id)


def _build_credentials_store(
    credentials: list[TalentsoftCredential],
) -> CredentialsStore:
    seen_client_ids = {credential.client_id for credential in credentials}
    if len(seen_client_ids) != len(credentials):
        raise ValueError("Duplicate client_id found in TALENTSOFT_CREDENTIALS")

    store = CredentialsStore()
    for credential in credentials:
        store.register(
            Credentials(
                client_id=credential.client_id,
                client_secret=credential.client_secret,
                base_url=credential.base_url,
            )
        )
    return store


def _make_db_engine(database_url: str | None) -> Engine:
    if not database_url:
        raise ValueError("DATABASE_URL is required")
    return make_engine(database_url)


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=["api.routes", "api.talentsoft", "infrastructure.di.container"]
    )

    config = providers.Configuration()

    http_client = providers.Factory(httpx.AsyncClient)

    web_gateway_credentials = providers.Singleton(
        WebGatewayCredentials,
        base_url=config.web_base_url,
        api_key=config.web_api_key,
    )

    sources_repository: providers.Provider[ISourcesRepository] = providers.Singleton(
        SourcesRepository
    )

    credentials_store = providers.Singleton(
        _build_credentials_store,
        credentials=config.talentsoft_credentials,
    )

    db_engine = providers.Singleton(
        _make_db_engine,
        database_url=config.database_url,
    )

    talentsoft_client_repository = providers.Singleton(TalentsoftClientRepository)

    raw_offer_repository: providers.Provider[IRawOfferRepository] = providers.Singleton(
        RawOfferRepository,
        engine=db_engine,
    )

    raw_organisme_repository: providers.Provider[IRawOrganismeRepository] = (
        providers.Singleton(
            RawOrganismeRepository,
            engine=db_engine,
        )
    )

    organisme_gateway: providers.Provider[IOrganismeGateway] = providers.Singleton(
        FinessOrganismeGateway
    )

    import_organismes_usecase: providers.Provider[ImportOrganismesUsecase] = (
        providers.Factory(
            ImportOrganismesUsecase,
            organisme_gateway=organisme_gateway,
            raw_organisme_repository=raw_organisme_repository,
        )
    )

    gipcdg_organisme_gateway: providers.Provider[IOrganismeGateway] = (
        providers.Singleton(
            GipcdgOrganismeGateway,
            api_key=config.gipcdg_api_key,
            collectivites_api_url=config.gipcdg_collectivites_api_url,
        )
    )

    import_organismes_gipcdg_usecase: providers.Provider[ImportOrganismesUsecase] = (
        providers.Factory(
            ImportOrganismesUsecase,
            organisme_gateway=gipcdg_organisme_gateway,
            raw_organisme_repository=raw_organisme_repository,
        )
    )

    organismes_cleaner: providers.Provider[IOrganismesCleaner] = providers.Singleton(
        OrganismesCleaner
    )

    clean_raw_organismes_usecase: providers.Provider[CleanRawOrganismesUsecase] = (
        providers.Factory(
            CleanRawOrganismesUsecase,
            organismes_cleaner=organismes_cleaner,
            raw_organisme_repository=raw_organisme_repository,
        )
    )

    publish_organismes_gateway: providers.Provider[IPublishOrganismesGateway] = (
        providers.Factory(
            WebPublishOrganismesGateway,
            client=http_client,
            credentials=web_gateway_credentials,
        )
    )

    publish_organismes_usecase: providers.Provider[PublishOrganismesUsecase] = (
        providers.Factory(
            PublishOrganismesUsecase,
            publish_organismes_gateway=publish_organismes_gateway,
        )
    )

    webhook_repository: providers.Provider[IWebhookRepository] = providers.Singleton(
        WebhookRepository,
        engine=db_engine,
    )

    save_webhook_usecase: providers.Provider[SaveWebhookUsecase] = providers.Factory(
        SaveWebhookUsecase,
        repository=webhook_repository,
    )

    sources_gateway: providers.Provider[ISourcesGateway] = providers.Factory(
        WebSourcesGateway,
        client=http_client,
        credentials=web_gateway_credentials,
    )

    archive_gateway: providers.Provider[IArchiveGateway] = providers.Factory(
        WebArchiveGateway,
        client=http_client,
        credentials=web_gateway_credentials,
    )

    archive_offer_usecase: providers.Provider[ArchiveOfferUsecase] = providers.Factory(
        ArchiveOfferUsecase,
        archive_gateway=archive_gateway,
        raw_offer_repository=raw_offer_repository,
    )

    offers_by_source_gateway: providers.Provider[IOffersBySourceGateway] = (
        providers.Factory(
            WebOffersBySourceGateway,
            client=http_client,
            credentials=web_gateway_credentials,
        )
    )

    archive_offers_usecase: providers.Provider[BatchArchiveOffersUsecase] = (
        providers.Factory(
            BatchArchiveOffersUsecase,
            web_offers_gateway=offers_by_source_gateway,
            sources_repository=sources_repository,
            talentsoft_client_repository=talentsoft_client_repository,
            archive_offer_usecase=archive_offer_usecase,
        )
    )

    load_sources_usecase = providers.Factory(
        LoadSourcesUsecase,
        sources_gateway=sources_gateway,
        repository=sources_repository,
    )

    offers_cleaner = providers.Singleton(OffersCleaner)

    clean_raw_offer_usecase = providers.Factory(
        CleanRawOfferUsecase,
        offers_cleaner=offers_cleaner,
    )

    publish_offer_gateway: providers.Provider[IPublishOfferGateway] = providers.Factory(
        WebPublishOfferGateway,
        client=http_client,
        credentials=web_gateway_credentials,
    )

    publish_offer_usecase: providers.Provider[PublishOfferUsecase] = providers.Factory(
        PublishOfferUsecase,
        publish_offer_gateway=publish_offer_gateway,
    )

    save_raw_offer_usecase: providers.Provider[SaveRawOfferUsecase] = providers.Factory(
        SaveRawOfferUsecase,
        raw_offer_repository=raw_offer_repository,
    )

    ingest_offer_pipeline: providers.Provider[IngestOfferPipeline] = providers.Factory(
        IngestOfferPipeline,
        clean_raw_offer=clean_raw_offer_usecase,
        raw_offer_repository=raw_offer_repository,
        publish_offer=publish_offer_usecase,
    )

    dispatch_save_raw_offer_webhook = providers.Object(_dispatch_save_raw_offer_webhook)

    import_offers_usecase: providers.Provider[ImportOffersUsecase] = providers.Factory(
        ImportOffersUsecase,
        sources_repository=sources_repository,
        talentsoft_client_repository=talentsoft_client_repository,
        webhook_repository=webhook_repository,
        dispatch_process_webhook=dispatch_save_raw_offer_webhook,
    )


def create_container() -> Container:
    settings = get_settings()
    container = Container()
    container.config.web_base_url.from_value(settings.web_base_url)
    container.config.web_api_key.from_value(settings.web_api_key)
    container.config.database_url.from_value(settings.database_url)
    container.config.talentsoft_credentials.from_value(settings.talentsoft_credentials)
    container.config.gipcdg_api_key.from_value(settings.gipcdg_api_key)
    container.config.gipcdg_collectivites_api_url.from_value(
        str(settings.gipcdg_collectivites_api_url)
    )

    _logger = logging.getLogger(__name__)
    register_talentsoft_front_clients(
        container, settings.talentsoft_credentials, _logger
    )
    return container


def register_talentsoft_front_clients(
    container: Container,
    credentials: list[TalentsoftCredential],
    logger: logging.Logger,
) -> None:
    for credential in [c for c in credentials if c.role == "front"]:
        config = TalentsoftConfig(
            base_url=credential.base_url,
            client_id=credential.client_id,
            client_secret=credential.client_secret,
        )
        client = TalentsoftFrontClient(config=config, logger=logger)
        container.talentsoft_client_repository().register(credential.client_id, client)
