import gzip
import json
from datetime import date

import pytest
from pytest_httpx import HTTPXMock

from domain.value_objects.organisme import OrganismeImportResource
from infrastructure.exceptions.exceptions import ExternalApiError
from infrastructure.external_gateways.finess_organisme_gateway import (
    DATASET_API_URL,
    FinessOrganismeGateway,
)


@pytest.fixture
def gateway() -> FinessOrganismeGateway:
    return FinessOrganismeGateway()


def _dataset_response(*titles_and_urls: tuple[str, str]) -> dict:
    return {
        "resources": [{"title": title, "url": url} for title, url in titles_and_urls]
    }


def _gzipped_structures(pmej: list[dict]) -> bytes:
    return gzip.compress(json.dumps({"pmej": pmej}).encode())


def _ege(numero_finess: str, **extra) -> dict:
    return {
        "informationsGeneralesEGE": {"numFinessEge": numero_finess, **extra},
    }


class TestFindResource:
    def test_picks_latest_daily_file(self, gateway, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            method="GET",
            url=DATASET_API_URL,
            json=_dataset_response(
                ("finess-structures-journalier-20260101.json.gz", "https://x/1"),
                ("finess-structures-journalier-20260819.json.gz", "https://x/2"),
                ("finess-structures-journalier-20260615.json.gz", "https://x/3"),
            ),
        )

        resource = gateway.find_resource()

        assert resource.url == "https://x/2"
        assert resource.millesime == date(2026, 8, 19)

    def test_ignores_non_matching_titles(self, gateway, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            method="GET",
            url=DATASET_API_URL,
            json=_dataset_response(
                ("finess-structures-annuel-2026.json.gz", "https://x/annual"),
                ("finess-structures-journalier-20260701.json.gz", "https://x/daily"),
            ),
        )

        resource = gateway.find_resource()

        assert resource.url == "https://x/daily"

    def test_raises_when_no_daily_file_found(self, gateway, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            method="GET", url=DATASET_API_URL, json=_dataset_response()
        )

        with pytest.raises(ExternalApiError, match="Aucun fichier"):
            gateway.find_resource()

    def test_raises_on_http_error(self, gateway, httpx_mock: HTTPXMock):
        httpx_mock.add_response(method="GET", url=DATASET_API_URL, status_code=500)

        with pytest.raises(ExternalApiError, match="Impossible de récupérer"):
            gateway.find_resource()


class TestStreamOrganismes:
    def test_yields_one_organisme_per_ege(self, gateway, httpx_mock: HTTPXMock):
        content = _gzipped_structures(
            [
                {"ege": [_ege("123456789"), _ege("987654321")]},
                {"ege": [_ege("111111111")]},
            ]
        )
        httpx_mock.add_response(method="GET", url="https://x/daily", content=content)
        resource = _resource("https://x/daily")

        results = list(gateway.stream_organismes(resource))

        assert [r.external_id for r in results] == [
            "123456789",
            "987654321",
            "111111111",
        ]
        assert all(r.referentiel == "FINESS" for r in results)

    def test_skips_ege_without_numero_finess(self, gateway, httpx_mock: HTTPXMock):
        content = _gzipped_structures(
            [{"ege": [{"informationsGeneralesEGE": {}}, _ege("123456789")]}]
        )
        httpx_mock.add_response(method="GET", url="https://x/daily", content=content)
        resource = _resource("https://x/daily")

        results = list(gateway.stream_organismes(resource))

        assert [r.external_id for r in results] == ["123456789"]

    def test_pmej_without_ege_yields_nothing(self, gateway, httpx_mock: HTTPXMock):
        content = _gzipped_structures([{}])
        httpx_mock.add_response(method="GET", url="https://x/daily", content=content)
        resource = _resource("https://x/daily")

        results = list(gateway.stream_organismes(resource))

        assert results == []

    def test_data_contains_raw_ege_payload(self, gateway, httpx_mock: HTTPXMock):
        content = _gzipped_structures(
            [{"ege": [_ege("123456789", nomEgeLong="Hôpital Test")]}]
        )
        httpx_mock.add_response(method="GET", url="https://x/daily", content=content)
        resource = _resource("https://x/daily")

        results = list(gateway.stream_organismes(resource))

        assert (
            results[0].data["informationsGeneralesEGE"]["nomEgeLong"] == "Hôpital Test"
        )

    def test_raises_on_http_error(self, gateway, httpx_mock: HTTPXMock):
        httpx_mock.add_response(method="GET", url="https://x/daily", status_code=500)
        resource = _resource("https://x/daily")

        with pytest.raises(ExternalApiError, match="Erreur lors du téléchargement"):
            list(gateway.stream_organismes(resource))


def _resource(url: str) -> OrganismeImportResource:
    return OrganismeImportResource(url=url, millesime=date(2026, 8, 19))
