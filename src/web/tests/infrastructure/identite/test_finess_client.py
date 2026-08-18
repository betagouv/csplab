import gzip
import json

import pytest

from infrastructure.exceptions.exceptions import ExternalApiError
from infrastructure.external_gateways.finess_client import (
    DATASET_API_URL,
    FinessClient,
)
from infrastructure.gateways.shared.logger import LoggerService

LATITUDE = 46.211257
LONGITUDE = 5.254203


@pytest.fixture(name="finess_client")
def finess_client_fixture():
    return FinessClient(logger=LoggerService())


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

    resource = finess_client.find_latest_journalier()

    assert resource.url == "https://static.data.gouv.fr/20260818.json.gz"
    assert resource.millesime.isoformat() == "2026-08-18"


def test_find_latest_journalier_raises_when_no_resource_matches(
    httpx_mock, finess_client
):
    httpx_mock.add_response(url=DATASET_API_URL, json={"resources": []})

    with pytest.raises(ExternalApiError):
        finess_client.find_latest_journalier()


def test_find_latest_journalier_raises_on_http_error(httpx_mock, finess_client):
    httpx_mock.add_response(url=DATASET_API_URL, status_code=500)

    with pytest.raises(ExternalApiError):
        finess_client.find_latest_journalier()


def test_stream_etablissements_raises_on_http_error(httpx_mock, finess_client):
    url = "https://static.data.gouv.fr/finess.json.gz"
    httpx_mock.add_response(url=url, status_code=500)

    with pytest.raises(ExternalApiError):
        list(finess_client.stream_etablissements(url))


def test_stream_etablissements_yields_ege_with_siret(httpx_mock, finess_client):
    url = "https://static.data.gouv.fr/finess.json.gz"
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
    httpx_mock.add_response(url=url, content=_gzip_payload(pmej))

    etablissements = list(finess_client.stream_etablissements(url))

    assert len(etablissements) == 1
    etablissement = etablissements[0]
    assert etablissement.nom == "CLINIQUE DOCTEUR CONVERT"
    assert etablissement.external_id == "010780195"
    assert etablissement.siret == "77220148900022"
    assert etablissement.latitude == LATITUDE
    assert etablissement.longitude == LONGITUDE
    assert etablissement.departement == "01"


def test_stream_etablissements_derives_dom_departement(httpx_mock, finess_client):
    url = "https://static.data.gouv.fr/finess.json.gz"
    pmej = [
        {
            "ege": [
                {
                    "informationsGeneralesEGE": {
                        "nomEgeLong": "CHU DE POINTE A PITRE",
                        "numFinessEge": "971000015",
                        "siret": "26971000100010",
                    },
                    "adresse": [{"cogCommune": "97120"}],
                }
            ]
        }
    ]
    httpx_mock.add_response(url=url, content=_gzip_payload(pmej))

    (etablissement,) = list(finess_client.stream_etablissements(url))

    assert etablissement.departement == "971"


@pytest.mark.parametrize(
    ("adresse", "coordonnees_geographique"),
    [
        ([], None),
        ([{"cogCommune": "01053"}], {"coordonneeX": "abc", "coordonneeY": "def"}),
    ],
)
def test_stream_etablissements_handles_missing_or_invalid_localisation(
    httpx_mock, finess_client, adresse, coordonnees_geographique
):
    url = "https://static.data.gouv.fr/finess.json.gz"
    if coordonnees_geographique is not None:
        adresse[0]["coordonneesGeographique"] = coordonnees_geographique
    pmej = [
        {
            "ege": [
                {
                    "informationsGeneralesEGE": {
                        "nomEgeLong": "CLINIQUE SANS COORDONNEES",
                        "numFinessEge": "010780195",
                        "siret": "77220148900022",
                    },
                    "adresse": adresse,
                }
            ]
        }
    ]
    httpx_mock.add_response(url=url, content=_gzip_payload(pmej))

    (etablissement,) = list(finess_client.stream_etablissements(url))

    assert etablissement.latitude is None
    assert etablissement.longitude is None


@pytest.mark.parametrize(
    ("cog_commune", "expected_departement"),
    [
        ("5", None),  # too short to be a commune code
        ("97", None),  # DOM/TOM prefix without enough digits
    ],
)
def test_stream_etablissements_handles_short_commune_codes(
    httpx_mock, finess_client, cog_commune, expected_departement
):
    url = "https://static.data.gouv.fr/finess.json.gz"
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
    httpx_mock.add_response(url=url, content=_gzip_payload(pmej))

    (etablissement,) = list(finess_client.stream_etablissements(url))

    assert etablissement.departement == expected_departement
