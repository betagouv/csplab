import httpx
from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject
from fastapi import Depends, Query

from application.interfaces.sources_repository import ISourcesRepository
from application.use_cases.archive_offer import ArchiveOfferUseCase
from application.use_cases.load_offer_details import LoadOfferDetailsUseCase
from application.use_cases.load_sources import LoadSourcesUseCase
from infrastructure.credentials_store import CredentialsStore
from infrastructure.sources_repository import SourcesRepository
from infrastructure.talentsoft_client_repository import TalentsoftClientRepository


def _build_credentials_store(
    credentials: list[tuple[str, str, str]],
) -> CredentialsStore:
    store = CredentialsStore()
    for client_id, secret, base_url in credentials:
        store.register(client_id, secret, base_url)
    return store


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

    talentsoft_client_repository = providers.Singleton(TalentsoftClientRepository)

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


@inject
def get_load_offer_details_use_case(
    client_id: str = Query(...),
    sources_repository: ISourcesRepository = Depends(
        Provide[Container.sources_repository]
    ),
    client_repository: TalentsoftClientRepository = Depends(
        Provide[Container.talentsoft_client_repository]
    ),
) -> LoadOfferDetailsUseCase | None:
    source = sources_repository.get_by_client_id_back(client_id)
    if source is None:
        return None
    client = client_repository.get(source.client_id_front)
    if client is None:
        return None
    return LoadOfferDetailsUseCase(talentsoft_client=client)
