import httpx
import pytest
from pytest_httpx import HTTPXMock

from application.interfaces.sources_registry import ISourcesRegistry
from application.use_cases.load_sources import LoadSourcesUseCase
from infrastructure.sources_registry import SourcesRegistry

WEB_BASE_URL = "https://web.example.com"
WEB_API_KEY = "test-api-key"
SOURCES_URL = f"{WEB_BASE_URL}/api/data/sources/"


@pytest.fixture
def registry() -> ISourcesRegistry:
    return SourcesRegistry()


@pytest.fixture
def use_case(registry: ISourcesRegistry) -> LoadSourcesUseCase:
    return LoadSourcesUseCase(
        client=httpx.AsyncClient(),
        web_base_url=WEB_BASE_URL,
        web_api_key=WEB_API_KEY,
        registry=registry,
    )


@pytest.mark.asyncio
async def test_execute_loads_sources_into_registry(
    use_case: LoadSourcesUseCase,
    registry: ISourcesRegistry,
    httpx_mock: HTTPXMock,
):
    sources = [
        {
            "source_id": "aaaa-bbbb",
            "type": "talentsoft",
            "client_id_back": "client-back-1",
            "client_id_front": "client-front-1",
            "base_url_front": "https://front.talentsoft.com",
            "base_url_back": "https://back.talentsoft.com",
        }
    ]
    httpx_mock.add_response(
        method="GET",
        url=SOURCES_URL,
        json=sources,
        status_code=200,
    )

    await use_case.execute()

    source = registry.get_by_client_id_back("client-back-1")
    assert source is not None
    assert source.source_id == "aaaa-bbbb"
    assert registry.get_by_client_id_back("unknown") is None
    assert len(registry) == 1


@pytest.mark.asyncio
async def test_execute_sends_api_key_header(
    use_case: LoadSourcesUseCase,
    httpx_mock: HTTPXMock,
):
    httpx_mock.add_response(method="GET", url=SOURCES_URL, json=[], status_code=200)

    await use_case.execute()

    requests = httpx_mock.get_requests()
    assert len(requests) == 1
    assert requests[0].headers["authorization"] == f"Api-Key {WEB_API_KEY}"


@pytest.mark.asyncio
async def test_execute_raises_on_error_response(
    use_case: LoadSourcesUseCase,
    httpx_mock: HTTPXMock,
):
    httpx_mock.add_response(method="GET", url=SOURCES_URL, status_code=500)

    with pytest.raises(httpx.HTTPStatusError):
        await use_case.execute()
