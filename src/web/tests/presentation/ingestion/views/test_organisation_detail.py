import pytest
from django.urls import reverse
from rest_framework import status

from infrastructure.factories.ingestion.talentsoft_organisme_django_factory import (
    TalentsoftOrganismeDjangoFactory,
)
from tests.utils.openapi_test_utils import assert_matches_openapi_schema


def _url(entity_code):
    return reverse(
        "ingestion_fake_ts:organisation_detail", kwargs={"entity_code": entity_code}
    )


@pytest.mark.django_db
def test_returns_talentsoft_organisation(authenticated_client):
    TalentsoftOrganismeDjangoFactory(
        entity_code="ENT-1",
        code=1,
        name="Commune de Paris",
        description="Description de la commune",
        url="https://paris.fr",
        phone_number="0102030405",
        post_code="75001",
        latitude=48.8566,
        longitude=2.3522,
        parent_name="Métropole du Grand Paris",
        logo_url="https://paris.fr/logo.png",
        max_delay_for_consent=30,
        retention_period=24,
        general_conditions="Conditions générales",
        personal_data_consent="Consentement",
    )

    response = authenticated_client.get(_url("ENT-1"))

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "entityCode": "ENT-1",
        "name": "Commune de Paris",
        "description": "Description de la commune",
        "url": "https://paris.fr",
        "phoneNumber": "0102030405",
        "postCode": "75001",
        "geolocation": {"latitude": 48.8566, "longitude": 2.3522},
        "parentName": "Métropole du Grand Paris",
        "logoUrl": "https://paris.fr/logo.png",
        "maxDelayForConsent": 30,
        "retentionPeriod": 24,
        "generalConditions": "Conditions générales",
        "personalDataConsent": "Consentement",
    }


@pytest.mark.django_db
def test_geolocation_is_null_without_coordinates(authenticated_client):
    TalentsoftOrganismeDjangoFactory(entity_code="ENT-1")

    response = authenticated_client.get(_url("ENT-1"))

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["geolocation"] is None


@pytest.mark.django_db
def test_unknown_organisation_returns_404(authenticated_client):
    response = authenticated_client.get(_url("UNKNOWN"))

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_unauthenticated_access(api_client):
    response = api_client.get(_url("ENT-1"))

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_response_matches_openapi_schema(authenticated_client):
    TalentsoftOrganismeDjangoFactory(entity_code="ENT-1")

    response = authenticated_client.get(_url("ENT-1"))

    assert_matches_openapi_schema(
        response.json(), "/api/fake-ts/organisation/{entity_code}", method="get"
    )
