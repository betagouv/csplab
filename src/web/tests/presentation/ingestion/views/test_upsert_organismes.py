from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from django.urls import reverse
from rest_framework import status

from infrastructure.django_apps.recruteur.models.organisme import OrganismeModel
from presentation.commons.serializers import INVALID_COUNTRY_CODE

URL = reverse("ingestion:organismes_upsert")


def _organisme_payload(**overrides) -> dict:
    payload = {
        "nom": "Commune de Paris",
        "versant": "FPT",
        "siret": "19754687200015",
        "parent_id": None,
        "external_id": "ext-123",
        "referentiel": "FINESS",
        "millesime": "2026-08-19",
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


def test_jwt_authentication_is_rejected(jwt_client, use_case):
    response = jwt_client.post(
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
        "errors": [{"entity_id": "xxx", "error": "db error", "exception": Exception()}],
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
        {"entity_id": "xxx", "error": "db error"},
        {
            "organisme": {"referentiel": "FINESS", "external_id": "ext-invalid"},
            "error": {"nom": ["Ce champ ne peut être nul."]},
        },
    ]


def _localisation(**overrides) -> dict:
    localisation = {
        "zone_geographique": "EU",
        "pays": "FRA",
        "region": "11",
        "departement": "75",
    }
    localisation.update(overrides)
    return localisation


@pytest.mark.parametrize("pays", ["fra", "Fra", "XXX"])
def test_invalid_country_code_is_rejected(api_key_client, use_case, pays):
    use_case.execute.return_value = {"created": 1, "updated": 0, "errors": []}

    response = api_key_client.post(
        URL,
        data={
            "organismes": [
                _organisme_payload(
                    external_id="ext-invalid", localisation=_localisation(pays=pays)
                ),
                _organisme_payload(localisation=_localisation()),
            ]
        },
        content_type="application/json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["errors"] == [
        {
            "organisme": {"referentiel": "FINESS", "external_id": "ext-invalid"},
            "error": {"localisation": {"pays": [INVALID_COUNTRY_CODE]}},
        }
    ]
    organismes = use_case.execute.call_args.args[0].organismes
    assert [organisme.external_id for organisme in organismes] == ["ext-123"]


def test_returns_error_500(api_key_client, use_case):
    use_case.execute.side_effect = Exception("db error")

    response = api_key_client.post(
        URL,
        data={"organismes": [_organisme_payload()]},
        content_type="application/json",
    )
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR


class TestOrganismesUpsertViewDbVerified:
    @pytest.fixture(autouse=True)
    def mock_container(self):
        return None

    def test_creates_and_persists_the_organisme(self, api_key_client):
        payload = _organisme_payload()

        response = api_key_client.post(
            URL,
            data={"organismes": [payload]},
            content_type="application/json",
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == {"created": 1, "updated": 0, "errors": []}

        organisme = OrganismeModel.objects.get(
            referentiel=payload["referentiel"], external_id=payload["external_id"]
        )
        assert organisme.nom == payload["nom"]
        assert organisme.versant == payload["versant"]
        assert organisme.siret == payload["siret"]
        assert organisme.parent_id == payload["parent_id"]
        assert organisme.millesime == payload["millesime"]


def test_upsert_errors_are_serialized_without_exception(api_key_client, use_case):
    entity_id = uuid4()
    use_case.execute.return_value = {
        "created": 0,
        "updated": 0,
        "errors": [
            {
                "entity_id": entity_id,
                "error": "SIRET déjà porté",
                "exception": ValueError("SIRET déjà porté"),
            }
        ],
    }

    response = api_key_client.post(
        URL,
        data={"organismes": [_organisme_payload()]},
        content_type="application/json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        "created": 0,
        "updated": 0,
        "errors": [{"entity_id": str(entity_id), "error": "SIRET déjà porté"}],
    }
