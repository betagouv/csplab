import pytest
from pytest_httpx import HTTPXMock

from application.usecases.load_sources import LoadSourcesUsecase
from tests.conftest import SOURCES_URL
from tests.shared_fixtures import WEB_API_KEY


@pytest.mark.asyncio
async def test_execute_sends_api_key_header(
    load_sources_usecase: LoadSourcesUsecase, httpx_mock: HTTPXMock
):
    httpx_mock.add_response(method="GET", url=SOURCES_URL, json=[], status_code=200)

    await load_sources_usecase.execute()

    requests = httpx_mock.get_requests()
    assert len(requests) == 1
    assert requests[0].headers["authorization"] == f"Api-Key {WEB_API_KEY}"
