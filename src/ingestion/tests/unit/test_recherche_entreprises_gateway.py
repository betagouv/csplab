import pytest
from pytest_httpx import HTTPXMock

from infrastructure.external_gateways.recherche_entreprises_gateway import (
    RechercheEntreprisesGateway,
)

SEARCH_URL = "https://recherche-entreprises.api.gouv.fr/search"


@pytest.fixture
def gateway() -> RechercheEntreprisesGateway:
    return RechercheEntreprisesGateway(
        search_url=SEARCH_URL,
        max_calls_per_second=1000,
    )


def _payload(siret: str | None = "26060047300342") -> dict:
    return {"results": [{"siege": {"siret": siret}}]}


def test_returns_siret_from_first_result(
    gateway: RechercheEntreprisesGateway, httpx_mock: HTTPXMock
):
    httpx_mock.add_response(
        method="GET", url=f"{SEARCH_URL}?q=Minist%C3%A8re", json=_payload()
    )

    assert gateway.find_siret("Ministère") == "26060047300342"


def test_returns_none_when_no_results(
    gateway: RechercheEntreprisesGateway, httpx_mock: HTTPXMock
):
    httpx_mock.add_response(
        method="GET", url=f"{SEARCH_URL}?q=Inconnu", json={"results": []}
    )

    assert gateway.find_siret("Inconnu") is None


def test_returns_none_when_first_result_has_no_siret(
    gateway: RechercheEntreprisesGateway, httpx_mock: HTTPXMock
):
    httpx_mock.add_response(
        method="GET", url=f"{SEARCH_URL}?q=Minist%C3%A8re", json=_payload(siret=None)
    )

    assert gateway.find_siret("Ministère") is None


def test_returns_none_on_http_error(
    gateway: RechercheEntreprisesGateway, httpx_mock: HTTPXMock
):
    httpx_mock.add_response(
        method="GET", url=f"{SEARCH_URL}?q=Minist%C3%A8re", status_code=500
    )

    assert gateway.find_siret("Ministère") is None
