import logging
from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest
from dependency_injector import providers
from faker import Faker
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pytest_httpx import HTTPXMock
from sqlalchemy import text
from sqlmodel import Session

from api.config import get_settings
from api.main import create_app
from application.use_cases.archive_offer import ArchiveOfferUseCase
from application.use_cases.load_sources import LoadSourcesUseCase
from domain.value_objects.source import Source
from infrastructure.database import make_engine, run_migrations
from infrastructure.di.container import Container
from infrastructure.external_gateways.talentsoft_client import (
    TalentsoftConfig,
    TalentsoftFrontClient,
)
from infrastructure.external_gateways.web_sources_gateway import WebSourcesGateway
from infrastructure.raw_offer_repository import RawOfferRepository
from infrastructure.sources_repository import SourcesRepository
from tests.conftest import (
    SOURCE_ID,
    TALENTSOFT_BACK_BASE_URL,
    TALENTSOFT_BACK_CLIENT_ID,
    TALENTSOFT_BACK_CLIENT_SECRET,
    TALENTSOFT_FRONT_BASE_URL,
    TALENTSOFT_FRONT_CLIENT_ID,
    TALENTSOFT_FRONT_CLIENT_SECRET,
    WEB_API_KEY,
    WEB_BASE_URL,
)

fake = Faker()
_logger = logging.getLogger(__name__)


_logger = logging.getLogger(__name__)

TALENTSOFT_TOKEN_URL = f"{TALENTSOFT_FRONT_BASE_URL}/api/token"
TALENTSOFT_DETAIL_OFFER_URL = f"{TALENTSOFT_FRONT_BASE_URL}/api/v2/offers/getoffer"
WEB_PUBLISH_OFFER_URL = f"{WEB_BASE_URL}/api/v1/offres/creer_modifier/"


def mock_talentsoft_token_response(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        method="POST",
        url=TALENTSOFT_TOKEN_URL,
        json={
            "access_token": fake.uuid4(),
            "token_type": "Bearer",
            "expires_in": 3600,
        },
    )


def mock_web_publish_offer_response(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        method="POST",
        url=WEB_PUBLISH_OFFER_URL,
        json={"created": 1, "updated": 0, "errors": []},
        status_code=201,
    )


# --- Helpers ---


def setup_talentsoft_front_in_container(
    app: FastAPI,
    base_url: str,
    client_id: str,
    client_secret: str,
) -> MagicMock:
    container: Container = app.state.container

    ts_client = TalentsoftFrontClient(
        config=TalentsoftConfig(
            base_url=base_url,
            client_id=client_id,
            client_secret=client_secret,
        ),
        logger=_logger,
    )
    container.talentsoft_client_repository().register(client_id, ts_client)

    mock_repo = MagicMock()
    mock_repo.upsert = AsyncMock()
    mock_repo.mark_as_cleaned = AsyncMock()
    mock_repo.mark_as_upserted = AsyncMock()
    mock_repo.mark_as_archived = AsyncMock()
    container.raw_offer_repository.override(providers.Object(mock_repo))

    return mock_repo


# --- App client fixtures ---


@pytest.fixture
def test_client(monkeypatch) -> TestClient:
    monkeypatch.setenv("TESTING", "true")
    monkeypatch.delenv("TALENTSOFT_BACK_CLIENT_ID", raising=False)
    monkeypatch.delenv("TALENTSOFT_BACK_CLIENT_SECRET", raising=False)
    monkeypatch.delenv("TALENTSOFT_FRONT_CLIENT_ID", raising=False)
    monkeypatch.delenv("TALENTSOFT_FRONT_CLIENT_SECRET", raising=False)
    app = create_app()
    return TestClient(app)


@pytest.fixture
def talentsoft_client(monkeypatch) -> TestClient:
    monkeypatch.setenv("TESTING", "true")
    monkeypatch.setenv("TALENTSOFT_BACK_CLIENT_ID", TALENTSOFT_BACK_CLIENT_ID)
    monkeypatch.setenv("TALENTSOFT_BACK_CLIENT_SECRET", TALENTSOFT_BACK_CLIENT_SECRET)
    monkeypatch.setenv("TALENTSOFT_BACK_BASE_URL", TALENTSOFT_BACK_BASE_URL)
    monkeypatch.setenv("TALENTSOFT_FRONT_CLIENT_ID", TALENTSOFT_FRONT_CLIENT_ID)
    monkeypatch.setenv("TALENTSOFT_FRONT_CLIENT_SECRET", TALENTSOFT_FRONT_CLIENT_SECRET)
    monkeypatch.setenv("TALENTSOFT_FRONT_BASE_URL", TALENTSOFT_FRONT_BASE_URL)
    monkeypatch.setenv("WEB_BASE_URL", WEB_BASE_URL)
    monkeypatch.setenv("WEB_API_KEY", WEB_API_KEY)
    app = create_app()

    mock_repo = setup_talentsoft_front_in_container(
        app,
        base_url=TALENTSOFT_FRONT_BASE_URL,
        client_id=TALENTSOFT_FRONT_CLIENT_ID,
        client_secret=TALENTSOFT_FRONT_CLIENT_SECRET,
    )
    app.state.mock_raw_offer_repository = mock_repo

    # Pre-populate the sources registry (the lifespan doesn't run in test mode)
    app.state.container.sources_repository().load(
        [
            Source(
                source_id=SOURCE_ID,
                type="talentsoft",
                client_id_front=TALENTSOFT_FRONT_CLIENT_ID,
                client_id_back=TALENTSOFT_BACK_CLIENT_ID,
                base_url_front=fake.url(),
                base_url_back=fake.url(),
            )
        ]
    )
    return TestClient(app)


# --- Use case fixtures ---


@pytest.fixture
def sources_repository() -> SourcesRepository:
    return SourcesRepository()


@pytest.fixture
def load_sources_use_case(sources_repository: SourcesRepository) -> LoadSourcesUseCase:
    return LoadSourcesUseCase(
        sources_gateway=WebSourcesGateway(
            client=httpx.AsyncClient(),
            base_url=WEB_BASE_URL,
            api_key=WEB_API_KEY,
        ),
        repository=sources_repository,
    )


@pytest.fixture
def mock_raw_offer_repository() -> MagicMock:
    mock_repo = MagicMock()
    mock_repo.upsert = AsyncMock()
    mock_repo.mark_as_archived = AsyncMock()
    mock_repo.mark_as_cleaned = AsyncMock()
    return mock_repo


@pytest.fixture
def archive_offer_use_case(mock_raw_offer_repository: MagicMock) -> ArchiveOfferUseCase:
    container = Container()
    container.config.from_dict(
        {"web_base_url": WEB_BASE_URL, "web_api_key": WEB_API_KEY, "database_url": None}
    )
    container.raw_offer_repository.override(providers.Object(mock_raw_offer_repository))
    use_case = container.archive_offer_use_case()
    assert use_case is not None
    return use_case


@pytest.fixture
def talentsoft_mock_client():
    client = MagicMock()
    client.get_detail = AsyncMock()
    return client


# --- Database fixtures ---


@pytest.fixture(scope="module")
def db_engine():
    url = get_settings().database_url
    if not url:
        pytest.skip("DATABASE_URL not set")
    engine = make_engine(url)
    run_migrations(url)
    yield engine
    engine.dispose()


@pytest.fixture
def clean_db(db_engine):
    with Session(db_engine) as session:
        session.execute(text("TRUNCATE TABLE raw_offers"))
        session.commit()
    yield


@pytest.fixture
def repository(db_engine) -> RawOfferRepository:
    return RawOfferRepository(engine=db_engine)
