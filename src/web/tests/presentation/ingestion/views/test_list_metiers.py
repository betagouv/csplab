from datetime import UTC, datetime
from unittest.mock import patch
from urllib.parse import parse_qs, urlparse

import pytest
from django.urls import reverse
from rest_framework import status

from infrastructure.django_apps.referentiel.models.metier import MetierQuerySet
from infrastructure.factories.referentiel.metier_django_factory import (
    MetierDjangoFactory,
)

URL = reverse("ingestion:metiers_list")
NOW = datetime.now(UTC)

NOMBRE_REQUETES_ATTENDU = (
    1  # authentification JWT
    + 1  # restriction IP du compte JWT
    + 2  # pagination : count + page
    + 1  # ApiRequestLoggerMiddleware redecode JWT token for logging
    # TODO: refactor ADR-009 : simplify UPDATE/INSERT
    + 2  # logging : UPDATE (manually assigned pk) then INSERT
)


def _codes(response) -> list[str]:
    return [metier["code_emploi_csp"] for metier in response.json()["results"]]


def test_unauthenticated_access(api_client):
    response = api_client.get(URL)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_post_not_allowed(jwt_client):
    response = jwt_client.post(URL)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_empty_result(jwt_client):
    response = jwt_client.get(URL)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "count": 0,
        "next": None,
        "previous": None,
        "results": [],
    }


def test_response_matches_db_record_field_by_field(jwt_client):
    metier = MetierDjangoFactory(
        domaine_fonctionnel_code="TRA",
        versants=["FPE"],
        activites=["Rédiger des actes"],
        conditions_particulieres=["Habilitation"],
    )

    response = jwt_client.get(URL)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["count"] == 1
    assert data["results"] == [
        {
            "libelle": metier.libelle_long,
            "description": metier.definition_synthetique,
            "domaine_fonctionnel_code": metier.domaine_fonctionnel_code,
            "versants": metier.versants,
            "activites": metier.activites,
            "conditions_particulieres": metier.conditions_particulieres,
            "code_emploi_csp": metier.offer_family_code,
            "actif": True,
            "referentiel": "RMFPv2",
        }
    ]


def test_archived_metier_is_returned_as_inactive(jwt_client):
    MetierDjangoFactory(archived_at=NOW)

    response = jwt_client.get(URL)

    assert [metier["actif"] for metier in response.json()["results"]] == [False]


def test_filters_by_several_domains(jwt_client):
    MetierDjangoFactory(domaine_fonctionnel_code="JUS", offer_family_code="ERJUS008")
    MetierDjangoFactory(domaine_fonctionnel_code="CTL", offer_family_code="ERCTL001")
    MetierDjangoFactory(domaine_fonctionnel_code="NUM", offer_family_code="ERNUM001")

    response = jwt_client.get(URL, {"domaine": "JUS,ctl"})

    assert response.status_code == status.HTTP_200_OK
    assert _codes(response) == ["ERCTL001", "ERJUS008"]


def test_unknown_domain_returns_400(jwt_client):
    response = jwt_client.get(URL, {"domaine": "JUS,ABC"})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Valeurs de domaine invalides : ABC." in response.json()["error"]


def test_filters_by_several_codes(jwt_client):
    MetierDjangoFactory(offer_family_code="ERJUS008")
    MetierDjangoFactory(offer_family_code="ERNUM001")
    MetierDjangoFactory(offer_family_code="ERTRA007")

    response = jwt_client.get(URL, {"code_emploi_csp": "ERJUS008, ERNUM001"})

    assert response.status_code == status.HTTP_200_OK
    assert _codes(response) == ["ERJUS008", "ERNUM001"]


@pytest.mark.parametrize(
    "actif, expected",
    [("true", ["ERACT001"]), ("false", ["ERARC001"]), (None, ["ERACT001", "ERARC001"])],
)
def test_filters_by_active(jwt_client, actif, expected):
    MetierDjangoFactory(offer_family_code="ERACT001")
    MetierDjangoFactory(offer_family_code="ERARC001", archived_at=NOW)

    response = jwt_client.get(URL, {"actif": actif} if actif else {})

    assert response.status_code == status.HTTP_200_OK
    assert _codes(response) == expected


def test_filters_by_versant(jwt_client):
    MetierDjangoFactory(offer_family_code="ERFPE001", versants=["FPE", "FPT"])
    MetierDjangoFactory(offer_family_code="ERFPH001", versants=["FPH"])

    response = jwt_client.get(URL, {"versant": "FPT"})

    assert response.status_code == status.HTTP_200_OK
    assert _codes(response) == ["ERFPE001"]


@pytest.mark.parametrize(
    "params",
    [{"actif": "peut-etre"}, {"versant": "FPX"}, {"versant": "FPE,FPT"}],
)
def test_invalid_filter_returns_400(jwt_client, params):
    response = jwt_client.get(URL, params)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "error" in response.json()


def test_sorted_by_code_then_id(jwt_client):
    second = MetierDjangoFactory(offer_family_code="ERTRA002")
    homonyms = sorted(
        MetierDjangoFactory.create_batch(2, offer_family_code="ERTRA001"),
        key=lambda metier: metier.id,
    )

    response = jwt_client.get(URL)

    assert [metier["libelle"] for metier in response.json()["results"]] == [
        homonyms[0].libelle_long,
        homonyms[1].libelle_long,
        second.libelle_long,
    ]


def test_pagination_page_arg(jwt_client):
    MetierDjangoFactory.create_batch(5)

    response = jwt_client.get(URL, {"page": 2, "taille": 2, "dummy": "arg"})

    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert data["count"] == 5  # noqa: PLR2004
    assert len(data["results"]) == 2  # noqa: PLR2004

    parsed_previous = urlparse(data["previous"])
    assert parsed_previous.path == URL
    assert parse_qs(parsed_previous.query) == {
        "dummy": ["arg"],
        "taille": ["2"],
    }

    parsed_next = urlparse(data["next"])
    assert parsed_next.path == URL
    assert parse_qs(parsed_next.query) == {
        "page": ["3"],
        "dummy": ["arg"],
        "taille": ["2"],
    }


def test_pagination_out_of_bounds_returns_404(jwt_client):
    MetierDjangoFactory.create_batch(3)

    response = jwt_client.get(URL, {"page": 3, "taille": 2})

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "detail" in response.json()


@pytest.mark.parametrize("page", ["0", "-1", "abc"])
def test_pagination_invalid_page_returns_404(jwt_client, page):
    response = jwt_client.get(URL, {"page": page})

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.parametrize("taille", ["0", "-5", "abc"])
def test_pagination_invalid_taille_falls_back_to_default(jwt_client, taille):
    MetierDjangoFactory.create_batch(3)

    response = jwt_client.get(URL, {"taille": taille})

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["results"]) == 3  # noqa: PLR2004


def test_pagination_taille_is_capped(jwt_client):
    MetierDjangoFactory.create_batch(3)

    response = jwt_client.get(URL, {"taille": 1_000_000, "page": 1})

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["results"]) == 3  # noqa: PLR2004


def test_unexpected_error_returns_500(jwt_client):
    with patch.object(MetierQuerySet, "stable_order", side_effect=KeyError("id")):
        response = jwt_client.get(URL)

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json() == {"error": "Unexpected error"}


def test_does_not_trigger_n_plus_one_queries(jwt_client, django_assert_num_queries):
    MetierDjangoFactory.create_batch(5)

    with django_assert_num_queries(NOMBRE_REQUETES_ATTENDU):
        response = jwt_client.get(URL)

    assert response.status_code == status.HTTP_200_OK
