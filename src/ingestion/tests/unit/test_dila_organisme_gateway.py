import json
from datetime import date

import pytest
from pytest_httpx import HTTPXMock

from domain.value_objects.organisme import OrganismeImportResource
from infrastructure.exceptions.exceptions import ExternalApiError
from infrastructure.external_gateways.dila_organisme_gateway import (
    DILA_EXPORT_URL,
    DilaOrganismeGateway,
)

CSV_HEADER = "id;nom;categorie;hierarchie"


@pytest.fixture
def gateway() -> DilaOrganismeGateway:
    return DilaOrganismeGateway()


def _csv_row(*values: str) -> str:
    return ";".join(values)


DILA_EXPORT_URL_WITH_PARAMS = (
    f"{DILA_EXPORT_URL}?lang=fr&timezone=Europe%2FParis&delimiter=%3B"
)


def _mock_csv_response(httpx_mock: HTTPXMock, rows: list[str]) -> None:
    body = "\n".join([CSV_HEADER, *rows])
    httpx_mock.add_response(method="GET", url=DILA_EXPORT_URL_WITH_PARAMS, text=body)


class TestFindResource:
    def test_returns_fixed_url_and_today_millesime(self, gateway: DilaOrganismeGateway):
        resource = gateway.find_resource()

        assert resource.url == DILA_EXPORT_URL
        assert resource.millesime == date.today()


class TestStreamOrganismes:
    def test_yields_only_fpe_categorie(
        self, gateway: DilaOrganismeGateway, httpx_mock: HTTPXMock
    ):
        _mock_csv_response(
            httpx_mock,
            [
                _csv_row("id-1", "Ministère 1", "SI", ""),
                _csv_row("id-2", "Mairie 1", "COL", ""),
            ],
        )

        results = list(gateway.stream_organismes(_resource()))

        assert [r.external_id for r in results] == ["id-1"]
        assert all(r.referentiel == "DILA" for r in results)

    def test_skips_rows_without_id(
        self, gateway: DilaOrganismeGateway, httpx_mock: HTTPXMock
    ):
        _mock_csv_response(
            httpx_mock,
            [
                _csv_row("", "Ministère 1", "SI", ""),
                _csv_row("id-2", "Ministère 2", "SI", ""),
            ],
        )

        results = list(gateway.stream_organismes(_resource()))

        assert [r.external_id for r in results] == ["id-2"]

    def test_reconstructs_parent_id_from_hierarchie(
        self, gateway: DilaOrganismeGateway, httpx_mock: HTTPXMock
    ):
        hierarchie = json.dumps(
            [{"type_hierarchie": "Service Fils", "service": "child-id"}]
        )
        _mock_csv_response(
            httpx_mock,
            [
                _csv_row("parent-id", "Parent", "SI", hierarchie),
                _csv_row("child-id", "Enfant", "SI", ""),
            ],
        )

        results = list(gateway.stream_organismes(_resource()))
        by_id = {r.external_id: r for r in results}

        assert by_id["parent-id"].data["parent_id"] == ""
        assert by_id["child-id"].data["parent_id"] == "parent-id"

    def test_parent_id_is_empty_string_when_no_parent(
        self, gateway: DilaOrganismeGateway, httpx_mock: HTTPXMock
    ):
        _mock_csv_response(httpx_mock, [_csv_row("id-1", "Ministère 1", "SI", "")])

        results = list(gateway.stream_organismes(_resource()))

        assert results[0].data["parent_id"] == ""

    def test_parent_lookup_uses_full_dataset_not_only_fpe(
        self, gateway: DilaOrganismeGateway, httpx_mock: HTTPXMock
    ):
        hierarchie = json.dumps(
            [{"type_hierarchie": "Service Fils", "service": "child-id"}]
        )
        _mock_csv_response(
            httpx_mock,
            [
                _csv_row("parent-id", "Parent non-SI", "COL", hierarchie),
                _csv_row("child-id", "Enfant", "SI", ""),
            ],
        )

        results = list(gateway.stream_organismes(_resource()))

        assert results[0].external_id == "child-id"
        assert results[0].data["parent_id"] == "parent-id"

    def test_raises_on_http_error(
        self, gateway: DilaOrganismeGateway, httpx_mock: HTTPXMock
    ):
        httpx_mock.add_response(
            method="GET", url=DILA_EXPORT_URL_WITH_PARAMS, status_code=500
        )

        with pytest.raises(ExternalApiError, match="Erreur lors du téléchargement"):
            list(gateway.stream_organismes(_resource()))


def _resource() -> OrganismeImportResource:
    return OrganismeImportResource(url=DILA_EXPORT_URL, millesime=date.today())
