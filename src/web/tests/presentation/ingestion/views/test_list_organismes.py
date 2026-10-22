import logging
from datetime import datetime, timezone
from unittest.mock import patch

from django.urls import reverse
from rest_framework import status

from config.logger_names import LoggerName
from infrastructure.django_apps.recruteur.models.organisme import OrganismeModel
from infrastructure.factories.identite.organisme_django_factory import (
    OrganismeDjangoFactory,
)


def _organisme(**kwargs) -> OrganismeModel:
    return OrganismeDjangoFactory(**{"referentiel": "FINESS", **kwargs})


URL = reverse("ingestion:organismes")


def _localisation(department: str) -> dict:
    return {"area": "EU", "country": "FRA", "region": "94", "department": department}


def _noms(response) -> list[str]:
    return [organisme["nom"] for organisme in response.json()["results"]]


def test_unauthenticated_access(api_client):
    response = api_client.get(URL)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_accessible_with_jwt(jwt_client):
    response = jwt_client.get(URL)
    assert response.status_code == status.HTTP_200_OK


def test_api_key_is_rejected(api_key_client):
    response = api_key_client.get(URL)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_put_remains_api_key_only(jwt_client):
    response = jwt_client.put(
        URL,
        data={"organismes": [{"referentiel": "FINESS", "external_id": "ext-1"}]},
        content_type="application/json",
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_returns_public_fields(jwt_client):
    parent = _organisme(nom="ARS Corse")
    organisme = _organisme(
        nom="Centre hospitalier de Bastia",
        versant="FPH",
        siret="26200017900016",
        parent_id=parent.id,
        referentiel="FINESS",
        external_id="2B0000020",
        millesime="2026-10",
        gestion_ats=True,
        localisation={
            "area": "EU",
            "country": "FRA",
            "region": "94",
            "department": "2B",
        },
    )

    response = jwt_client.get(URL, {"siret": "26200017900016"})

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "count": 1,
        "next": None,
        "previous": None,
        "results": [
            {
                "id": str(organisme.id),
                "nom": "Centre hospitalier de Bastia",
                "versant": "FPH",
                "siret": "26200017900016",
                "parent_id": str(parent.id),
                "referentiel": "FINESS",
                "external_id": "2B0000020",
                "millesime": "2026-10",
                "localisation": {
                    "zone_geographique": "EU",
                    "pays": "FRA",
                    "region": "94",
                    "departement": "2B",
                },
            }
        ],
    }


def test_localisation_is_null_when_unknown(jwt_client):
    _organisme(localisation=None)

    response = jwt_client.get(URL)

    assert response.json()["results"][0]["localisation"] is None


def test_excludes_deleted_organismes(jwt_client):
    _organisme(nom="Actif")
    _organisme(nom="Supprimé", supprime_le=datetime(2026, 1, 1, tzinfo=timezone.utc))

    response = jwt_client.get(URL)

    assert _noms(response) == ["Actif"]


def test_excludes_organismes_outside_public_referentiels(jwt_client):
    _organisme(nom="Finess", referentiel="FINESS")
    _organisme(nom="Gipcdg", referentiel="GIPCDG")
    _organisme(nom="Dila", referentiel="DILA")
    OrganismeDjangoFactory(nom="Créé par un recruteur", referentiel=None)
    OrganismeDjangoFactory(nom="Autre référentiel", referentiel="INSEE")

    response = jwt_client.get(URL)

    assert _noms(response) == ["Dila", "Finess", "Gipcdg"]


def test_filters_by_several_versants(jwt_client):
    _organisme(nom="Etat", versant="FPE")
    _organisme(nom="Territoriale", versant="FPT")
    _organisme(nom="Hospitaliere", versant="FPH")

    response = jwt_client.get(URL, {"versant": "FPE,FPH"})

    assert _noms(response) == ["Etat", "Hospitaliere"]


def test_invalid_versant_returns_400(jwt_client):
    response = jwt_client.get(URL, {"versant": "FPX"})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "FPX" in response.json()["error"]


def test_filters_by_siret(jwt_client):
    _organisme(nom="Cherché", siret="11111111111111")
    _organisme(nom="Autre", siret="22222222222222")

    response = jwt_client.get(URL, {"siret": "11111111111111"})

    assert _noms(response) == ["Cherché"]


def test_siret_must_have_14_characters(jwt_client):
    response = jwt_client.get(URL, {"siret": "123"})
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_filters_by_name_case_insensitive(jwt_client):
    _organisme(nom="Centre Hospitalier de Bastia")
    _organisme(nom="Mairie de Bastia")

    response = jwt_client.get(URL, {"nom": "hospitalier"})

    assert _noms(response) == ["Centre Hospitalier de Bastia"]


def test_filters_by_departement(jwt_client):
    _organisme(
        nom="Bastia",
        localisation=_localisation("2B"),
    )
    _organisme(
        nom="Ajaccio",
        localisation=_localisation("2A"),
    )
    _organisme(nom="Sans localisation", localisation=None)

    response = jwt_client.get(URL, {"departement": "2B"})

    assert _noms(response) == ["Bastia"]


def test_invalid_departement_returns_400(jwt_client):
    response = jwt_client.get(URL, {"departement": "999"})
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_filters_by_referentiel(jwt_client):
    _organisme(nom="Finess", referentiel="FINESS")
    _organisme(nom="Dila", referentiel="DILA")

    response = jwt_client.get(URL, {"referentiel": "DILA"})

    assert _noms(response) == ["Dila"]


def test_invalid_referentiel_returns_400(jwt_client):
    response = jwt_client.get(URL, {"referentiel": "INSEE"})
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_stable_order_and_pagination(jwt_client):
    homonymes = sorted(
        (_organisme(nom="Mairie") for _ in range(2)),
        key=lambda organisme: organisme.id,
    )

    abbaye = _organisme(nom="Abbaye")

    first_page = jwt_client.get(URL, {"taille": 2, "page": 1}).json()
    second_page = jwt_client.get(URL, {"taille": 2, "page": 2}).json()

    assert first_page["count"] == len(homonymes) + 1
    assert [o["id"] for o in first_page["results"]] == [
        str(abbaye.id),
        str(homonymes[0].id),
    ]
    assert first_page["next"] is not None
    assert [o["id"] for o in second_page["results"]] == [str(homonymes[1].id)]
    assert second_page["next"] is None


def test_page_out_of_range_returns_404(jwt_client):
    _organisme()

    response = jwt_client.get(URL, {"page": 2})

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_unexpected_error_returns_500_and_logs_traceback(jwt_client, caplog):
    with (
        caplog.at_level(logging.ERROR),
        patch(
            "presentation.ingestion.views.organismes.list_public_organismes",
            side_effect=KeyError("siret"),
        ),
    ):
        response = jwt_client.get(URL)

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json() == {"error": "Unexpected error"}
    [record] = [r for r in caplog.records if r.name == LoggerName.INGESTION.value]
    assert record.exc_info[0] is KeyError
