import httpx
from dependency_injector import containers, providers
from sqlalchemy import Engine

from application.interfaces.sources_repository import ISourcesRepository
from application.use_cases.archive_offer import ArchiveOfferUseCase
from application.use_cases.load_offer_details import LoadOfferDetailsUseCase
from application.use_cases.load_sources import LoadSourcesUseCase
from application.use_cases.save_raw_offer import SaveRawOfferUseCase
from infrastructure.database import make_engine
from infrastructure.external_gateways.talentsoft_client import TalentsoftFrontClient
from infrastructure.raw_offer_repository import RawOfferRepository
from infrastructure.credentials_store import CredentialsStore
from infrastructure.sources_repository import SourcesRepository


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


def _make_load_offer_details_use_case(
    talentsoft_client: TalentsoftFrontClient | None,
) -> LoadOfferDetailsUseCase | None:
    if talentsoft_client is None:
        return None
    return LoadOfferDetailsUseCase(talentsoft_client=talentsoft_client)


def _make_save_raw_offer_use_case(
    load_offer_details: LoadOfferDetailsUseCase | None,
    engine: Engine | None,
) -> SaveRawOfferUseCase | None:
    if load_offer_details is None or engine is None:
        return None
    return SaveRawOfferUseCase(
        load_offer_details=load_offer_details,
        raw_offer_repository=RawOfferRepository(engine=engine),
    )


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

    # Overridden in main.py lifespan once the client is created and cached on app.state
    talentsoft_front_client: providers.Provider[TalentsoftFrontClient | None] = (
        providers.Object(None)
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

    load_offer_details_use_case = providers.Factory(
        _make_load_offer_details_use_case,
        talentsoft_client=talentsoft_front_client,
    )

    save_raw_offer_use_case = providers.Factory(
        _make_save_raw_offer_use_case,
        load_offer_details=load_offer_details_use_case,
        engine=db_engine,
    )
