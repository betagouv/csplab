import httpx
from dependency_injector import containers, providers

from application.use_cases.archive_offer import ArchiveOfferUseCase
from application.use_cases.load_sources import LoadSourcesUseCase
from infrastructure.credentials_store import CredentialsStore
from infrastructure.sources_repository import SourcesRepository


def _build_credentials_store(credentials: list[tuple[str, str]]) -> CredentialsStore:
    store = CredentialsStore()
    for client_id, secret in credentials:
        store.register(client_id, secret)
    return store


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=["api.routes", "api.talentsoft"]
    )

    config = providers.Configuration()

    http_client = providers.Singleton(httpx.AsyncClient)

    sources_repository = providers.Singleton(SourcesRepository)

    credentials_store = providers.Singleton(
        _build_credentials_store,
        credentials=config.talentsoft_credentials,
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
        registry=sources_repository,
    )
