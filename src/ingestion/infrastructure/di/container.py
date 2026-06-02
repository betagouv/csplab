import logging

import httpx
from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject
from fastapi import Depends, Query
from sqlalchemy import Engine

from application.pipelines.ingest_offer_pipeline import IngestOfferPipeline
from application.use_cases.archive_offer import ArchiveOfferUseCase
from application.use_cases.clean_raw_offer import CleanRawOfferUseCase
from application.use_cases.load_sources import LoadSourcesUseCase
from application.use_cases.save_raw_offer import SaveRawOfferUseCase
from domain.gateways.archive_gateway import IArchiveGateway
from domain.gateways.sources_gateway import ISourcesGateway
from domain.repositories.raw_offer_repository import IRawOfferRepository
from domain.repositories.sources_repository import ISourcesRepository
from infrastructure.credentials_store import CredentialsStore
from infrastructure.database import make_engine, run_migrations
from infrastructure.external_gateways.talentsoft_client import (
    TalentsoftConfig,
    TalentsoftFrontClient,
)
from infrastructure.external_gateways.web_archive_gateway import WebArchiveGateway
from infrastructure.external_gateways.web_sources_gateway import WebSourcesGateway
from infrastructure.gateways.offers_cleaner import OffersCleaner
from infrastructure.raw_offer_repository import RawOfferRepository
from infrastructure.sources_repository import SourcesRepository
from infrastructure.talentsoft_client_repository import TalentsoftClientRepository


def _build_credentials_store(
    credentials: list[tuple[str, str, str]],
) -> CredentialsStore:
    store = CredentialsStore()
    for client_id, client_secret, base_url in credentials:
        store.register(client_id, client_secret, base_url)
    return store


def _make_db_engine(database_url: str | None) -> Engine | None:
    if not database_url:
        return None
    return make_engine(database_url)


def _make_sources_repository() -> ISourcesRepository:
    return SourcesRepository()


def _make_sources_gateway(
    client: httpx.AsyncClient, base_url: str | None, api_key: str | None
) -> ISourcesGateway | None:
    if not base_url or not api_key:
        return None
    return WebSourcesGateway(client=client, base_url=base_url, api_key=api_key)


def _make_archive_gateway(
    client: httpx.AsyncClient, base_url: str | None, api_key: str | None
) -> IArchiveGateway | None:
    if not base_url or not api_key:
        return None
    return WebArchiveGateway(client=client, base_url=base_url, api_key=api_key)


def _make_archive_use_case(
    archive_gateway: IArchiveGateway | None,
) -> ArchiveOfferUseCase | None:
    if archive_gateway is None:
        return None
    return ArchiveOfferUseCase(archive_gateway=archive_gateway)


def _make_raw_offer_repository(engine: Engine | None) -> IRawOfferRepository | None:
    if engine is None:
        return None
    return RawOfferRepository(engine=engine)


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=["api.routes", "api.talentsoft", "infrastructure.di.container"]
    )

    config = providers.Configuration()

    http_client = providers.Singleton(httpx.AsyncClient)

    sources_repository: providers.Provider[ISourcesRepository] = providers.Singleton(
        _make_sources_repository
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

    raw_offer_repository: providers.Provider[IRawOfferRepository | None] = (
        providers.Singleton(
            _make_raw_offer_repository,
            engine=db_engine,
        )
    )

    sources_gateway: providers.Provider[ISourcesGateway | None] = providers.Factory(
        _make_sources_gateway,
        client=http_client,
        base_url=config.web_base_url,
        api_key=config.web_api_key,
    )

    archive_gateway: providers.Provider[IArchiveGateway | None] = providers.Factory(
        _make_archive_gateway,
        client=http_client,
        base_url=config.web_base_url,
        api_key=config.web_api_key,
    )

    archive_offer_use_case: providers.Provider[ArchiveOfferUseCase | None] = (
        providers.Factory(
            _make_archive_use_case,
            archive_gateway=archive_gateway,
        )
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


def run_database_migrations(database_url: str) -> None:
    run_migrations(database_url)


def register_talentsoft_front_client(
    container: Container, client_id: str, logger: logging.Logger
) -> None:
    creds = container.credentials_store().get_credentials(client_id)
    if not creds:
        return
    config = TalentsoftConfig(
        base_url=creds.base_url,
        client_id=creds.client_id,
        client_secret=creds.client_secret,
    )
    client = TalentsoftFrontClient(config=config, logger=logger)
    container.talentsoft_client_repository().register(client_id, client)


@inject
def get_ingest_offer_pipeline(
    client_id: str = Query(...),
    sources_repository: ISourcesRepository = Depends(
        Provide[Container.sources_repository]
    ),
    client_repository: TalentsoftClientRepository = Depends(
        Provide[Container.talentsoft_client_repository]
    ),
    raw_offer_repository: IRawOfferRepository | None = Depends(
        Provide[Container.raw_offer_repository]
    ),
) -> IngestOfferPipeline | None:
    if raw_offer_repository is None:
        return None
    source = sources_repository.get_by_client_id_back(client_id)
    if source is None:
        return None
    client = client_repository.get(source.client_id_front)
    if client is None:
        return None
    save_use_case = SaveRawOfferUseCase(
        offers_gateway=client,
        raw_offer_repository=raw_offer_repository,
    )
    clean_use_case = CleanRawOfferUseCase(offers_cleaner=OffersCleaner())
    return IngestOfferPipeline(
        save_raw_offer=save_use_case,
        clean_raw_offer=clean_use_case,
        raw_offer_repository=raw_offer_repository,
    )
