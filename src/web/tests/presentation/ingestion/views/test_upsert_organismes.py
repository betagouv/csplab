from unittest.mock import MagicMock

import pytest
from django.urls import reverse
from rest_framework import status

URL = reverse("ingestion:organismes_upsert")


def _organisme_payload(**overrides) -> dict:
    payload = {
        "nom": "Commune de Paris",
        "versant": "FPT",
        "siret": "19754687200015",
        "parent_id": None,
        "external_id": "ext-123",
        "referentiel": "FINESS",
        "millesime": None,
    }
    payload.update(overrides)
    return payload


@pytest.fixture
def use_case():
    mock = MagicMock()
    mock.execute.return_value = {"created": 0, "updated": 0, "errors": []}
    return mock


@pytest.fixture(autouse=True)
def mock_container(mock_organismes_container, use_case):
    mock_organismes_container.upsert_organismes_usecase.return_value = use_case


def test_unauthenticated_access(api_client):
    response = api_client.post(URL)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_jwt_authentication_is_rejected(authenticated_client, use_case):
    response = authenticated_client.post(
        URL,
        data={"organismes": [_organisme_payload()]},
        content_type="application/json",
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_api_key_authentication(api_key_client, use_case):
    use_case.execute.return_value = {"created": 1, "updated": 0, "errors": []}
    response = api_key_client.post(
        URL,
        data={"organismes": [_organisme_payload()]},
        content_type="application/json",
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {"created": 1, "updated": 0, "errors": []}


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
    response = api_key_client.post(
        URL,
        data={"organismes": [_organisme_payload()] * num_organismes},
        content_type="application/json",
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"organismes": [expected_msg]}


def test_valid_payload_calls_usecase_with_mapped_organismes(api_key_client, use_case):
    use_case.execute.return_value = {"created": 1, "updated": 0, "errors": []}

    response = api_key_client.post(
        URL,
        data={"organismes": [_organisme_payload()]},
        content_type="application/json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    upsert_input = use_case.execute.call_args[0][0]
    assert len(upsert_input.organismes) == 1
    organisme_data = upsert_input.organismes[0]
    assert organisme_data.nom == "Commune de Paris"
    assert organisme_data.external_id == "ext-123"
    assert organisme_data.referentiel == "FINESS"


def test_mixed_valid_invalid_organismes_in_payload(api_key_client, use_case):
    use_case.execute.return_value = {
        "created": 1,
        "updated": 0,
        "errors": ["db error on organisme xxx"],
    }
    response = api_key_client.post(
        URL,
        data={
            "organismes": [
                _organisme_payload(),
                _organisme_payload(nom=None, external_id="ext-invalid"),
            ]
        },
        content_type="application/json",
    )
    assert response.status_code == status.HTTP_201_CREATED
    errors = response.json()["errors"]
    assert errors == [
        "db error on organisme xxx",
        {
            "organisme": {"referentiel": "FINESS", "external_id": "ext-invalid"},
            "error": {"nom": ["Ce champ ne peut être nul."]},
        },
    ]


def test_returns_error_500(api_key_client, use_case):
    use_case.execute.side_effect = Exception("db error")

    response = api_key_client.post(
        URL,
        data={"organismes": [_organisme_payload()]},
        content_type="application/json",
    )
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
