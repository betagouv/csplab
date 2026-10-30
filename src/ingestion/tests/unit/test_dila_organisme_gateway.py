import json
from datetime import date

import pytest
from pytest_httpx import HTTPXMock

from domain.value_objects.organisme import OrganismeImportResource
from infrastructure.exceptions.exceptions import ExternalApiError
from infrastructure.external_gateways.dila_organisme_gateway import (
    DilaOrganismeGateway,
)

CSV_HEADER = "id;nom;categorie;hierarchie"

DILA_EXPORT_URL = (
    "https://api-lannuaire.service-public.fr/api/explore/v2.1/catalog/datasets/"
    "api-lannuaire-administration/exports/csv"
)


@pytest.fixture
def gateway() -> DilaOrganismeGateway:
    return DilaOrganismeGateway(export_url=DILA_EXPORT_URL)


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

    def test_reconstructs_ancestors_from_hierarchie(
        self, gateway: DilaOrganismeGateway, httpx_mock: HTTPXMock
    ):
        _mock_csv_response(
            httpx_mock,
            [
                _csv_row("root-id", "Ministère", "SI", _children("parent-id")),
                _csv_row("parent-id", "Direction", "SI", _children("child-id")),
                _csv_row("child-id", "Bureau", "SI", ""),
            ],
        )

        results = list(gateway.stream_organismes(_resource()))
        by_id = {r.external_id: r for r in results}

        assert by_id["root-id"].data["ancestors"] == []
        assert by_id["parent-id"].data["ancestors"] == ["root-id"]
        assert by_id["child-id"].data["ancestors"] == ["parent-id", "root-id"]

    def test_ignores_autre_hierarchie_links(
        self, gateway: DilaOrganismeGateway, httpx_mock: HTTPXMock
    ):
        hierarchie = json.dumps(
            [{"type_hierarchie": "Autre hiérarchie", "service": "child-id"}]
        )
        _mock_csv_response(
            httpx_mock,
            [
                _csv_row("other-id", "Autre", "SI", hierarchie),
                _csv_row("child-id", "Enfant", "SI", ""),
            ],
        )

        results = list(gateway.stream_organismes(_resource()))
        by_id = {r.external_id: r for r in results}

        assert by_id["child-id"].data["ancestors"] == []

    def test_ancestors_stop_on_cycles(
        self, gateway: DilaOrganismeGateway, httpx_mock: HTTPXMock
    ):
        _mock_csv_response(
            httpx_mock,
            [
                _csv_row("a-id", "A", "SI", _children("b-id")),
                _csv_row("b-id", "B", "SI", _children("a-id")),
            ],
        )

        results = list(gateway.stream_organismes(_resource()))
        by_id = {r.external_id: r for r in results}

        assert by_id["a-id"].data["ancestors"] == ["b-id"]
        assert by_id["b-id"].data["ancestors"] == ["a-id"]

    def test_ancestors_use_full_dataset_not_only_fpe(
        self, gateway: DilaOrganismeGateway, httpx_mock: HTTPXMock
    ):
        _mock_csv_response(
            httpx_mock,
            [
                _csv_row("parent-id", "Parent non-SI", "COL", _children("child-id")),
                _csv_row("child-id", "Enfant", "SI", ""),
            ],
        )

        results = list(gateway.stream_organismes(_resource()))

        assert results[0].external_id == "child-id"
        assert results[0].data["ancestors"] == ["parent-id"]

    def test_counts_fpe_homonyms_by_normalized_name(
        self, gateway: DilaOrganismeGateway, httpx_mock: HTTPXMock
    ):
        _mock_csv_response(
            httpx_mock,
            [
                _csv_row("sg-1", "Secrétariat général", "SI", ""),
                _csv_row("sg-2", "SECRETARIAT GENERAL", "SI", ""),
                _csv_row("sg-3", "Secrétariat général", "COL", ""),
                _csv_row("senat", "Sénat", "SI", ""),
            ],
        )

        results = list(gateway.stream_organismes(_resource()))
        by_id = {r.external_id: r for r in results}

        assert by_id["sg-1"].data["homonyms"] == 2
        assert by_id["sg-2"].data["homonyms"] == 2
        assert by_id["senat"].data["homonyms"] == 1

    def test_raises_on_http_error(
        self, gateway: DilaOrganismeGateway, httpx_mock: HTTPXMock
    ):
        httpx_mock.add_response(
            method="GET", url=DILA_EXPORT_URL_WITH_PARAMS, status_code=500
        )

        with pytest.raises(ExternalApiError, match="Erreur lors du téléchargement"):
            list(gateway.stream_organismes(_resource()))


def _children(*services: str) -> str:
    return json.dumps(
        [{"type_hierarchie": "Service Fils", "service": s} for s in services]
    )


def _resource() -> OrganismeImportResource:
    return OrganismeImportResource(url=DILA_EXPORT_URL, millesime=date.today())
