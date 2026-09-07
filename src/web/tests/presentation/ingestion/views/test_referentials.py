import pytest
from django.urls import reverse
from referentiel.value_objects.area import GeographicalArea
from referentiel.value_objects.category import Category
from referentiel.value_objects.contract_type import ContractType
from referentiel.value_objects.experience_level import ExperienceLevel
from referentiel.value_objects.offer_conditions import Management, WorkingPlace
from referentiel.value_objects.verse import Verse
from rest_framework import status

from presentation.ingestion.serializers import (
    COUNTRY_NAMES,
    DEPARTMENT_NAMES,
    DOMAIN_NAMES,
    REGION_NAMES,
    FakeTsCodedObjectSerializer,
)
from tests.utils.openapi_test_utils import assert_matches_openapi_schema


@pytest.mark.parametrize(
    "referential_type,enum_cls",
    [
        ("verse", Verse),
        ("area", GeographicalArea),
        ("management", Management),
        ("working_place", WorkingPlace),
        ("contract_type", ContractType),
        ("offer_family_category", Category),
        ("experience_level", ExperienceLevel),
    ],
)
def test_returns_all_enum_members(authenticated_client, referential_type, enum_cls):
    url = reverse(
        "ingestion_fake_ts:referentials_list", kwargs={"type": referential_type}
    )

    response = authenticated_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == len(list(enum_cls))
    assert {item["clientCode"] for item in data} == {e.name for e in enum_cls}
    assert {item["label"] for item in data} == {e.label for e in enum_cls}
    assert all(item["type"] == referential_type for item in data)
    assert all(item["active"] is True for item in data)


@pytest.mark.parametrize(
    "referential_type,names",
    [
        ("country", COUNTRY_NAMES),
        ("region", REGION_NAMES),
        ("department", DEPARTMENT_NAMES),
        ("domain", DOMAIN_NAMES),
    ],
)
def test_returns_all_code_names(authenticated_client, referential_type, names):
    url = reverse(
        "ingestion_fake_ts:referentials_list", kwargs={"type": referential_type}
    )

    response = authenticated_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == len(names)
    assert {item["clientCode"] for item in data} == set(names.keys())
    assert {item["label"] for item in data} == set(names.values())
    assert all(item["type"] == referential_type for item in data)
    assert all(item["active"] is True for item in data)


def test_unauthenticated_access(api_client):
    url = reverse("ingestion_fake_ts:referentials_list", kwargs={"type": "verse"})

    response = api_client.get(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_unknown_referential_returns_404(authenticated_client):
    url = reverse("ingestion_fake_ts:referentials_list", kwargs={"type": "unknown"})

    response = authenticated_client.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_response_has_no_undeclared_fields(authenticated_client):
    url = reverse("ingestion_fake_ts:referentials_list", kwargs={"type": "verse"})

    response = authenticated_client.get(url)
    result = response.json()[0]

    assert set(result.keys()) == set(FakeTsCodedObjectSerializer().fields.keys())


def test_response_matches_openapi_schema(authenticated_client):
    url = reverse("ingestion_fake_ts:referentials_list", kwargs={"type": "verse"})

    response = authenticated_client.get(url)

    assert_matches_openapi_schema(
        response.json(), "/api/fake-ts/referentials/{type}", method="get"
    )
