import httpx
import pytest
from pytest_httpx import HTTPXMock

from application.use_cases.archive_offer import ArchiveOfferUseCase

WEB_BASE_URL = "https://web.example.com"
WEB_API_KEY = "test-api-key"
REFERENCE = "2019-1234"


@pytest.fixture
def use_case(httpx_mock: HTTPXMock) -> ArchiveOfferUseCase:
    return ArchiveOfferUseCase(
        client=httpx.AsyncClient(),
        web_base_url=WEB_BASE_URL,
        web_api_key=WEB_API_KEY,
    )


@pytest.mark.asyncio
async def test_execute_posts_to_archive_endpoint(
    use_case: ArchiveOfferUseCase, httpx_mock: HTTPXMock
):
    httpx_mock.add_response(
        method="POST",
        url=f"{WEB_BASE_URL}/api/offers/{REFERENCE}/archive",
        status_code=200,
    )
    await use_case.execute(REFERENCE)

    requests = httpx_mock.get_requests()
    assert len(requests) == 1
    assert requests[0].url == httpx.URL(
        f"{WEB_BASE_URL}/api/offers/{REFERENCE}/archive"
    )
    assert requests[0].headers["authorization"] == f"Api-Key {WEB_API_KEY}"


@pytest.mark.asyncio
async def test_execute_raises_on_error_response(
    use_case: ArchiveOfferUseCase, httpx_mock: HTTPXMock
):
    httpx_mock.add_response(
        method="POST",
        url=f"{WEB_BASE_URL}/api/offers/{REFERENCE}/archive",
        status_code=500,
    )
    with pytest.raises(httpx.HTTPStatusError):
        await use_case.execute(REFERENCE)
