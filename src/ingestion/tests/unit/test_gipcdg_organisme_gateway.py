from datetime import date

import pytest
from pytest_httpx import HTTPXMock

from domain.value_objects.organisme import OrganismeImportResource
from infrastructure.exceptions.exceptions import ExternalApiError
from infrastructure.external_gateways.gipcdg_organisme_gateway import (
    GipcdgOrganismeGateway,
)

COLLECTIVITES_API_URL = (
    "https://emploi-territorial.fr/api/cdg/collectivites?etab=5&limit=1000"
)


@pytest.fixture
def gateway() -> GipcdgOrganismeGateway:
    return GipcdgOrganismeGateway(
        api_key="secret-token", collectivites_api_url=COLLECTIVITES_API_URL
    )


def _collectivite(id_col: int, **extra) -> dict:
    return {"id_col": id_col, **extra}


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
            url=COLLECTIVITES_API_URL,
            json={"status": 200, "success": [_collectivite(1)]},
            match_headers={"X-API-Key": "secret-token"},
        )

        list(gateway.stream_organismes(_resource()))

    def test_yields_one_organisme_per_collectivite(
        self, gateway: GipcdgOrganismeGateway, httpx_mock: HTTPXMock
    ):
        httpx_mock.add_response(
            method="GET",
            url=COLLECTIVITES_API_URL,
            json={
                "status": 200,
                "success": [_collectivite(1), _collectivite(2)],
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
            url=COLLECTIVITES_API_URL,
            json={"status": 200, "success": [{"libc_col": "no id"}, _collectivite(1)]},
        )

        results = list(gateway.stream_organismes(_resource()))

        assert [r.external_id for r in results] == ["1"]

    def test_data_contains_raw_payload(
        self, gateway: GipcdgOrganismeGateway, httpx_mock: HTTPXMock
    ):
        httpx_mock.add_response(
            method="GET",
            url=COLLECTIVITES_API_URL,
            json={"status": 200, "success": [_collectivite(1, libl_col="Mairie")]},
        )

        results = list(gateway.stream_organismes(_resource()))

        assert results[0].data["libl_col"] == "Mairie"

    def test_raises_when_status_is_not_200(
        self, gateway: GipcdgOrganismeGateway, httpx_mock: HTTPXMock
    ):
        httpx_mock.add_response(
            method="GET",
            url=COLLECTIVITES_API_URL,
            json={"status": 401, "status_message": "Invalid API Key"},
        )

        with pytest.raises(ExternalApiError, match="Réponse invalide"):
            list(gateway.stream_organismes(_resource()))

    def test_raises_on_http_error(
        self, gateway: GipcdgOrganismeGateway, httpx_mock: HTTPXMock
    ):
        httpx_mock.add_response(
            method="GET", url=COLLECTIVITES_API_URL, status_code=500
        )

        with pytest.raises(ExternalApiError, match="Erreur lors de la récupération"):
            list(gateway.stream_organismes(_resource()))


def _resource() -> OrganismeImportResource:
    return OrganismeImportResource(
        url=COLLECTIVITES_API_URL, millesime=date(2026, 8, 20)
    )
