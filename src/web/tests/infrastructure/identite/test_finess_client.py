import gzip
import json
from datetime import date

import pytest

from domain.identite.errors.organisme_errors import EtablissementInvalideError
from domain.identite.gateways.organisme_gateway_interface import (
    OrganismeImportResource,
)
from infrastructure.exceptions.exceptions import ExternalApiError
from infrastructure.external_gateways.finess_client import (
    DATASET_API_URL,
    FinessClient,
)
from infrastructure.gateways.shared.logger import LoggerService
from infrastructure.mappers.organisme_finess_mapper import OrganismeFinessMapper

LATITUDE = 46.211257
LONGITUDE = 5.254203

RESOURCE = OrganismeImportResource(
    url="https://static.data.gouv.fr/finess.json.gz",
    millesime=date(2026, 8, 18),
)


@pytest.fixture(name="finess_client")
def finess_client_fixture():
    return FinessClient(
        logger=LoggerService(), organisme_mapper=OrganismeFinessMapper()
    )


def _gzip_payload(pmej: list[dict]) -> bytes:
    return gzip.compress(json.dumps({"pmej": pmej}).encode())


def test_find_latest_journalier_picks_most_recent(httpx_mock, finess_client):
    httpx_mock.add_response(
        url=DATASET_API_URL,
        json={
            "resources": [
                {
                    "title": "finess-structures-mensuel-202607.json.gz",
                    "url": "https://static.data.gouv.fr/mensuel.json.gz",
                },
                {
                    "title": "finess-structures-journalier-20260817.json.gz",
                    "url": "https://static.data.gouv.fr/20260817.json.gz",
                },
                {
                    "title": "finess-structures-journalier-20260818.json.gz",
                    "url": "https://static.data.gouv.fr/20260818.json.gz",
                },
            ]
        },
    )

    resource = finess_client.find_latest_resource()

    assert resource.url == "https://static.data.gouv.fr/20260818.json.gz"
    assert resource.millesime.isoformat() == "2026-08-18"


def test_find_latest_journalier_raises_when_no_resource_matches(
    httpx_mock, finess_client
):
    httpx_mock.add_response(url=DATASET_API_URL, json={"resources": []})

    with pytest.raises(ExternalApiError):
        finess_client.find_latest_resource()


def test_find_latest_journalier_raises_on_http_error(httpx_mock, finess_client):
    httpx_mock.add_response(url=DATASET_API_URL, status_code=500)

    with pytest.raises(ExternalApiError):
        finess_client.find_latest_resource()


def test_stream_organismes_raises_on_http_error(httpx_mock, finess_client):
    httpx_mock.add_response(url=RESOURCE.url, status_code=500)

    with pytest.raises(ExternalApiError):
        list(finess_client.stream_organismes(RESOURCE))


def test_stream_organismes_yields_ege_with_siret(httpx_mock, finess_client):
    pmej = [
        {
            "ege": [
                {
                    "informationsGeneralesEGE": {
                        "nomEgeLong": "CLINIQUE DOCTEUR CONVERT",
                        "numFinessEge": "010780195",
                        "siret": "77220148900022",
                    },
                    "adresse": [
                        {
                            "cogCommune": "01053",
                            "coordonneesGeographique": {
                                "coordonneeX": "5.254203",
                                "coordonneeY": "46.211257",
                            },
                        }
                    ],
                },
                {
                    "informationsGeneralesEGE": {
                        "nomEgeLong": "SMUR SANS SIRET",
                        "numFinessEge": "010787190",
                        "siret": None,
                    },
                    "adresse": [],
                },
            ]
        }
    ]
    httpx_mock.add_response(url=RESOURCE.url, content=_gzip_payload(pmej))

    organismes = list(finess_client.stream_organismes(RESOURCE))

    assert len(organismes) == 1
    organisme = organismes[0]
    assert organisme.nom == "CLINIQUE DOCTEUR CONVERT"
    assert organisme.external_id == "010780195"
    assert organisme.siret.value == "77220148900022"
    assert organisme.millesime == "2026-08-18"
    assert organisme.localisation is not None
    assert organisme.localisation.latitude == LATITUDE
    assert organisme.localisation.longitude == LONGITUDE
    assert organisme.localisation.department.code == "01"


def test_stream_organismes_derives_dom_departement(httpx_mock, finess_client):
    pmej = [
        {
            "ege": [
                {
                    "informationsGeneralesEGE": {
                        "nomEgeLong": "CHU DE POINTE A PITRE",
                        "numFinessEge": "971000015",
                        "siret": "77220148900022",
                    },
                    "adresse": [{"cogCommune": "97120"}],
                }
            ]
        }
    ]
    httpx_mock.add_response(url=RESOURCE.url, content=_gzip_payload(pmej))

    (organisme,) = list(finess_client.stream_organismes(RESOURCE))

    assert organisme.localisation is not None
    assert organisme.localisation.department.code == "971"


def test_stream_organismes_raises_for_invalid_siret(httpx_mock, finess_client):
    pmej = [
        {
            "ege": [
                {
                    "informationsGeneralesEGE": {
                        "nomEgeLong": "ETABLISSEMENT SIRET INVALIDE",
                        "numFinessEge": "010780195",
                        "siret": "1234567890123",
                    },
                    "adresse": [],
                }
            ]
        }
    ]
    httpx_mock.add_response(url=RESOURCE.url, content=_gzip_payload(pmej))

    with pytest.raises(EtablissementInvalideError) as exc_info:
        list(finess_client.stream_organismes(RESOURCE))

    assert exc_info.value.external_id == "010780195"


def test_stream_organismes_without_adresse_has_no_localisation(
    httpx_mock, finess_client
):
    pmej = [
        {
            "ege": [
                {
                    "informationsGeneralesEGE": {
                        "nomEgeLong": "CLINIQUE SANS ADRESSE",
                        "numFinessEge": "010780195",
                        "siret": "77220148900022",
                    },
                    "adresse": [],
                }
            ]
        }
    ]
    httpx_mock.add_response(url=RESOURCE.url, content=_gzip_payload(pmej))

    (organisme,) = list(finess_client.stream_organismes(RESOURCE))

    assert organisme.localisation is None


def test_stream_organismes_handles_invalid_coordinates(httpx_mock, finess_client):
    pmej = [
        {
            "ege": [
                {
                    "informationsGeneralesEGE": {
                        "nomEgeLong": "CLINIQUE SANS COORDONNEES",
                        "numFinessEge": "010780195",
                        "siret": "77220148900022",
                    },
                    "adresse": [
                        {
                            "cogCommune": "01053",
                            "coordonneesGeographique": {
                                "coordonneeX": "abc",
                                "coordonneeY": "def",
                            },
                        }
                    ],
                }
            ]
        }
    ]
    httpx_mock.add_response(url=RESOURCE.url, content=_gzip_payload(pmej))

    (organisme,) = list(finess_client.stream_organismes(RESOURCE))

    assert organisme.localisation is not None
    assert organisme.localisation.latitude is None
    assert organisme.localisation.longitude is None


@pytest.mark.parametrize(
    "cog_commune",
    [
        "5",  # too short to be a commune code
        "97",  # DOM/TOM prefix without enough digits
    ],
)
def test_stream_organismes_handles_short_commune_codes(
    httpx_mock, finess_client, cog_commune
):
    pmej = [
        {
            "ege": [
                {
                    "informationsGeneralesEGE": {
                        "nomEgeLong": "ETABLISSEMENT COMMUNE INCOMPLETE",
                        "numFinessEge": "010780195",
                        "siret": "77220148900022",
                    },
                    "adresse": [{"cogCommune": cog_commune}],
                }
            ]
        }
    ]
    httpx_mock.add_response(url=RESOURCE.url, content=_gzip_payload(pmej))

    (organisme,) = list(finess_client.stream_organismes(RESOURCE))

    assert organisme.localisation is None
