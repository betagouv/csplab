from uuid import uuid4

import factory
import pytest
from django.urls import reverse
from rest_framework import status

from infrastructure.django_apps.ingestion.models.talentsoft_organisme import (
    TalentsoftOrganismeModel,
)
from infrastructure.factories.identite.organisme_django_factory import (
    OrganismeDjangoFactory,
)

URL = reverse("ingestion:talentsoft_organismes_upsert")

pytestmark = pytest.mark.django_db


class TalentsoftOrganismeUpsertPayloadFactory(factory.DictFactory):
    entity_code = "ENT-1"
    code = factory.Sequence(lambda n: n + 1)
    parent_code = None
    has_children = False
    name = "Commune de Paris"
    description = "Description"
    url = "https://example.com"
    phone_number = "0102030405"
    post_code = "75001"
    latitude = 48.8566
    longitude = 2.3522
    parent_name = None
    logo_url = "https://example.com/logo.png"
    max_delay_for_consent = 30
    retention_period = 365
    general_conditions = "CGU"
    personal_data_consent = "Consentement"


def test_unauthenticated_access(api_client):
    response = api_client.post(URL)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_jwt_authentication_is_rejected(authenticated_client):
    organisme = OrganismeDjangoFactory()
    payload = TalentsoftOrganismeUpsertPayloadFactory(organisme_id=str(organisme.id))
    response = authenticated_client.post(
        URL,
        data={"talentsoft_organismes": [payload]},
        content_type="application/json",
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_method_not_allowed(api_key_client):
    response = api_key_client.get(URL)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.parametrize(
    "num_items,expected_msg",
    [
        (101, "Assurez-vous que ce champ n'a pas plus de 100 éléments."),
        (0, "Assurez-vous que ce champ a au moins 1 éléments."),
    ],
)
def test_invalid_payload_returns_error_400(api_key_client, num_items, expected_msg):
    payload = TalentsoftOrganismeUpsertPayloadFactory(organisme_id=str(uuid4()))
    response = api_key_client.post(
        URL,
        data={"talentsoft_organismes": [payload] * num_items},
        content_type="application/json",
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"talentsoft_organismes": [expected_msg]}


def test_creates_talentsoft_organisme(api_key_client):
    organisme = OrganismeDjangoFactory()
    payload = TalentsoftOrganismeUpsertPayloadFactory(organisme_id=str(organisme.id))

    response = api_key_client.post(
        URL,
        data={"talentsoft_organismes": [payload]},
        content_type="application/json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {"created": 1, "updated": 0, "errors": []}

    talentsoft_organisme = TalentsoftOrganismeModel.objects.get(
        organisme_id=organisme.id
    )
    assert talentsoft_organisme.entity_code == "ENT-1"
    assert talentsoft_organisme.code == payload["code"]
    assert talentsoft_organisme.name == "Commune de Paris"
    assert talentsoft_organisme.latitude == pytest.approx(48.8566)


def test_creates_talentsoft_organisme_with_null_organisme_id(api_key_client):
    payload = TalentsoftOrganismeUpsertPayloadFactory(organisme_id=None)

    response = api_key_client.post(
        URL,
        data={"talentsoft_organismes": [payload]},
        content_type="application/json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {"created": 1, "updated": 0, "errors": []}
    talentsoft_organisme = TalentsoftOrganismeModel.objects.get(entity_code="ENT-1")
    assert talentsoft_organisme.organisme_id is None


def test_creates_talentsoft_organisme_without_organisme_id_field(api_key_client):
    payload = TalentsoftOrganismeUpsertPayloadFactory()
    assert "organisme_id" not in payload

    response = api_key_client.post(
        URL,
        data={"talentsoft_organismes": [payload]},
        content_type="application/json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {"created": 1, "updated": 0, "errors": []}
    talentsoft_organisme = TalentsoftOrganismeModel.objects.get(entity_code="ENT-1")
    assert talentsoft_organisme.organisme_id is None


def test_updates_existing_talentsoft_organisme(api_key_client):
    organisme = OrganismeDjangoFactory()
    payload = TalentsoftOrganismeUpsertPayloadFactory(organisme_id=str(organisme.id))
    api_key_client.post(
        URL,
        data={"talentsoft_organismes": [payload]},
        content_type="application/json",
    )

    payload["name"] = "Commune de Lyon"
    payload["code"] += 1
    response = api_key_client.post(
        URL,
        data={"talentsoft_organismes": [payload]},
        content_type="application/json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {"created": 0, "updated": 1, "errors": []}
    talentsoft_organisme = TalentsoftOrganismeModel.objects.get(
        organisme_id=organisme.id
    )
    assert talentsoft_organisme.name == "Commune de Lyon"
    assert talentsoft_organisme.code == payload["code"]


def test_upsert_matches_by_entity_code_not_organisme_id(api_key_client):
    first_organisme = OrganismeDjangoFactory()
    second_organisme = OrganismeDjangoFactory()
    payload = TalentsoftOrganismeUpsertPayloadFactory(
        organisme_id=str(first_organisme.id)
    )
    api_key_client.post(
        URL,
        data={"talentsoft_organismes": [payload]},
        content_type="application/json",
    )

    payload["organisme_id"] = str(second_organisme.id)
    response = api_key_client.post(
        URL,
        data={"talentsoft_organismes": [payload]},
        content_type="application/json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {"created": 0, "updated": 1, "errors": []}
    assert TalentsoftOrganismeModel.objects.count() == 1
    talentsoft_organisme = TalentsoftOrganismeModel.objects.get(entity_code="ENT-1")
    assert talentsoft_organisme.organisme_id == second_organisme.id


def test_unknown_organisme_id_reported_as_error(api_key_client):
    unknown_id = uuid4()
    payload = TalentsoftOrganismeUpsertPayloadFactory(organisme_id=str(unknown_id))

    response = api_key_client.post(
        URL,
        data={"talentsoft_organismes": [payload]},
        content_type="application/json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    body = response.json()
    assert body["created"] == 0
    assert body["updated"] == 0
    assert body["errors"] == [
        {
            "talentsoft_organisme": {
                "entity_code": "ENT-1",
                "organisme_id": str(unknown_id),
            },
            "error": "Organisme introuvable.",
        }
    ]


def test_creates_and_updates_multiple_items_in_a_single_batch(api_key_client):
    organisme_a = OrganismeDjangoFactory()
    organisme_b = OrganismeDjangoFactory()
    payload_a = TalentsoftOrganismeUpsertPayloadFactory(
        organisme_id=str(organisme_a.id), entity_code="ENT-A"
    )
    api_key_client.post(
        URL,
        data={"talentsoft_organismes": [payload_a]},
        content_type="application/json",
    )

    payload_a_updated = TalentsoftOrganismeUpsertPayloadFactory(
        organisme_id=str(organisme_a.id), entity_code="ENT-A", name="Renommé"
    )
    payload_b = TalentsoftOrganismeUpsertPayloadFactory(
        organisme_id=str(organisme_b.id), entity_code="ENT-B"
    )

    response = api_key_client.post(
        URL,
        data={"talentsoft_organismes": [payload_a_updated, payload_b]},
        content_type="application/json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {"created": 1, "updated": 1, "errors": []}
    assert TalentsoftOrganismeModel.objects.get(entity_code="ENT-A").name == "Renommé"
    assert TalentsoftOrganismeModel.objects.filter(entity_code="ENT-B").exists()


def test_duplicate_entity_code_in_same_batch_is_rejected(api_key_client):
    organisme = OrganismeDjangoFactory()
    first = TalentsoftOrganismeUpsertPayloadFactory(
        organisme_id=str(organisme.id), name="Premier"
    )
    second = TalentsoftOrganismeUpsertPayloadFactory(
        organisme_id=str(organisme.id), name="Second"
    )

    response = api_key_client.post(
        URL,
        data={"talentsoft_organismes": [first, second]},
        content_type="application/json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    body = response.json()
    assert body["created"] == 0
    assert body["updated"] == 0
    assert (
        body["errors"]
        == [
            {
                "talentsoft_organisme": {
                    "entity_code": "ENT-1",
                    "organisme_id": str(organisme.id),
                },
                "error": "entity_code en doublon dans le lot.",
            }
        ]
        * 2
    )
    assert not TalentsoftOrganismeModel.objects.exists()


def test_duplicate_code_in_same_batch_is_rejected(api_key_client):
    first = TalentsoftOrganismeUpsertPayloadFactory(entity_code="ENT-A", code=1)
    second = TalentsoftOrganismeUpsertPayloadFactory(entity_code="ENT-B", code=1)

    response = api_key_client.post(
        URL,
        data={"talentsoft_organismes": [first, second]},
        content_type="application/json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    body = response.json()
    assert body["created"] == 0
    assert body["updated"] == 0
    assert [error["error"] for error in body["errors"]] == [
        "code en doublon dans le lot."
    ] * 2
    assert not TalentsoftOrganismeModel.objects.exists()


def test_missing_code_is_rejected(api_key_client):
    payload = TalentsoftOrganismeUpsertPayloadFactory()
    del payload["code"]

    response = api_key_client.post(
        URL,
        data={"talentsoft_organismes": [payload]},
        content_type="application/json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    body = response.json()
    assert body["created"] == 0
    assert len(body["errors"]) == 1
    assert not TalentsoftOrganismeModel.objects.exists()


def test_all_items_invalid_returns_zero_counts(api_key_client):
    invalid_payload = TalentsoftOrganismeUpsertPayloadFactory(
        organisme_id=str(uuid4()), name=None
    )

    response = api_key_client.post(
        URL,
        data={"talentsoft_organismes": [invalid_payload]},
        content_type="application/json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    body = response.json()
    assert body["created"] == 0
    assert body["updated"] == 0
    assert len(body["errors"]) == 1


def test_mixed_valid_invalid_items_in_payload(api_key_client):
    organisme = OrganismeDjangoFactory()
    valid_payload = TalentsoftOrganismeUpsertPayloadFactory(
        organisme_id=str(organisme.id)
    )
    invalid_payload = TalentsoftOrganismeUpsertPayloadFactory(
        organisme_id=str(organisme.id), name=None
    )

    response = api_key_client.post(
        URL,
        data={"talentsoft_organismes": [valid_payload, invalid_payload]},
        content_type="application/json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    body = response.json()
    assert body["created"] == 1
    assert body["updated"] == 0
    assert len(body["errors"]) == 1
    assert body["errors"][0]["talentsoft_organisme"]["organisme_id"] == str(
        organisme.id
    )
