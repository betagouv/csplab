import httpx
import pytest
from pytest_httpx import HTTPXMock

from infrastructure.external_gateways.web_offers_by_source_gateway import (
    WebOffersBySourceGateway,
)
from tests.conftest import OFFERS_BY_SOURCE_URL as BASE_OFFERS_BY_SOURCE_URL
from tests.conftest import SOURCE_UUID
from tests.conftest import WEB_API_KEY as API_KEY
from tests.conftest import WEB_BASE_URL as BASE_URL

OFFERS_BY_SOURCE_URL = f"{BASE_OFFERS_BY_SOURCE_URL}/{SOURCE_UUID}"


def _page(references: list[str], next_url: str | None) -> dict:
    return {
        "count": len(references),
        "next": next_url,
        "previous": None,
        "results": [{"reference": r} for r in references],
    }


@pytest.fixture
def gateway() -> WebOffersBySourceGateway:
    return WebOffersBySourceGateway(
        client=httpx.AsyncClient(), base_url=BASE_URL, api_key=API_KEY
    )


@pytest.mark.asyncio
async def test_single_page_returns_references(gateway, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        method="GET",
        url=OFFERS_BY_SOURCE_URL,
        json=_page(["2026-111111", "2026-222222"], next_url=None),
    )

    result = await gateway.fetch_references(SOURCE_UUID)

    assert result == ["2026-111111", "2026-222222"]


@pytest.mark.asyncio
async def test_sends_api_key_header(gateway, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        method="GET", url=OFFERS_BY_SOURCE_URL, json=_page([], next_url=None)
    )

    await gateway.fetch_references(SOURCE_UUID)

    request = httpx_mock.get_requests()[0]
    assert request.headers["Authorization"] == f"Api-Key {API_KEY}"


@pytest.mark.asyncio
async def test_calls_correct_url(gateway, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        method="GET", url=OFFERS_BY_SOURCE_URL, json=_page([], next_url=None)
    )

    await gateway.fetch_references(SOURCE_UUID)

    assert str(httpx_mock.get_requests()[0].url) == OFFERS_BY_SOURCE_URL


@pytest.mark.asyncio
async def test_follows_next_url_for_pagination(gateway, httpx_mock: HTTPXMock):
    page2_url = f"{OFFERS_BY_SOURCE_URL}?page=2"
    httpx_mock.add_response(
        method="GET",
        url=OFFERS_BY_SOURCE_URL,
        json=_page(["2026-111111"], next_url=page2_url),
    )
    httpx_mock.add_response(
        method="GET",
        url=page2_url,
        json=_page(["2026-222222"], next_url=None),
    )

    result = await gateway.fetch_references(SOURCE_UUID)

    assert result == ["2026-111111", "2026-222222"]
    assert len(httpx_mock.get_requests()) == 2


@pytest.mark.asyncio
async def test_empty_results_returns_empty_list(gateway, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        method="GET", url=OFFERS_BY_SOURCE_URL, json=_page([], next_url=None)
    )

    result = await gateway.fetch_references(SOURCE_UUID)

    assert result == []


@pytest.mark.asyncio
async def test_raises_on_http_error(gateway, httpx_mock: HTTPXMock):
    httpx_mock.add_response(method="GET", url=OFFERS_BY_SOURCE_URL, status_code=401)

    with pytest.raises(httpx.HTTPStatusError):
        await gateway.fetch_references(SOURCE_UUID)
