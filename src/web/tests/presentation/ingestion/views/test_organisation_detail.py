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


def test_returns_talentsoft_organisation(db, authenticated_client):
    ts_organisme = TalentsoftOrganismeDjangoFactory()

    response = authenticated_client.get(_url(ts_organisme.entity_code))

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "entityCode": ts_organisme.entity_code,
        "name": ts_organisme.name,
        "description": ts_organisme.description,
        "url": ts_organisme.url,
        "phoneNumber": ts_organisme.phone_number,
        "postCode": ts_organisme.post_code,
        "geolocation": {
            "latitude": ts_organisme.latitude,
            "longitude": ts_organisme.longitude,
        },
        "parentName": ts_organisme.parent_name,
        "logoUrl": ts_organisme.logo_url,
        "maxDelayForConsent": ts_organisme.max_delay_for_consent,
        "retentionPeriod": ts_organisme.retention_period,
        "generalConditions": ts_organisme.general_conditions,
        "personalDataConsent": ts_organisme.personal_data_consent,
    }


def test_geolocation_is_null_without_coordinates(db, authenticated_client):
    ts_organisme = TalentsoftOrganismeDjangoFactory(latitude=None, longitude=None)

    response = authenticated_client.get(_url(ts_organisme.entity_code))

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["geolocation"] is None


def test_unknown_organisation_returns_404(db, authenticated_client):
    response = authenticated_client.get(_url("UNKNOWN"))

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"error": "Organisation inconnue : UNKNOWN."}


def test_unauthenticated_access(api_client):
    response = api_client.get(_url("ENT-1"))

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_response_matches_openapi_schema(db, authenticated_client):
    ts_organisme = TalentsoftOrganismeDjangoFactory()

    response = authenticated_client.get(_url(ts_organisme.entity_code))

    assert_matches_openapi_schema(
        response.json(), "/api/fake-ts/organisation/{entity_code}", method="get"
    )
