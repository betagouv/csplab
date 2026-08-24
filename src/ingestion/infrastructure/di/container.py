import logging

import httpx
from dependency_injector import containers, providers
from pydantic import BaseModel, Field, HttpUrl
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
from application.usecases.publish_organismes import PublishOrganismesUseCase
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
from infrastructure.external_gateways.finess_organisme_gateway import (
    FinessOrganismeGateway,
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


class WebGatewayCredentials(BaseModel):
    base_url: HttpUrl
    api_key: str = Field(min_length=1)


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


def _make_sources_gateway(
    client: httpx.AsyncClient, base_url: str | None, api_key: str | None
) -> ISourcesGateway:
    creds = WebGatewayCredentials(base_url=base_url, api_key=api_key)
    return WebSourcesGateway(
        client=client, base_url=str(creds.base_url), api_key=creds.api_key
    )


def _make_archive_gateway(
    client: httpx.AsyncClient, base_url: str | None, api_key: str | None
) -> IArchiveGateway:
    creds = WebGatewayCredentials(base_url=base_url, api_key=api_key)
    return WebArchiveGateway(
        client=client, base_url=str(creds.base_url), api_key=creds.api_key
    )


def _make_offers_by_source_gateway(
    client: httpx.AsyncClient, base_url: str | None, api_key: str | None
) -> IOffersBySourceGateway:
    creds = WebGatewayCredentials(base_url=base_url, api_key=api_key)
    return WebOffersBySourceGateway(
        client=client, base_url=str(creds.base_url), api_key=creds.api_key
    )


def _make_publish_offer_gateway(
    client: httpx.AsyncClient, base_url: str | None, api_key: str | None
) -> IPublishOfferGateway:
    creds = WebGatewayCredentials(base_url=base_url, api_key=api_key)
    return WebPublishOfferGateway(
        client=client, base_url=str(creds.base_url), api_key=creds.api_key
    )


def _make_publish_organismes_gateway(
    client: httpx.AsyncClient, base_url: str | None, api_key: str | None
) -> IPublishOrganismesGateway:
    creds = WebGatewayCredentials(base_url=base_url, api_key=api_key)
    return WebPublishOrganismesGateway(
        client=client, base_url=str(creds.base_url), api_key=creds.api_key
    )


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=["api.routes", "api.talentsoft", "infrastructure.di.container"]
    )

    config = providers.Configuration()

    http_client = providers.Factory(httpx.AsyncClient)

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
            _make_publish_organismes_gateway,
            client=http_client,
            base_url=config.web_base_url,
            api_key=config.web_api_key,
        )
    )

    publish_organismes_use_case: providers.Provider[PublishOrganismesUseCase] = (
        providers.Factory(
            PublishOrganismesUseCase,
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
        _make_sources_gateway,
        client=http_client,
        base_url=config.web_base_url,
        api_key=config.web_api_key,
    )

    archive_gateway: providers.Provider[IArchiveGateway] = providers.Factory(
        _make_archive_gateway,
        client=http_client,
        base_url=config.web_base_url,
        api_key=config.web_api_key,
    )

    archive_offer_usecase: providers.Provider[ArchiveOfferUsecase] = providers.Factory(
        ArchiveOfferUsecase,
        archive_gateway=archive_gateway,
        raw_offer_repository=raw_offer_repository,
    )

    offers_by_source_gateway: providers.Provider[IOffersBySourceGateway] = (
        providers.Factory(
            _make_offers_by_source_gateway,
            client=http_client,
            base_url=config.web_base_url,
            api_key=config.web_api_key,
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
        _make_publish_offer_gateway,
        client=http_client,
        base_url=config.web_base_url,
        api_key=config.web_api_key,
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
