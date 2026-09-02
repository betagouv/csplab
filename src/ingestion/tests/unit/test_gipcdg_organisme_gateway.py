from datetime import date

import pytest
from pytest_httpx import HTTPXMock

from domain.value_objects.organisme import OrganismeImportResource
from infrastructure.exceptions.exceptions import ExternalApiError
from infrastructure.external_gateways.gipcdg_organisme_gateway import (
    GipcdgOrganismeGateway,
)

COLLECTIVITES_API_URL = "https://emploi-territorial.fr/api/cdg/collectivites?limit=1000"


@pytest.fixture
def gateway() -> GipcdgOrganismeGateway:
    return GipcdgOrganismeGateway(
        api_key="secret-token", collectivites_api_url=COLLECTIVITES_API_URL
    )


def _collectivite(id_col: int, rank: int, total: int, **extra) -> dict:
    return {"id_col": id_col, "_rank": rank, "_total": total, **extra}


class TestFindResource:
    def test_returns_fixed_url_and_today_millesime(
        self, gateway: GipcdgOrganismeGateway
    ):
        resource = gateway.find_resource()

        assert resource.url == COLLECTIVITES_API_URL
        assert resource.millesime == date.today()


class TestStreamOrganismes:
    def test_sends_api_key_header(
        self, gateway: GipcdgOrganismeGateway, httpx_mock: HTTPXMock
    ):
        httpx_mock.add_response(
            method="GET",
            url=f"{COLLECTIVITES_API_URL}&offset=0",
            json={"status": 200, "success": [_collectivite(1, 1, 1)]},
            match_headers={"X-API-Key": "secret-token"},
        )

        list(gateway.stream_organismes(_resource()))

    def test_yields_one_organisme_per_collectivite(
        self, gateway: GipcdgOrganismeGateway, httpx_mock: HTTPXMock
    ):
        httpx_mock.add_response(
            method="GET",
            url=f"{COLLECTIVITES_API_URL}&offset=0",
            json={
                "status": 200,
                "success": [_collectivite(1, 1, 2), _collectivite(2, 2, 2)],
            },
        )

        results = list(gateway.stream_organismes(_resource()))

        assert [r.external_id for r in results] == ["1", "2"]
        assert all(r.referentiel == "GIPCDG" for r in results)

    def test_skips_entries_without_id(
        self, gateway: GipcdgOrganismeGateway, httpx_mock: HTTPXMock
    ):
        httpx_mock.add_response(
            method="GET",
            url=f"{COLLECTIVITES_API_URL}&offset=0",
            json={
                "status": 200,
                "success": [{"_rank": 1, "_total": 2}, _collectivite(1, 2, 2)],
            },
        )

        results = list(gateway.stream_organismes(_resource()))

        assert [r.external_id for r in results] == ["1"]

    def test_data_contains_raw_payload(
        self, gateway: GipcdgOrganismeGateway, httpx_mock: HTTPXMock
    ):
        httpx_mock.add_response(
            method="GET",
            url=f"{COLLECTIVITES_API_URL}&offset=0",
            json={
                "status": 200,
                "success": [_collectivite(1, 1, 1, libl_col="Mairie")],
            },
        )

        results = list(gateway.stream_organismes(_resource()))

        assert results[0].data["libl_col"] == "Mairie"

    def test_fetches_next_page_using_offset_until_rank_reaches_total(
        self, gateway: GipcdgOrganismeGateway, httpx_mock: HTTPXMock
    ):
        httpx_mock.add_response(
            method="GET",
            url=f"{COLLECTIVITES_API_URL}&offset=0",
            json={
                "status": 200,
                "success": [_collectivite(1, 1, 3), _collectivite(2, 2, 3)],
            },
        )
        httpx_mock.add_response(
            method="GET",
            url=f"{COLLECTIVITES_API_URL}&offset=2",
            json={"status": 200, "success": [_collectivite(3, 3, 3)]},
        )

        results = list(gateway.stream_organismes(_resource()))

        assert [r.external_id for r in results] == ["1", "2", "3"]

    def test_stops_when_page_is_empty(
        self, gateway: GipcdgOrganismeGateway, httpx_mock: HTTPXMock
    ):
        httpx_mock.add_response(
            method="GET",
            url=f"{COLLECTIVITES_API_URL}&offset=0",
            json={"status": 200, "success": []},
        )

        results = list(gateway.stream_organismes(_resource()))

        assert results == []

    def test_raises_when_status_is_not_200(
        self, gateway: GipcdgOrganismeGateway, httpx_mock: HTTPXMock
    ):
        httpx_mock.add_response(
            method="GET",
            url=f"{COLLECTIVITES_API_URL}&offset=0",
            json={"status": 401, "status_message": "Invalid API Key"},
        )

        with pytest.raises(ExternalApiError, match="Réponse invalide"):
            list(gateway.stream_organismes(_resource()))

    def test_raises_on_http_error(
        self, gateway: GipcdgOrganismeGateway, httpx_mock: HTTPXMock
    ):
        httpx_mock.add_response(
            method="GET", url=f"{COLLECTIVITES_API_URL}&offset=0", status_code=500
        )

        with pytest.raises(ExternalApiError, match="Erreur lors de la récupération"):
            list(gateway.stream_organismes(_resource()))


def _resource() -> OrganismeImportResource:
    return OrganismeImportResource(
        url=COLLECTIVITES_API_URL, millesime=date(2026, 8, 20)
    )
