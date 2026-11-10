import pytest
from pytest_httpx import HTTPXMock

from domain.value_objects.siret_candidate import SiretCandidate
from infrastructure.exceptions.exceptions import ExternalApiError
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


def _url(query: str) -> str:
    return (
        f"{SEARCH_URL}?q={query}&per_page=5&etat_administratif=A"
        "&minimal=true&include=siege"
    )


def _result(
    *,
    siren: str = "110000072",
    nom_complet: str = "MINISTERE DU TRAVAIL",
    nature_juridique: str | None = "7113",
    siret: str | None = "11000007200014",
) -> dict:
    return {
        "siren": siren,
        "nom_complet": nom_complet,
        "nature_juridique": nature_juridique,
        "siege": {"siret": siret},
    }


def test_returns_candidates_with_nature_juridique(
    gateway: RechercheEntreprisesGateway, httpx_mock: HTTPXMock
):
    httpx_mock.add_response(
        method="GET",
        url=_url("Minist%C3%A8re"),
        json={
            "results": [
                _result(),
                _result(
                    siren="552081317",
                    nom_complet="ELECTRICITE DE FRANCE",
                    nature_juridique="5599",
                    siret="55208131766522",
                ),
            ]
        },
    )

    assert gateway.search("Ministère") == [
        SiretCandidate(
            siret="11000007200014",
            siren="110000072",
            denomination="MINISTERE DU TRAVAIL",
            nature_juridique="7113",
        ),
        SiretCandidate(
            siret="55208131766522",
            siren="552081317",
            denomination="ELECTRICITE DE FRANCE",
            nature_juridique="5599",
        ),
    ]


def test_returns_empty_list_when_no_results(
    gateway: RechercheEntreprisesGateway, httpx_mock: HTTPXMock
):
    httpx_mock.add_response(method="GET", url=_url("Inconnu"), json={"results": []})

    assert gateway.search("Inconnu") == []


def test_candidate_siret_is_none_without_siege(
    gateway: RechercheEntreprisesGateway, httpx_mock: HTTPXMock
):
    result = _result()
    del result["siege"]
    httpx_mock.add_response(
        method="GET", url=_url("11000007200014"), json={"results": [result]}
    )

    [candidate] = gateway.search("11000007200014")

    assert candidate.siret is None
    assert candidate.siren == "110000072"


def test_raises_on_http_error(
    gateway: RechercheEntreprisesGateway, httpx_mock: HTTPXMock
):
    httpx_mock.add_response(method="GET", url=_url("Minist%C3%A8re"), status_code=500)

    with pytest.raises(ExternalApiError):
        gateway.search("Ministère")
