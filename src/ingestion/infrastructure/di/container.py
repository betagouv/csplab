import logging

import httpx
from dependency_injector import containers, providers
from sqlalchemy import Engine

from api.config import get_settings
from application.pipelines.ingest_offer_pipeline import IngestOfferPipeline
from application.use_cases.archive_offer import ArchiveOfferUseCase
from application.use_cases.clean_raw_offer import CleanRawOfferUseCase
from application.use_cases.load_sources import LoadSourcesUseCase
from application.use_cases.publish_offer import PublishOfferUseCase
from application.use_cases.save_raw_offer import SaveRawOfferUseCase
from application.use_cases.save_webhook import SaveWebhookUseCase
from domain.gateways.archive_gateway import IArchiveGateway
from domain.gateways.publish_offer_gateway import IPublishOfferGateway
from domain.gateways.sources_gateway import ISourcesGateway
from domain.repositories.raw_offer_repository import IRawOfferRepository
from domain.repositories.sources_repository import ISourcesRepository
from domain.repositories.webhook_repository import IWebhookRepository
from infrastructure.credentials_store import CredentialsStore
from infrastructure.database import make_engine
from infrastructure.external_gateways.talentsoft_client import (
    TalentsoftConfig,
    TalentsoftFrontClient,
)
from infrastructure.external_gateways.web_archive_gateway import WebArchiveGateway
from infrastructure.external_gateways.web_publish_offer_gateway import (
    WebPublishOfferGateway,
)
from infrastructure.external_gateways.web_sources_gateway import WebSourcesGateway
from infrastructure.gateways.offers_cleaner import OffersCleaner
from infrastructure.raw_offer_repository import RawOfferRepository
from infrastructure.sources_repository import SourcesRepository
from infrastructure.talentsoft_client_repository import TalentsoftClientRepository
from infrastructure.webhook_repository import WebhookRepository


def _build_credentials_store(
    credentials: list[tuple[str, str, str]],
) -> CredentialsStore:
    store = CredentialsStore()
    for client_id, client_secret, base_url in credentials:
        store.register(client_id, client_secret, base_url)
    return store


def _make_db_engine(database_url: str | None) -> Engine:
    if not database_url:
        raise ValueError("DATABASE_URL is required")
    return make_engine(database_url)


def _make_sources_gateway(
    client: httpx.AsyncClient, base_url: str | None, api_key: str | None
) -> ISourcesGateway:
    if not base_url or not api_key:
        raise ValueError("WEB_BASE_URL and WEB_API_KEY are required")
    return WebSourcesGateway(client=client, base_url=base_url, api_key=api_key)


def _make_archive_gateway(
    client: httpx.AsyncClient, base_url: str | None, api_key: str | None
) -> IArchiveGateway:
    if not base_url or not api_key:
        raise ValueError("WEB_BASE_URL and WEB_API_KEY are required")
    return WebArchiveGateway(client=client, base_url=base_url, api_key=api_key)


def _make_publish_offer_gateway(
    client: httpx.AsyncClient, base_url: str | None, api_key: str | None
) -> IPublishOfferGateway:
    if not base_url or not api_key:
        raise ValueError("WEB_BASE_URL and WEB_API_KEY are required")
    return WebPublishOfferGateway(client=client, base_url=base_url, api_key=api_key)


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

    webhook_repository: providers.Provider[IWebhookRepository] = providers.Singleton(
        WebhookRepository,
        engine=db_engine,
    )

    save_webhook_use_case: providers.Provider[SaveWebhookUseCase] = providers.Factory(
        SaveWebhookUseCase,
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

    archive_offer_use_case: providers.Provider[ArchiveOfferUseCase] = providers.Factory(
        ArchiveOfferUseCase,
        archive_gateway=archive_gateway,
        raw_offer_repository=raw_offer_repository,
    )

    load_sources_use_case = providers.Factory(
        LoadSourcesUseCase,
        sources_gateway=sources_gateway,
        repository=sources_repository,
    )

    offers_cleaner = providers.Singleton(OffersCleaner)

    clean_raw_offer_use_case = providers.Factory(
        CleanRawOfferUseCase,
        offers_cleaner=offers_cleaner,
    )

    publish_offer_gateway: providers.Provider[IPublishOfferGateway] = providers.Factory(
        _make_publish_offer_gateway,
        client=http_client,
        base_url=config.web_base_url,
        api_key=config.web_api_key,
    )

    publish_offer_use_case: providers.Provider[PublishOfferUseCase] = providers.Factory(
        PublishOfferUseCase,
        publish_offer_gateway=publish_offer_gateway,
    )

    save_raw_offer_use_case: providers.Provider[SaveRawOfferUseCase] = (
        providers.Factory(
            SaveRawOfferUseCase,
            raw_offer_repository=raw_offer_repository,
        )
    )

    ingest_offer_pipeline: providers.Provider[IngestOfferPipeline] = providers.Factory(
        IngestOfferPipeline,
        clean_raw_offer=clean_raw_offer_use_case,
        raw_offer_repository=raw_offer_repository,
        publish_offer=publish_offer_use_case,
    )


def create_container() -> Container:
    settings = get_settings()
    container = Container()
    container.config.web_base_url.from_value(settings.web_base_url)
    container.config.web_api_key.from_value(settings.web_api_key)
    container.config.database_url.from_value(settings.database_url)
    container.config.talentsoft_credentials.from_value(
        [
            (client_id, secret, base_url)
            for client_id, secret, base_url in [
                (
                    settings.talentsoft_back_client_id,
                    settings.talentsoft_back_client_secret,
                    settings.talentsoft_back_base_url,
                ),
                (
                    settings.talentsoft_front_client_id,
                    settings.talentsoft_front_client_secret,
                    settings.talentsoft_front_base_url,
                ),
            ]
            if client_id and secret and base_url
        ]
    )
    if settings.talentsoft_front_client_id:
        _logger = logging.getLogger(__name__)
        register_talentsoft_front_client(
            container, settings.talentsoft_front_client_id, _logger
        )
    return container


def register_talentsoft_front_client(
    container: Container, client_id: str, logger: logging.Logger
) -> None:
    creds = container.credentials_store().get_credentials(client_id)
    if not creds:
        raise ValueError(f"No credentials found for TalentSoft client {client_id}")
    config = TalentsoftConfig(
        base_url=creds.base_url,
        client_id=creds.client_id,
        client_secret=creds.client_secret,
    )
    client = TalentsoftFrontClient(config=config, logger=logger)
    container.talentsoft_client_repository().register(client_id, client)
