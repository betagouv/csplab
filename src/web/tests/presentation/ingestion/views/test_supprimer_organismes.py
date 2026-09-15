import pytest
from django.urls import reverse
from rest_framework import status

from infrastructure.factories.identite.organisme_django_factory import (
    OrganismeDjangoFactory,
)

URL = reverse("ingestion:organismes_delete")


def _organisme_payload(**overrides) -> dict:
    payload = {"referentiel": "FINESS", "external_id": "ext-123"}
    payload.update(overrides)
    return payload


def test_unauthenticated_access(api_client):
    response = api_client.put(URL)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_jwt_authentication_is_rejected(authenticated_client):
    response = authenticated_client.put(
        URL,
        data={"organismes": [_organisme_payload()]},
        content_type="application/json",
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_method_not_allowed(api_key_client):
    response = api_key_client.get(URL)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.parametrize(
    "num_organismes,expected_msg",
    [
        (101, "Assurez-vous que ce champ n'a pas plus de 100 éléments."),
        (0, "Assurez-vous que ce champ a au moins 1 éléments."),
    ],
)
def test_invalid_payload_returns_error_400(
    api_key_client, num_organismes, expected_msg
):
    response = api_key_client.put(
        URL,
        data={"organismes": [_organisme_payload()] * num_organismes},
        content_type="application/json",
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"organismes": [expected_msg]}


def test_soft_deletes_matching_organisme(api_key_client):
    organisme = OrganismeDjangoFactory(referentiel="FINESS", external_id="ext-123")

    response = api_key_client.put(
        URL,
        data={"organismes": [_organisme_payload()]},
        content_type="application/json",
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"deleted": 1, "not_found": []}
    organisme.refresh_from_db()
    assert organisme.supprime_le is not None


def test_does_not_hard_delete(api_key_client):
    organisme = OrganismeDjangoFactory(referentiel="FINESS", external_id="ext-123")

    api_key_client.put(
        URL,
        data={"organismes": [_organisme_payload()]},
        content_type="application/json",
    )

    assert type(organisme).objects.filter(id=organisme.id).exists()


def test_returns_unknown_pair_as_not_found(api_key_client):
    response = api_key_client.put(
        URL,
        data={"organismes": [_organisme_payload(external_id="unknown")]},
        content_type="application/json",
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "deleted": 0,
        "not_found": [{"referentiel": "FINESS", "external_id": "unknown"}],
    }


def test_handles_multiple_organismes_in_a_single_call(api_key_client):
    OrganismeDjangoFactory(referentiel="FINESS", external_id="ext-1")
    OrganismeDjangoFactory(referentiel="RNE", external_id="ext-2")

    response = api_key_client.put(
        URL,
        data={
            "organismes": [
                _organisme_payload(referentiel="FINESS", external_id="ext-1"),
                _organisme_payload(referentiel="RNE", external_id="ext-2"),
                _organisme_payload(referentiel="RNE", external_id="unknown"),
            ]
        },
        content_type="application/json",
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "deleted": 2,
        "not_found": [{"referentiel": "RNE", "external_id": "unknown"}],
    }
