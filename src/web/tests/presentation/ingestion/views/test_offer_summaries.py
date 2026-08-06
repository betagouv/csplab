from unittest.mock import MagicMock

import pytest
from django.urls import reverse
from drf_spectacular.generators import SchemaGenerator
from referentiel.value_objects.category import Category
from referentiel.value_objects.contract_type import ContractType
from referentiel.value_objects.country import Country
from referentiel.value_objects.department import Department
from referentiel.value_objects.domaine_fonctionnel import DomaineFonctionnel
from referentiel.value_objects.experience_level import ExperienceLevel
from referentiel.value_objects.offer_conditions import Management, WorkingPlace
from referentiel.value_objects.region import Region
from referentiel.value_objects.verse import Verse
from rest_framework import status

from application.ingestion.interfaces.list_offers_input import GetFilteredOffersInput
from infrastructure.factories.referentiel.offer_factory import OfferFactory

URL = reverse("ingestion_fake_ts:offer_summaries")


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


def test_post_not_allowed(authenticated_client):
    response = authenticated_client.post(URL)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_empty_result(mock_offer_summaries_container, authenticated_client):
    _make_paginated_mock(mock_offer_summaries_container, total=0, offers_slice=[])

    response = authenticated_client.get(URL)

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


def test_only_queries_non_archived_offers(
    mock_offer_summaries_container, authenticated_client
):
    _make_paginated_mock(mock_offer_summaries_container, total=0, offers_slice=[])

    authenticated_client.get(URL)

    mock_offer_summaries_container.list_offers_usecase.return_value.execute.assert_called_once_with(
        GetFilteredOffersInput(active=True, external_id_contains=None)
    )


def test_call_without_arg(mock_offer_summaries_container, authenticated_client):
    offer = OfferFactory.create_entity(
        contract_type=ContractType.TERRITORIAL,
        category=Category.A,
    )
    _make_paginated_mock(mock_offer_summaries_container, total=1, offers_slice=[offer])

    response = authenticated_client.get(URL)

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
    assert result["contractType"]["clientCode"] == offer.contract_type.name
    assert result["contractType"]["label"] == offer.contract_type.value
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


@pytest.mark.parametrize(
    "start,count",
    [(0, 10), (5, 20), (10, 1)],
)
def test_start_and_count_are_forwarded_to_pagination(
    mock_offer_summaries_container, authenticated_client, start, count
):
    mock_usecase = _make_paginated_mock(
        mock_offer_summaries_container, total=100, offers_slice=[]
    )

    response = authenticated_client.get(URL, {"start": start, "count": count})

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["_pagination"]["start"] == start
    assert data["_pagination"]["resultsPerPage"] == count
    mock_usecase.execute.return_value.slice.assert_called_once_with(start, count)


def test_has_more_true_when_more_results_exist(
    mock_offer_summaries_container, authenticated_client
):
    offers = [OfferFactory.create_entity() for _ in range(2)]
    _make_paginated_mock(mock_offer_summaries_container, total=5, offers_slice=offers)

    response = authenticated_client.get(URL, {"start": 0, "count": 2})

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["_pagination"]["hasMore"] is True


def test_category_filter_is_forwarded_to_usecase(
    mock_offer_summaries_container, authenticated_client
):
    _make_paginated_mock(mock_offer_summaries_container, total=0, offers_slice=[])

    authenticated_client.get(URL, {"category": "A,B"})

    mock_offer_summaries_container.list_offers_usecase.return_value.execute.assert_called_once_with(
        GetFilteredOffersInput(
            active=True,
            external_id_contains=None,
            category=[Category.A, Category.B],
        )
    )


def test_invalid_category_returns_400(
    mock_offer_summaries_container, authenticated_client
):
    _make_paginated_mock(mock_offer_summaries_container, total=0, offers_slice=[])

    response = authenticated_client.get(URL, {"category": "INVALID"})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "INVALID" in response.json()["error"]
    assert "A, APLUS, B, C" in response.json()["error"]


def test_verse_filter_is_forwarded_to_usecase(
    mock_offer_summaries_container, authenticated_client
):
    _make_paginated_mock(mock_offer_summaries_container, total=0, offers_slice=[])

    authenticated_client.get(URL, {"verse": "FPE,FPT"})

    mock_offer_summaries_container.list_offers_usecase.return_value.execute.assert_called_once_with(
        GetFilteredOffersInput(
            active=True,
            external_id_contains=None,
            verse=[Verse.FPE, Verse.FPT],
        )
    )


def test_invalid_verse_returns_400(
    mock_offer_summaries_container, authenticated_client
):
    _make_paginated_mock(mock_offer_summaries_container, total=0, offers_slice=[])

    response = authenticated_client.get(URL, {"verse": "INVALID"})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "INVALID" in response.json()["error"]
    assert "FPE, FPH, FPT" in response.json()["error"]


def test_contract_type_filter_is_forwarded_to_usecase(
    mock_offer_summaries_container, authenticated_client
):
    _make_paginated_mock(mock_offer_summaries_container, total=0, offers_slice=[])

    authenticated_client.get(URL, {"contractType": "CONTRACTUELS,TERRITORIAL"})

    mock_offer_summaries_container.list_offers_usecase.return_value.execute.assert_called_once_with(
        GetFilteredOffersInput(
            active=True,
            external_id_contains=None,
            contract_type=[ContractType.CONTRACTUELS, ContractType.TERRITORIAL],
        )
    )


def test_invalid_contract_type_returns_400(
    mock_offer_summaries_container, authenticated_client
):
    _make_paginated_mock(mock_offer_summaries_container, total=0, offers_slice=[])

    response = authenticated_client.get(URL, {"contractType": "INVALID"})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "INVALID" in response.json()["error"]
    assert (
        "CONTRACTUELS, TERRITORIAL, TITULAIRE_CONTRACTUEL" in response.json()["error"]
    )


def test_experience_level_filter_is_forwarded_to_usecase(
    mock_offer_summaries_container, authenticated_client
):
    _make_paginated_mock(mock_offer_summaries_container, total=0, offers_slice=[])

    authenticated_client.get(URL, {"experienceLevel": "DEBUTANT,EXPERT"})

    mock_offer_summaries_container.list_offers_usecase.return_value.execute.assert_called_once_with(
        GetFilteredOffersInput(
            active=True,
            external_id_contains=None,
            experience_level=[ExperienceLevel.DEBUTANT, ExperienceLevel.EXPERT],
        )
    )


def test_invalid_experience_level_returns_400(
    mock_offer_summaries_container, authenticated_client
):
    _make_paginated_mock(mock_offer_summaries_container, total=0, offers_slice=[])

    response = authenticated_client.get(URL, {"experienceLevel": "INVALID"})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "INVALID" in response.json()["error"]
    assert "CONFIRME, DEBUTANT, EXPERT" in response.json()["error"]


def test_management_filter_is_forwarded_to_usecase(
    mock_offer_summaries_container, authenticated_client
):
    _make_paginated_mock(mock_offer_summaries_container, total=0, offers_slice=[])

    authenticated_client.get(URL, {"management": "SANS,AVEC"})

    mock_offer_summaries_container.list_offers_usecase.return_value.execute.assert_called_once_with(
        GetFilteredOffersInput(
            active=True,
            external_id_contains=None,
            management=[Management.SANS, Management.AVEC],
        )
    )


def test_invalid_management_returns_400(
    mock_offer_summaries_container, authenticated_client
):
    _make_paginated_mock(mock_offer_summaries_container, total=0, offers_slice=[])

    response = authenticated_client.get(URL, {"management": "INVALID"})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "INVALID" in response.json()["error"]
    assert "AVEC, SANS" in response.json()["error"]


def test_working_place_filter_is_forwarded_to_usecase(
    mock_offer_summaries_container, authenticated_client
):
    _make_paginated_mock(mock_offer_summaries_container, total=0, offers_slice=[])

    authenticated_client.get(URL, {"workingPlace": "SUR_SITE,TELETRAVAIL"})

    mock_offer_summaries_container.list_offers_usecase.return_value.execute.assert_called_once_with(
        GetFilteredOffersInput(
            active=True,
            external_id_contains=None,
            working_place=[WorkingPlace.SUR_SITE, WorkingPlace.TELETRAVAIL],
        )
    )


def test_invalid_working_place_returns_400(
    mock_offer_summaries_container, authenticated_client
):
    _make_paginated_mock(mock_offer_summaries_container, total=0, offers_slice=[])

    response = authenticated_client.get(URL, {"workingPlace": "INVALID"})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "INVALID" in response.json()["error"]
    assert "NON_DEFINI, SUR_SITE, TELETRAVAIL" in response.json()["error"]


def test_region_filter_is_forwarded_to_usecase(
    mock_offer_summaries_container, authenticated_client
):
    _make_paginated_mock(mock_offer_summaries_container, total=0, offers_slice=[])

    authenticated_client.get(URL, {"region": "11,84"})

    mock_offer_summaries_container.list_offers_usecase.return_value.execute.assert_called_once_with(
        GetFilteredOffersInput(
            active=True,
            external_id_contains=None,
            region=[Region(code="11"), Region(code="84")],
        )
    )


def test_invalid_region_returns_400(
    mock_offer_summaries_container, authenticated_client
):
    _make_paginated_mock(mock_offer_summaries_container, total=0, offers_slice=[])

    response = authenticated_client.get(URL, {"region": "INVALID"})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "INVALID" in response.json()["error"]


def test_department_filter_is_forwarded_to_usecase(
    mock_offer_summaries_container, authenticated_client
):
    _make_paginated_mock(mock_offer_summaries_container, total=0, offers_slice=[])

    authenticated_client.get(URL, {"department": "75,69"})

    mock_offer_summaries_container.list_offers_usecase.return_value.execute.assert_called_once_with(
        GetFilteredOffersInput(
            active=True,
            external_id_contains=None,
            department=[Department(code="75"), Department(code="69")],
        )
    )


def test_invalid_department_returns_400(
    mock_offer_summaries_container, authenticated_client
):
    _make_paginated_mock(mock_offer_summaries_container, total=0, offers_slice=[])

    response = authenticated_client.get(URL, {"department": "INVALID"})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "INVALID" in response.json()["error"]


def test_country_filter_is_forwarded_to_usecase(
    mock_offer_summaries_container, authenticated_client
):
    _make_paginated_mock(mock_offer_summaries_container, total=0, offers_slice=[])

    authenticated_client.get(URL, {"country": "fra,bel"})

    mock_offer_summaries_container.list_offers_usecase.return_value.execute.assert_called_once_with(
        GetFilteredOffersInput(
            active=True,
            external_id_contains=None,
            country=[Country("FRA"), Country("BEL")],
        )
    )


def test_invalid_country_returns_400(
    mock_offer_summaries_container, authenticated_client
):
    _make_paginated_mock(mock_offer_summaries_container, total=0, offers_slice=[])

    response = authenticated_client.get(URL, {"country": "INVALID"})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "INVALID" in response.json()["error"]


def test_domain_filter_is_forwarded_to_usecase(
    mock_offer_summaries_container, authenticated_client
):
    _make_paginated_mock(mock_offer_summaries_container, total=0, offers_slice=[])

    authenticated_client.get(URL, {"domain": "NUM,ACH"})

    mock_offer_summaries_container.list_offers_usecase.return_value.execute.assert_called_once_with(
        GetFilteredOffersInput(
            active=True,
            external_id_contains=None,
            domain=[DomaineFonctionnel.NUMERIQUE.value, DomaineFonctionnel.ACHAT.value],
        )
    )


def test_invalid_domain_returns_400(
    mock_offer_summaries_container, authenticated_client
):
    _make_paginated_mock(mock_offer_summaries_container, total=0, offers_slice=[])

    response = authenticated_client.get(URL, {"domain": "INVALID"})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "INVALID" in response.json()["error"]


def test_organization_filter_is_forwarded_to_usecase(
    mock_offer_summaries_container, authenticated_client
):
    _make_paginated_mock(mock_offer_summaries_container, total=0, offers_slice=[])

    authenticated_client.get(URL, [("organization", "Mairie de Paris")])

    mock_offer_summaries_container.list_offers_usecase.return_value.execute.assert_called_once_with(
        GetFilteredOffersInput(
            active=True,
            external_id_contains=None,
            organization=["Mairie de Paris"],
        )
    )


def test_organization_filter_with_multiple_values_is_forwarded_to_usecase(
    mock_offer_summaries_container, authenticated_client
):
    _make_paginated_mock(mock_offer_summaries_container, total=0, offers_slice=[])

    authenticated_client.get(
        URL,
        [
            ("organization", "Mairie de Paris"),
            ("organization", "Société Générale, SA"),
        ],
    )

    mock_offer_summaries_container.list_offers_usecase.return_value.execute.assert_called_once_with(
        GetFilteredOffersInput(
            active=True,
            external_id_contains=None,
            organization=["Mairie de Paris", "Société Générale, SA"],
        )
    )


def test_keywords_filter_is_forwarded_to_usecase(
    mock_offer_summaries_container, authenticated_client
):
    _make_paginated_mock(mock_offer_summaries_container, total=0, offers_slice=[])

    authenticated_client.get(URL, {"keywords": "développeur informatique"})

    mock_offer_summaries_container.list_offers_usecase.return_value.execute.assert_called_once_with(
        GetFilteredOffersInput(
            active=True,
            external_id_contains=None,
            keywords="développeur informatique",
        )
    )


def test_blank_keywords_is_treated_as_not_provided(
    mock_offer_summaries_container, authenticated_client
):
    _make_paginated_mock(mock_offer_summaries_container, total=0, offers_slice=[])

    response = authenticated_client.get(URL, {"keywords": ""})

    assert response.status_code == status.HTTP_200_OK
    mock_offer_summaries_container.list_offers_usecase.return_value.execute.assert_called_once_with(
        GetFilteredOffersInput(active=True, external_id_contains=None)
    )


def test_publication_date_filter_is_forwarded_to_usecase(
    mock_offer_summaries_container, authenticated_client
):
    _make_paginated_mock(mock_offer_summaries_container, total=0, offers_slice=[])

    authenticated_client.get(URL, {"publicationDate": "-7"})

    mock_offer_summaries_container.list_offers_usecase.return_value.execute.assert_called_once_with(
        GetFilteredOffersInput(
            active=True,
            external_id_contains=None,
            published_within_days=-7,
        )
    )


def test_positive_publication_date_returns_400(
    mock_offer_summaries_container, authenticated_client
):
    _make_paginated_mock(mock_offer_summaries_container, total=0, offers_slice=[])

    response = authenticated_client.get(URL, {"publicationDate": "7"})

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_geo_filter_is_forwarded_to_usecase(
    mock_offer_summaries_container, authenticated_client
):
    _make_paginated_mock(mock_offer_summaries_container, total=0, offers_slice=[])

    authenticated_client.get(
        URL, {"latitude": "48.8566", "longitude": "2.3522", "radius": "10"}
    )

    mock_offer_summaries_container.list_offers_usecase.return_value.execute.assert_called_once_with(
        GetFilteredOffersInput(
            active=True,
            external_id_contains=None,
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
    mock_offer_summaries_container, authenticated_client, params
):
    _make_paginated_mock(mock_offer_summaries_container, total=0, offers_slice=[])

    response = authenticated_client.get(URL, params)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_radius_below_one_returns_400(
    mock_offer_summaries_container, authenticated_client
):
    _make_paginated_mock(mock_offer_summaries_container, total=0, offers_slice=[])

    response = authenticated_client.get(
        URL, {"latitude": "48.8566", "longitude": "2.3522", "radius": "0"}
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_non_integer_radius_returns_400(
    mock_offer_summaries_container, authenticated_client
):
    _make_paginated_mock(mock_offer_summaries_container, total=0, offers_slice=[])

    response = authenticated_client.get(
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
    mock_offer_summaries_container, authenticated_client, params
):
    _make_paginated_mock(mock_offer_summaries_container, total=0, offers_slice=[])

    response = authenticated_client.get(URL, params)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_returns_error_500(mock_offer_summaries_container, authenticated_client):
    mock_usecase = MagicMock()
    mock_usecase.execute.side_effect = Exception("db error")
    mock_offer_summaries_container.list_offers_usecase.return_value = mock_usecase

    response = authenticated_client.get(URL)
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR


def test_is_excluded_from_openapi_schema():
    generator = SchemaGenerator()
    schema = generator.get_schema(request=None, public=True)
    assert "/api/fake-ts/offersummaries" not in schema["paths"]
