import httpx
from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject
from fastapi import Depends, Query
from sqlalchemy import Engine

from application.interfaces.raw_offer_repository import IRawOfferRepository
from application.interfaces.sources_repository import ISourcesRepository
from application.use_cases.archive_offer import ArchiveOfferUseCase
from application.use_cases.load_sources import LoadSourcesUseCase
from application.use_cases.save_raw_offer import SaveRawOfferUseCase
from infrastructure.credentials_store import CredentialsStore
from infrastructure.database import make_engine
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

    sources_repository = providers.Singleton(SourcesRepository)

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

    archive_offer_use_case = providers.Factory(
        ArchiveOfferUseCase,
        client=http_client,
        web_base_url=config.web_base_url,
        web_api_key=config.web_api_key,
    )

    load_sources_use_case = providers.Factory(
        LoadSourcesUseCase,
        client=http_client,
        web_base_url=config.web_base_url,
        web_api_key=config.web_api_key,
        repository=sources_repository,
    )


@inject
def get_save_raw_offer_use_case(
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
) -> SaveRawOfferUseCase | None:
    if raw_offer_repository is None:
        return None
    source = sources_repository.get_by_client_id_back(client_id)
    if source is None:
        return None
    client = client_repository.get(source.client_id_front)
    if client is None:
        return None
    return SaveRawOfferUseCase(
        talentsoft_client=client,
        raw_offer_repository=raw_offer_repository,
    )
