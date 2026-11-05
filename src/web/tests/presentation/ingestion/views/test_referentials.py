import pytest
from django.urls import reverse
from referentiel.value_objects.area import GeographicalArea
from referentiel.value_objects.category import Category
from referentiel.value_objects.experience_level import ExperienceLevel
from referentiel.value_objects.offer_conditions import Management, WorkingPlace
from referentiel.value_objects.offer_nature import OfferNature
from referentiel.value_objects.radius import Radius
from referentiel.value_objects.verse import Verse
from rest_framework import status

from infrastructure.factories.ingestion.talentsoft_organisme_django_factory import (
    TalentsoftOrganismeDjangoFactory,
)
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
        ("contract_type", OfferNature),
        ("offer_family_category", Category),
        ("experience_level", ExperienceLevel),
        ("radius", Radius),
    ],
)
def test_returns_all_enum_members(jwt_client, referential_type, enum_cls):
    url = reverse(
        "ingestion_fake_ts:referentials_list",
        kwargs={"referential_type": referential_type},
    )

    response = jwt_client.get(url)

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
def test_returns_all_code_names(jwt_client, referential_type, names):
    url = reverse(
        "ingestion_fake_ts:referentials_list",
        kwargs={"referential_type": referential_type},
    )

    response = jwt_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == len(names)
    assert {item["clientCode"] for item in data} == set(names.keys())
    assert {item["label"] for item in data} == set(names.values())
    assert all(item["type"] == referential_type for item in data)
    assert all(item["active"] is True for item in data)


def _get_referential(client, referential_type, **params):
    url = reverse(
        "ingestion_fake_ts:referentials_list",
        kwargs={"referential_type": referential_type},
    )
    response = client.get(url, params)
    assert response.status_code == status.HTTP_200_OK
    return {item["clientCode"]: item for item in response.json()}


def test_departments_belong_to_their_region(jwt_client):
    departments = _get_referential(jwt_client, "department")

    assert all(item["parentType"] == "region" for item in departments.values())
    assert set(departments) == set(DEPARTMENT_NAMES)
    assert {item["parentCode"] for item in departments.values()} <= set(REGION_NAMES)
    assert departments["75"]["parentCode"] == "11"
    assert departments["2A"]["parentCode"] == "94"
    assert departments["971"]["parentCode"] == "DOM"
    assert departments["988"]["parentCode"] == "TOM"
    assert departments["SPM"]["parentCode"] == "TOM"
    assert departments["75"]["code"] is None
    assert departments["75"]["hasChildren"] is False


def test_regions_belong_to_france(jwt_client):
    regions = _get_referential(jwt_client, "region")

    assert all(item["parentCode"] == "FRA" for item in regions.values())
    assert all(item["parentType"] == "country" for item in regions.values())
    assert regions["11"]["hasChildren"] is True
    assert regions["DOM"]["hasChildren"] is True
    assert regions["TOM"]["hasChildren"] is True
    assert regions["01"]["hasChildren"] is False


def test_countries_belong_to_their_zone(jwt_client):
    countries = _get_referential(jwt_client, "country")
    zone_codes = {area.name for area in GeographicalArea}

    assert all(item["parentCode"] in zone_codes for item in countries.values())
    assert all(item["parentType"] == "area" for item in countries.values())
    assert countries["FRA"]["parentCode"] == "EUROPE"
    assert countries["MAR"]["parentCode"] == "MOYEN_ORIENT_AFRIQUE_DU_NORD"
    assert countries["FRA"]["hasChildren"] is True
    assert countries["BEL"]["hasChildren"] is False


def test_zones_have_countries(jwt_client):
    areas = _get_referential(jwt_client, "area")

    assert all(item["parentCode"] is None for item in areas.values())
    assert all(item["hasChildren"] is True for item in areas.values())


def test_filters_countries_by_zone(jwt_client):
    countries = _get_referential(jwt_client, "country", parentCode="ANTARTIQUE")

    assert set(countries) == {"ATA", "ATF", "BVT", "HMD", "SGS"}


def test_filters_departments_by_parent_code(jwt_client):
    departments = _get_referential(jwt_client, "department", parentCode="11")

    assert set(departments) == {"75", "77", "78", "91", "92", "93", "94", "95"}


def test_filters_regions_by_parent_code(jwt_client):
    assert set(_get_referential(jwt_client, "region", parentCode="FRA")) == set(
        REGION_NAMES
    )
    assert _get_referential(jwt_client, "region", parentCode="BEL") == {}


def test_parent_code_filter_excludes_values_without_parent(jwt_client):
    assert _get_referential(jwt_client, "area", parentCode="EUROPE") == {}


@pytest.mark.django_db
def test_filters_talentsoft_organismes_by_parent_code(jwt_client):
    TalentsoftOrganismeDjangoFactory(
        entity_code="ENT-1", code=1, name="Ministère", has_children=True
    )
    TalentsoftOrganismeDjangoFactory(
        entity_code="ENT-2", code=2, name="Direction", parent_code=1
    )

    organisations = _get_referential(jwt_client, "organisation", parentCode="1")

    assert set(organisations) == {"ENT-2"}
    assert organisations["ENT-2"]["parentCode"] == 1


@pytest.mark.django_db
def test_returns_all_talentsoft_organismes(jwt_client):
    TalentsoftOrganismeDjangoFactory(
        entity_code="ENT-1", code=1, name="Ministère", has_children=True
    )
    TalentsoftOrganismeDjangoFactory(
        entity_code="ENT-2", code=2, name="Direction", parent_code=1
    )
    url = reverse(
        "ingestion_fake_ts:referentials_list",
        kwargs={"referential_type": "organisation"},
    )

    response = jwt_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {
            "code": 1,
            "clientCode": "ENT-1",
            "label": "Ministère",
            "active": True,
            "parentCode": None,
            "type": "organisation",
            "parentType": "",
            "hasChildren": True,
        },
        {
            "code": 2,
            "clientCode": "ENT-2",
            "label": "Direction",
            "active": True,
            "parentCode": 1,
            "type": "organisation",
            "parentType": "organisation",
            "hasChildren": False,
        },
    ]


def test_unauthenticated_access(api_client):
    url = reverse(
        "ingestion_fake_ts:referentials_list", kwargs={"referential_type": "verse"}
    )

    response = api_client.get(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_unknown_referential_returns_404(jwt_client):
    url = reverse(
        "ingestion_fake_ts:referentials_list", kwargs={"referential_type": "unknown"}
    )

    response = jwt_client.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_response_has_no_undeclared_fields(jwt_client):
    url = reverse(
        "ingestion_fake_ts:referentials_list", kwargs={"referential_type": "verse"}
    )

    response = jwt_client.get(url)
    result = response.json()[0]

    assert set(result.keys()) == set(FakeTsCodedObjectSerializer().fields.keys())


@pytest.mark.parametrize(
    "referential_type", ["verse", "area", "country", "region", "department"]
)
def test_response_matches_openapi_schema(jwt_client, referential_type):
    url = reverse(
        "ingestion_fake_ts:referentials_list",
        kwargs={"referential_type": referential_type},
    )

    response = jwt_client.get(url)

    assert_matches_openapi_schema(
        response.json(), "/api/fake-ts/referentials/{referential_type}", method="get"
    )
