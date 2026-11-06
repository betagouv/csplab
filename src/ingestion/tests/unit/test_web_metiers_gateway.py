import httpx
import pytest
from pytest_httpx import HTTPXMock

from infrastructure.external_gateways.base_web_gateway import WebGatewayCredentials
from infrastructure.external_gateways.web_metiers_gateway import WebMetiersGateway
from tests.conftest import METIERS_URL, WEB_API_KEY, WEB_BASE_URL


def _metier(code: str, domain: str) -> dict:
    return {"code_emploi_csp": code, "domaine_fonctionnel_code": domain}


def _page(results: list[dict], next_url: str | None) -> dict:
    return {"count": 0, "next": next_url, "previous": None, "results": results}


@pytest.fixture
def gateway() -> WebMetiersGateway:
    return WebMetiersGateway(
        client=httpx.AsyncClient(),
        credentials=WebGatewayCredentials(base_url=WEB_BASE_URL, api_key=WEB_API_KEY),
    )


@pytest.mark.asyncio
async def test_fetch_returns_codes_with_several_domains_across_pages(
    gateway, httpx_mock: HTTPXMock
):
    httpx_mock.add_response(
        url=f"{METIERS_URL}?taille=1000&page=1",
        json=_page(
            [
                _metier("ERJUS008", "JUS"),
                _metier("ERSEC031", "SEC"),
                _metier("ERSEC031", "SEC"),
                _metier("ERTRA007", "TRA"),
            ],
            next_url=f"{METIERS_URL}?page=2&taille=1000",
        ),
    )
    httpx_mock.add_response(
        url=f"{METIERS_URL}?taille=1000&page=2",
        json=_page(
            [_metier("ERJUS008", "CTL"), _metier("ERTRA007", "SEC")], next_url=None
        ),
    )

    codes = await gateway.fetch_metiers_multi_domaines()

    assert codes == {"ERJUS008", "ERTRA007"}


@pytest.mark.asyncio
async def test_fetch_sends_api_key_header(gateway, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url=f"{METIERS_URL}?taille=1000&page=1", json=_page([], next_url=None)
    )

    await gateway.fetch_metiers_multi_domaines()

    request = httpx_mock.get_requests()[0]
    assert request.headers["authorization"] == f"Api-Key {WEB_API_KEY}"


@pytest.mark.asyncio
async def test_fetch_raises_on_http_error(gateway, httpx_mock: HTTPXMock):
    httpx_mock.add_response(url=f"{METIERS_URL}?taille=1000&page=1", status_code=401)

    with pytest.raises(httpx.HTTPStatusError):
        await gateway.fetch_metiers_multi_domaines()
