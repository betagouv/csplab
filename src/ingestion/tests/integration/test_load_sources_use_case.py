import pytest
from faker import Faker
from pytest_httpx import HTTPXMock

from application.use_cases.load_sources import LoadSourcesUseCase
from infrastructure.sources_repository import SourcesRepository
from tests.conftest import SOURCES_URL

fake = Faker()

SOURCE_DATA = {
    "source_id": "aaaa-bbbb",
    "type": "talentsoft",
    "client_id_back": "client-back-1",
    "client_id_front": "client-front-1",
    "base_url_front": fake.url(),
    "base_url_back": fake.url(),
}


@pytest.mark.asyncio
async def test_execute_populates_registry(
    load_sources_use_case: LoadSourcesUseCase,
    sources_repository: SourcesRepository,
    httpx_mock: HTTPXMock,
):
    httpx_mock.add_response(
        method="GET", url=SOURCES_URL, json=[SOURCE_DATA], status_code=200
    )

    await load_sources_use_case.execute()

    source = sources_repository.get_by_client_id_back("client-back-1")
    assert source is not None
    assert source.source_id == "aaaa-bbbb"
    assert source.type == "talentsoft"
    assert len(sources_repository) == 1


@pytest.mark.asyncio
async def test_execute_with_empty_response_leaves_registry_empty(
    load_sources_use_case: LoadSourcesUseCase,
    sources_repository: SourcesRepository,
    httpx_mock: HTTPXMock,
):
    httpx_mock.add_response(method="GET", url=SOURCES_URL, json=[], status_code=200)

    await load_sources_use_case.execute()

    assert len(sources_repository) == 0
    assert sources_repository.get_by_client_id_back("any") is None


@pytest.mark.asyncio
async def test_execute_replaces_previous_registry_contents(
    load_sources_use_case: LoadSourcesUseCase,
    sources_repository: SourcesRepository,
    httpx_mock: HTTPXMock,
):
    first_source = {**SOURCE_DATA, "source_id": "first-id", "client_id_back": "back-1"}
    second_source = {
        **SOURCE_DATA,
        "source_id": "second-id",
        "client_id_back": "back-2",
    }

    httpx_mock.add_response(
        method="GET", url=SOURCES_URL, json=[first_source], status_code=200
    )
    await load_sources_use_case.execute()
    assert len(sources_repository) == 1

    httpx_mock.add_response(
        method="GET", url=SOURCES_URL, json=[second_source], status_code=200
    )
    await load_sources_use_case.execute()

    assert len(sources_repository) == 1
    assert sources_repository.get_by_client_id_back("back-1") is None
    assert sources_repository.get_by_client_id_back("back-2") is not None
