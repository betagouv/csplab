from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest
from faker import Faker
from fastapi.testclient import TestClient

fake = Faker()

from api.main import create_app
from application.use_cases.archive_offer import ArchiveOfferUseCase
from application.use_cases.load_offer_details import LoadOfferDetailsUseCase
from application.use_cases.load_sources import LoadSourcesUseCase
from domain.source import Source
from infrastructure.sources_registry import SourcesRegistry
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

# --- App client fixtures ---


@pytest.fixture
def test_client(monkeypatch) -> TestClient:
    monkeypatch.setenv("TESTING", "true")
    monkeypatch.delenv("TALENTSOFT_BACK_CLIENT_ID", raising=False)
    monkeypatch.delenv("TALENTSOFT_BACK_CLIENT_SECRET", raising=False)
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

    # Pre-populate the sources registry (the lifespan doesn't run in test mode)
    app.state.container.sources_registry().load(
        [
            Source(
                source_id=SOURCE_ID,
                type="talentsoft",
                client_id_front="test_client_id_front",
                client_id_back=TALENTSOFT_BACK_CLIENT_ID,
                base_url_front=fake.url(),
                base_url_back=fake.url(),
            )
        ]
    )
    return TestClient(app)


# --- Use case fixtures ---


@pytest.fixture
def sources_registry() -> SourcesRegistry:
    return SourcesRegistry()


@pytest.fixture
def load_sources_use_case(sources_registry: SourcesRegistry) -> LoadSourcesUseCase:
    return LoadSourcesUseCase(
        client=httpx.AsyncClient(),
        web_base_url=WEB_BASE_URL,
        web_api_key=WEB_API_KEY,
        registry=sources_registry,
    )


@pytest.fixture
def archive_offer_use_case() -> ArchiveOfferUseCase:
    return ArchiveOfferUseCase(
        client=httpx.AsyncClient(),
        web_base_url=WEB_BASE_URL,
        web_api_key=WEB_API_KEY,
    )


@pytest.fixture
def talentsoft_mock_client():
    client = MagicMock()
    client.get_detail = AsyncMock()
    return client


@pytest.fixture
def load_offer_details_use_case(talentsoft_mock_client) -> LoadOfferDetailsUseCase:
    return LoadOfferDetailsUseCase(talentsoft_client=talentsoft_mock_client)
