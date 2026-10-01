from datetime import UTC, datetime
from unittest.mock import MagicMock

import pytest
from django.urls import reverse
from pydantic import HttpUrl
from referentiel.value_objects.area import GeographicalArea
from referentiel.value_objects.category import Category
from referentiel.value_objects.country import Country
from referentiel.value_objects.department import Department
from referentiel.value_objects.domaine_fonctionnel import DomaineFonctionnel
from referentiel.value_objects.experience_level import ExperienceLevel
from referentiel.value_objects.offer_conditions import Management, WorkingPlace
from referentiel.value_objects.offer_nature import OfferNature
from referentiel.value_objects.region import Region
from referentiel.value_objects.verse import Verse
from rest_framework import status

from application.ingestion.interfaces.list_offers_input import GetFilteredOffersInput
from infrastructure.factories.ingestion.talentsoft_organisme_django_factory import (
    TalentsoftOrganismeDjangoFactory,
)
from infrastructure.factories.referentiel.offer_django_factory import (
    OfferDjangoFactory,
)
from infrastructure.factories.referentiel.offer_factory import OfferFactory
from presentation.ingestion.serializers import (
    FakeTsCodedObjectSerializer,
    FakeTsOfferSummarySerializer,
)
from tests.utils.openapi_test_utils import assert_matches_openapi_schema

URL = reverse("ingestion_fake_ts:offer_summaries")

NOMBRE_REQUETES_ATTENDU = (
    1  # view JWT authentication
    + 2  # pagination: count + slice
    + 1  # ApiRequestLoggerMiddleware re-decodes the JWT to log the request
    + 2  # logging: DJ tries an UPDATE (manually-assigned pk) then falls back to INSERT
)


def _make_paginated_mock(mock_container, total, offers_slice):
    mock_page = MagicMock()
    mock_page.count.return_value = total
    mock_page.slice.return_value = iter(offers_slice)

    mock_usecase = MagicMock()
    mock_usecase.execute.return_value = mock_page
    mock_container.list_offers_usecase.return_value = mock_usecase

    return mock_usecase


def test_unauthenticated_access(api_client):
    response = api_client.get(URL)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_valid_api_key_no_longer_grants_access(api_key_client):
    response = api_key_client.get(URL)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_post_not_allowed(jwt_client):
    response = jwt_client.post(URL)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_empty_result(mock_offer_summaries_container, jwt_client):
    _make_paginated_mock(mock_offer_summaries_container, total=0, offers_slice=[])

    response = jwt_client.get(URL)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "data": [],
        "_pagination": {
            "start": 0,
            "count": 0,
            "total": 0,
            "resultsPerPage": 100,
            "hasMore": False,
        },
    }


def test_only_queries_non_archived_offers(mock_offer_summaries_container, jwt_client):
    _make_paginated_mock(mock_offer_summaries_container, total=0, offers_slice=[])

    jwt_client.get(URL)

    mock_offer_summaries_container.list_offers_usecase.return_value.execute.assert_called_once_with(
        GetFilteredOffersInput(active=True)
    )


def test_call_without_arg(mock_offer_summaries_container, jwt_client):
    offer = OfferFactory.create_entity(
        offer_nature=OfferNature.TERRITORIAL,
        category=Category.A,
    )
    _make_paginated_mock(mock_offer_summaries_container, total=1, offers_slice=[offer])

    response = jwt_client.get(URL)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert data["_pagination"] == {
        "start": 0,
        "count": 1,
        "total": 1,
        "resultsPerPage": 100,
        "hasMore": False,
    }

    result = data["data"][0]
    assert result["reference"] == offer.reference
    assert result["title"] == offer.title
    assert result["organisationName"] == offer.organization
    assert result["description1"] == offer.mission
    assert result["description2"] == offer.profile
    assert result["contractType"]["clientCode"] == offer.offer_nature.name
    assert result["contractType"]["label"] == offer.offer_nature.value
    assert result["offerFamilyCategory"]["clientCode"] == offer.category.name
    assert result["offerFamilyCategory"]["label"] == offer.category.value
    assert result["startPublicationDate"] == "2024-01-15T00:00:00"
    assert result["country"] == [
        {
            "code": None,
            "clientCode": str(offer.localisation.country),
            "label": offer.localisation.country.short_name,
            "active": True,
            "parentCode": None,
            "type": "country",
            "parentType": "",
            "hasChildren": False,
        }
    ]
    assert result["region"][0]["clientCode"] == offer.localisation.region.code
    assert result["region"][0]["label"] == offer.localisation.region.name
    assert result["department"][0]["clientCode"] == offer.localisation.department.code
    assert result["department"][0]["label"] == offer.localisation.department.name


def test_response_matches_openapi_schema(mock_offer_summaries_container, jwt_client):
    offer = OfferFactory.create_entity(
        offer_nature=OfferNature.TERRITORIAL,
        category=Category.A,
    )
    _make_paginated_mock(mock_offer_summaries_container, total=1, offers_slice=[offer])

    response = jwt_client.get(URL)

    assert_matches_openapi_schema(
        response.json(), "/api/fake-ts/offersummaries", method="get"
    )


def test_response_has_no_undeclared_fields(mock_offer_summaries_container, jwt_client):
    offer = OfferFactory.create_entity(
        offer_nature=OfferNature.TERRITORIAL,
        category=Category.A,
    )
    _make_paginated_mock(mock_offer_summaries_container, total=1, offers_slice=[offer])

    response = jwt_client.get(URL)
    result = response.json()["data"][0]

    assert set(result.keys()) == set(FakeTsOfferSummarySerializer().fields.keys())
    assert set(result["contractType"].keys()) == set(
        FakeTsCodedObjectSerializer().fields.keys()
    )
    assert set(result["offerFamilyCategory"].keys()) == set(
        FakeTsCodedObjectSerializer().fields.keys()
    )
    assert set(result["country"][0].keys()) == set(
        FakeTsCodedObjectSerializer().fields.keys()
    )


class TestOfferSummariesViewDbVerified:
    def test_response_matches_db_record_field_by_field(self, jwt_client):
        OfferDjangoFactory(
            reference="REF-E2E-SUMMARY-1",
            title="Développeur Backend",
            profile="Profil recherché",
            mission="Mission du poste",
            organization="Ministère Test",
            category=Category.A,
            offer_nature=OfferNature.TERRITORIAL,
            offer_url=HttpUrl("https://exemple.gouv.fr/offres/e2e-1"),
            country="FRA",
            region="11",
            department="75",
            location_label="Paris",
            latitude=48.8566,
            longitude=2.3522,
            publication_date=datetime(2024, 3, 1, 9, 0, tzinfo=UTC),
            beginning_date=datetime(2024, 6, 1, tzinfo=UTC),
            conditions={"duree_contrat": "36 mois"},
        )

        response = jwt_client.get(URL)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            "data": [
                {
                    "reference": "REF-E2E-SUMMARY-1",
                    "isTopOffer": False,
                    "title": "Développeur Backend",
                    "location": "Paris",
                    "modificationDate": "2024-03-01T09:00:00",
                    "contractType": {
                        "code": None,
                        "clientCode": "TERRITORIAL",
                        "label": "TERRITORIAL",
                        "active": True,
                        "parentCode": None,
                        "type": "contractType",
                        "parentType": "",
                        "hasChildren": False,
                    },
                    "offerFamilyCategory": {
                        "code": None,
                        "clientCode": "A",
                        "label": "A",
                        "active": True,
                        "parentCode": None,
                        "type": "offerFamilyCategory",
                        "parentType": "",
                        "hasChildren": False,
                    },
                    "organisationName": "Ministère Test",
                    "organisationDescription": None,
                    "organisationLogoUrl": None,
                    "contractDuration": "36 mois",
                    "contractTypeCountry": None,
                    "description1": "Mission du poste",
                    "description2": "Profil recherché",
                    "description1Formatted": None,
                    "description2Formatted": None,
                    "salaryRange": None,
                    "geographicalLocation": [],
                    "country": [
                        {
                            "code": None,
                            "clientCode": "FRA",
                            "label": "France",
                            "active": True,
                            "parentCode": None,
                            "type": "country",
                            "parentType": "",
                            "hasChildren": False,
                        }
                    ],
                    "region": [
                        {
                            "code": None,
                            "clientCode": "11",
                            "label": "Île-de-France",
                            "active": True,
                            "parentCode": None,
                            "type": "region",
                            "parentType": "",
                            "hasChildren": False,
                        }
                    ],
                    "department": [
                        {
                            "code": None,
                            "clientCode": "75",
                            "label": "Paris",
                            "active": True,
                            "parentCode": None,
                            "type": "department",
                            "parentType": "",
                            "hasChildren": False,
                        }
                    ],
                    "latitude": 48.8566,
                    "longitude": 2.3522,
                    "professionalCategory": None,
                    "_links": [],
                    "offerUrl": "https://exemple.gouv.fr/offres/e2e-1",
                    "_format": None,
                    "_metadata": None,
                    "urlRedirectionEmployee": None,
                    "urlRedirectionApplicant": None,
                    "startPublicationDate": "2024-03-01T09:00:00",
                    "beginningDate": "2024-06-01T00:00:00",
                    "locations": [],
                }
            ],
            "_pagination": {
                "start": 0,
                "count": 1,
                "total": 1,
                "resultsPerPage": 100,
                "hasMore": False,
            },
        }

    def test_organization_filter_includes_child_organizations(self, jwt_client):
        parent = TalentsoftOrganismeDjangoFactory(has_children=True)
        child_b = TalentsoftOrganismeDjangoFactory(parent_code=parent.code)
        child_c = TalentsoftOrganismeDjangoFactory(parent_code=parent.code)
        OfferDjangoFactory(reference="REF-A", talentsoft_organisme_entity_code=parent)
        OfferDjangoFactory(reference="REF-B", talentsoft_organisme_entity_code=child_b)
        OfferDjangoFactory(reference="REF-C", talentsoft_organisme_entity_code=child_c)
        OfferDjangoFactory(
            reference="REF-AUTRE",
            talentsoft_organisme_entity_code=TalentsoftOrganismeDjangoFactory(),
        )

        response = jwt_client.get(URL, {"organization": parent.entity_code})

        assert response.status_code == status.HTTP_200_OK
        references = {offer["reference"] for offer in response.json()["data"]}
        assert references == {"REF-A", "REF-B", "REF-C"}

    def test_does_not_trigger_n_plus_one_queries(
        self, jwt_client, django_assert_num_queries
    ):
        OfferDjangoFactory.create_batch(5)

        with django_assert_num_queries(NOMBRE_REQUETES_ATTENDU):
            response = jwt_client.get(URL)

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.parametrize(
    "start,count",
    [(0, 10), (5, 20), (10, 1)],
)
def test_start_and_count_are_forwarded_to_pagination(
    mock_offer_summaries_container, jwt_client, start, count
):
    mock_usecase = _make_paginated_mock(
        mock_offer_summaries_container, total=100, offers_slice=[]
    )

    response = jwt_client.get(URL, {"start": start, "count": count})

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["_pagination"]["start"] == start
    assert data["_pagination"]["resultsPerPage"] == count
    mock_usecase.execute.return_value.slice.assert_called_once_with(start, count)


def test_has_more_true_when_more_results_exist(
    mock_offer_summaries_container, jwt_client
):
    offers = [OfferFactory.create_entity() for _ in range(2)]
    _make_paginated_mock(mock_offer_summaries_container, total=5, offers_slice=offers)

    response = jwt_client.get(URL, {"start": 0, "count": 2})

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["_pagination"]["hasMore"] is True


def test_category_filter_is_forwarded_to_usecase(
    mock_offer_summaries_container, jwt_client
):
    _make_paginated_mock(mock_offer_summaries_container, total=0, offers_slice=[])

    jwt_client.get(URL, {"category": "A,B"})

    mock_offer_summaries_container.list_offers_usecase.return_value.execute.assert_called_once_with(
        GetFilteredOffersInput(
            active=True,
            category=[Category.A, Category.B],
        )
    )


def test_invalid_category_returns_400(mock_offer_summaries_container, jwt_client):
    _make_paginated_mock(mock_offer_summaries_container, total=0, offers_slice=[])

    response = jwt_client.get(URL, {"category": "INVALID"})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "INVALID" in response.json()["error"]
    assert "A, APLUS, B, C" in response.json()["error"]


def test_verse_filter_is_forwarded_to_usecase(
    mock_offer_summaries_container, jwt_client
):
    _make_paginated_mock(mock_offer_summaries_container, total=0, offers_slice=[])

    jwt_client.get(URL, {"verse": "FPE,FPT"})

    mock_offer_summaries_container.list_offers_usecase.return_value.execute.assert_called_once_with(
        GetFilteredOffersInput(
            active=True,
            verse=[Verse.FPE, Verse.FPT],
        )
    )


def test_invalid_verse_returns_400(mock_offer_summaries_container, jwt_client):
    _make_paginated_mock(mock_offer_summaries_container, total=0, offers_slice=[])

    response = jwt_client.get(URL, {"verse": "INVALID"})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "INVALID" in response.json()["error"]
    assert "FPE, FPH, FPT" in response.json()["error"]


def test_offer_nature_filter_is_forwarded_to_usecase(
    mock_offer_summaries_container, jwt_client
):
    _make_paginated_mock(mock_offer_summaries_container, total=0, offers_slice=[])

    jwt_client.get(URL, {"contractType": "CONTRACTUEL,TERRITORIAL"})

    mock_offer_summaries_container.list_offers_usecase.return_value.execute.assert_called_once_with(
        GetFilteredOffersInput(
            active=True,
            offer_nature=[OfferNature.CONTRACTUEL, OfferNature.TERRITORIAL],
        )
    )


def test_invalid_contract_type_returns_400(mock_offer_summaries_container, jwt_client):
    _make_paginated_mock(mock_offer_summaries_container, total=0, offers_slice=[])

    response = jwt_client.get(URL, {"contractType": "INVALID"})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "INVALID" in response.json()["error"]
    assert "CONTRACTUEL, TERRITORIAL, TITULAIRE_CONTRACTUEL" in response.json()["error"]


def test_experience_level_filter_is_forwarded_to_usecase(
    mock_offer_summaries_container, jwt_client
):
    _make_paginated_mock(mock_offer_summaries_container, total=0, offers_slice=[])

    jwt_client.get(URL, {"experienceLevel": "DEBUTANT,EXPERT"})

    mock_offer_summaries_container.list_offers_usecase.return_value.execute.assert_called_once_with(
        GetFilteredOffersInput(
            active=True,
            experience_level=[ExperienceLevel.DEBUTANT, ExperienceLevel.EXPERT],
        )
    )


def test_invalid_experience_level_returns_400(
    mock_offer_summaries_container, jwt_client
):
    _make_paginated_mock(mock_offer_summaries_container, total=0, offers_slice=[])

    response = jwt_client.get(URL, {"experienceLevel": "INVALID"})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "INVALID" in response.json()["error"]
    assert "CONFIRME, DEBUTANT, EXPERT" in response.json()["error"]


def test_management_filter_is_forwarded_to_usecase(
    mock_offer_summaries_container, jwt_client
):
    _make_paginated_mock(mock_offer_summaries_container, total=0, offers_slice=[])

    jwt_client.get(URL, {"management": "SANS,AVEC"})

    mock_offer_summaries_container.list_offers_usecase.return_value.execute.assert_called_once_with(
        GetFilteredOffersInput(
            active=True,
            management=[Management.SANS, Management.AVEC],
        )
    )


def test_invalid_management_returns_400(mock_offer_summaries_container, jwt_client):
    _make_paginated_mock(mock_offer_summaries_container, total=0, offers_slice=[])

    response = jwt_client.get(URL, {"management": "INVALID"})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "INVALID" in response.json()["error"]
    assert "AVEC, SANS" in response.json()["error"]


def test_working_place_filter_is_forwarded_to_usecase(
    mock_offer_summaries_container, jwt_client
):
    _make_paginated_mock(mock_offer_summaries_container, total=0, offers_slice=[])

    jwt_client.get(URL, {"workingPlace": "SUR_SITE,TELETRAVAIL"})

    mock_offer_summaries_container.list_offers_usecase.return_value.execute.assert_called_once_with(
        GetFilteredOffersInput(
            active=True,
            working_place=[WorkingPlace.SUR_SITE, WorkingPlace.TELETRAVAIL],
        )
    )


def test_invalid_working_place_returns_400(mock_offer_summaries_container, jwt_client):
    _make_paginated_mock(mock_offer_summaries_container, total=0, offers_slice=[])

    response = jwt_client.get(URL, {"workingPlace": "INVALID"})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "INVALID" in response.json()["error"]
    assert "NON_DEFINI, SUR_SITE, TELETRAVAIL" in response.json()["error"]


def test_region_filter_is_forwarded_to_usecase(
    mock_offer_summaries_container, jwt_client
):
    _make_paginated_mock(mock_offer_summaries_container, total=0, offers_slice=[])

    jwt_client.get(URL, {"region": "11,84"})

    mock_offer_summaries_container.list_offers_usecase.return_value.execute.assert_called_once_with(
        GetFilteredOffersInput(
            active=True,
            region=[Region(code="11"), Region(code="84")],
        )
    )


def test_invalid_region_returns_400(mock_offer_summaries_container, jwt_client):
    _make_paginated_mock(mock_offer_summaries_container, total=0, offers_slice=[])

    response = jwt_client.get(URL, {"region": "INVALID"})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "INVALID" in response.json()["error"]


def test_department_filter_is_forwarded_to_usecase(
    mock_offer_summaries_container, jwt_client
):
    _make_paginated_mock(mock_offer_summaries_container, total=0, offers_slice=[])

    jwt_client.get(URL, {"department": "75,69"})

    mock_offer_summaries_container.list_offers_usecase.return_value.execute.assert_called_once_with(
        GetFilteredOffersInput(
            active=True,
            department=[Department(code="75"), Department(code="69")],
        )
    )


def test_invalid_department_returns_400(mock_offer_summaries_container, jwt_client):
    _make_paginated_mock(mock_offer_summaries_container, total=0, offers_slice=[])

    response = jwt_client.get(URL, {"department": "INVALID"})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "INVALID" in response.json()["error"]


def test_country_filter_is_forwarded_to_usecase(
    mock_offer_summaries_container, jwt_client
):
    _make_paginated_mock(mock_offer_summaries_container, total=0, offers_slice=[])

    jwt_client.get(URL, {"country": "fra,bel"})

    mock_offer_summaries_container.list_offers_usecase.return_value.execute.assert_called_once_with(
        GetFilteredOffersInput(
            active=True,
            country=[Country("FRA"), Country("BEL")],
        )
    )


def test_invalid_country_returns_400(mock_offer_summaries_container, jwt_client):
    _make_paginated_mock(mock_offer_summaries_container, total=0, offers_slice=[])

    response = jwt_client.get(URL, {"country": "INVALID"})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "INVALID" in response.json()["error"]


def test_area_filter_is_forwarded_to_usecase(
    mock_offer_summaries_container, jwt_client
):
    _make_paginated_mock(mock_offer_summaries_container, total=0, offers_slice=[])

    jwt_client.get(URL, {"area": "EUROPE,AFRIQUE"})

    mock_offer_summaries_container.list_offers_usecase.return_value.execute.assert_called_once_with(
        GetFilteredOffersInput(
            active=True,
            area=[GeographicalArea.EUROPE, GeographicalArea.AFRIQUE],
        )
    )


def test_invalid_area_returns_400(mock_offer_summaries_container, jwt_client):
    _make_paginated_mock(mock_offer_summaries_container, total=0, offers_slice=[])

    response = jwt_client.get(URL, {"area": "INVALID"})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "INVALID" in response.json()["error"]


def test_domain_filter_is_forwarded_to_usecase(
    mock_offer_summaries_container, jwt_client
):
    _make_paginated_mock(mock_offer_summaries_container, total=0, offers_slice=[])

    jwt_client.get(URL, {"domain": "NUM,ACH"})

    mock_offer_summaries_container.list_offers_usecase.return_value.execute.assert_called_once_with(
        GetFilteredOffersInput(
            active=True,
            domain=[DomaineFonctionnel.NUMERIQUE.value, DomaineFonctionnel.ACHAT.value],
        )
    )


def test_invalid_domain_returns_400(mock_offer_summaries_container, jwt_client):
    _make_paginated_mock(mock_offer_summaries_container, total=0, offers_slice=[])

    response = jwt_client.get(URL, {"domain": "INVALID"})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "INVALID" in response.json()["error"]


def test_organization_filter_is_forwarded_to_usecase(
    mock_offer_summaries_container, jwt_client
):
    _make_paginated_mock(mock_offer_summaries_container, total=0, offers_slice=[])

    jwt_client.get(URL, [("organization", "ORG1")])

    mock_offer_summaries_container.list_offers_usecase.return_value.execute.assert_called_once_with(
        GetFilteredOffersInput(
            active=True,
            organization=["ORG1"],
        )
    )


def test_organization_filter_with_multiple_values_is_forwarded_to_usecase(
    mock_offer_summaries_container, jwt_client
):
    _make_paginated_mock(mock_offer_summaries_container, total=0, offers_slice=[])

    jwt_client.get(
        URL,
        [
            ("organization", "ORG1"),
            ("organization", "ORG2"),
        ],
    )

    mock_offer_summaries_container.list_offers_usecase.return_value.execute.assert_called_once_with(
        GetFilteredOffersInput(
            active=True,
            organization=["ORG1", "ORG2"],
        )
    )


def test_keywords_filter_is_forwarded_to_usecase(
    mock_offer_summaries_container, jwt_client
):
    _make_paginated_mock(mock_offer_summaries_container, total=0, offers_slice=[])

    jwt_client.get(URL, {"keywords": "développeur informatique"})

    mock_offer_summaries_container.list_offers_usecase.return_value.execute.assert_called_once_with(
        GetFilteredOffersInput(
            active=True,
            keywords="développeur informatique",
        )
    )


def test_blank_keywords_is_treated_as_not_provided(
    mock_offer_summaries_container, jwt_client
):
    _make_paginated_mock(mock_offer_summaries_container, total=0, offers_slice=[])

    response = jwt_client.get(URL, {"keywords": ""})

    assert response.status_code == status.HTTP_200_OK
    mock_offer_summaries_container.list_offers_usecase.return_value.execute.assert_called_once_with(
        GetFilteredOffersInput(active=True)
    )


def test_publication_date_filter_is_forwarded_to_usecase(
    mock_offer_summaries_container, jwt_client
):
    _make_paginated_mock(mock_offer_summaries_container, total=0, offers_slice=[])

    jwt_client.get(URL, {"publicationDate": "-7"})

    mock_offer_summaries_container.list_offers_usecase.return_value.execute.assert_called_once_with(
        GetFilteredOffersInput(
            active=True,
            published_within_days=-7,
        )
    )


def test_positive_publication_date_returns_400(
    mock_offer_summaries_container, jwt_client
):
    _make_paginated_mock(mock_offer_summaries_container, total=0, offers_slice=[])

    response = jwt_client.get(URL, {"publicationDate": "7"})

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_geo_filter_is_forwarded_to_usecase(mock_offer_summaries_container, jwt_client):
    _make_paginated_mock(mock_offer_summaries_container, total=0, offers_slice=[])

    jwt_client.get(URL, {"latitude": "48.8566", "longitude": "2.3522", "radius": "10"})

    mock_offer_summaries_container.list_offers_usecase.return_value.execute.assert_called_once_with(
        GetFilteredOffersInput(
            active=True,
            latitude=48.8566,
            longitude=2.3522,
            radius_km=10,
        )
    )


@pytest.mark.parametrize(
    "params",
    [
        {"latitude": "48.8566"},
        {"longitude": "2.3522"},
        {"radius": "10"},
        {"latitude": "48.8566", "longitude": "2.3522"},
        {"latitude": "48.8566", "radius": "10"},
        {"longitude": "2.3522", "radius": "10"},
    ],
)
def test_partial_geo_filter_returns_400(
    mock_offer_summaries_container, jwt_client, params
):
    _make_paginated_mock(mock_offer_summaries_container, total=0, offers_slice=[])

    response = jwt_client.get(URL, params)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_radius_below_one_returns_400(mock_offer_summaries_container, jwt_client):
    _make_paginated_mock(mock_offer_summaries_container, total=0, offers_slice=[])

    response = jwt_client.get(
        URL, {"latitude": "48.8566", "longitude": "2.3522", "radius": "0"}
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_non_integer_radius_returns_400(mock_offer_summaries_container, jwt_client):
    _make_paginated_mock(mock_offer_summaries_container, total=0, offers_slice=[])

    response = jwt_client.get(
        URL, {"latitude": "48.8566", "longitude": "2.3522", "radius": "10.5"}
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.parametrize(
    "params",
    [
        {"latitude": "-91", "longitude": "2.3522", "radius": "10"},
        {"latitude": "48.8566", "longitude": "181", "radius": "10"},
    ],
)
def test_out_of_range_lat_lon_returns_400(
    mock_offer_summaries_container, jwt_client, params
):
    _make_paginated_mock(mock_offer_summaries_container, total=0, offers_slice=[])

    response = jwt_client.get(URL, params)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_returns_error_500(mock_offer_summaries_container, jwt_client):
    mock_usecase = MagicMock()
    mock_usecase.execute.side_effect = Exception("db error")
    mock_offer_summaries_container.list_offers_usecase.return_value = mock_usecase

    response = jwt_client.get(URL)
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
