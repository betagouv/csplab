from datetime import datetime
from unittest.mock import MagicMock, patch
from urllib.parse import parse_qs, urlparse

import pytest
from django.urls import reverse
from faker import Faker
from referentiel.value_objects.area import GeographicalArea
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

fake = Faker()
URL = reverse("ingestion:offers_list")


def test_unauthenticated_access(api_client):
    response = api_client.get(URL)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_authenticated_access(authenticated_client):
    response = authenticated_client.get(URL)
    assert response.status_code == status.HTTP_200_OK


def test_logged_user_access_without_token_is_rejected(api_client, test_user):
    api_client.force_login(test_user)
    response = api_client.get(URL)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_invalid_api_key_returns_401(api_client):
    api_client.credentials(HTTP_AUTHORIZATION="Api-Key wrong-key")
    response = api_client.get(URL)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_api_key_authentication_access(mock_offers_container, api_key_client):
    _make_paginated_mock(mock_offers_container, num_offers=0, offers_slice=[])
    response = api_key_client.get(URL)
    assert response.status_code == status.HTTP_200_OK


def test_post_not_allowed(authenticated_client):
    response = authenticated_client.post(URL)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def _make_paginated_mock(mock_offers_container, num_offers, offers_slice):
    mock_page = MagicMock()
    mock_page.count.return_value = num_offers
    mock_page.slice.return_value = iter(offers_slice)

    mock_usecase = MagicMock()
    mock_usecase.execute.return_value = mock_page
    mock_offers_container.list_offers_usecase.return_value = mock_usecase

    return mock_usecase


def test_empty_result(mock_offers_container, authenticated_client, list_offers_usecase):
    _make_paginated_mock(mock_offers_container, num_offers=0, offers_slice=[])

    response = authenticated_client.get(URL)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "count": 0,
        "next": None,
        "previous": None,
        "results": [],
    }


def test_call_without_arg(mock_offers_container, authenticated_client):
    first_offer = OfferFactory.create_entity(
        contract_type=ContractType.TERRITORIAL,
        offer_url=fake.url(),
        archived_at=datetime.now(),
    )
    second_offer = OfferFactory.create_entity()
    offers = [first_offer, second_offer]

    _make_paginated_mock(
        mock_offers_container, num_offers=len(offers), offers_slice=offers
    )

    response = authenticated_client.get(URL)

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data["count"] == len(offers)
    assert data["next"] is None
    assert data["previous"] is None

    for result, offer in zip(data["results"], offers, strict=True):
        assert result["external_id"] == offer.external_id
        assert result["reference"] == offer.reference
        assert result["source_id"] == str(offer.source_id)
        assert result["title"] == offer.title
        assert result["organization"] == offer.organization
        assert result["contract_type"] == (
            offer.contract_type.value if offer.contract_type else None
        )
        assert result["category"] == offer.category.value
        assert result["publication_date"] == "2024-01-15T00:00:00Z"
        assert result["offer_url"] == offer.offer_url
        if offer.archived_at:
            assert result["archived_at"] == offer.archived_at.isoformat(
                timespec="microseconds"
            ).replace("+00:00", "Z")
        else:
            assert result["archived_at"] is None


@pytest.mark.parametrize("active", [True, False])
def test_call_with_args(mock_offers_container, authenticated_client, active):
    _make_paginated_mock(mock_offers_container, num_offers=0, offers_slice=[])

    authenticated_client.get(URL, {"actif": active})

    mock_offers_container.list_offers_usecase.return_value.execute.assert_called_once_with(
        GetFilteredOffersInput(active=active, external_id_contains=None)
    )


def test_external_id_contains_is_not_accepted(
    mock_offers_container, authenticated_client
):
    _make_paginated_mock(mock_offers_container, num_offers=0, offers_slice=[])

    authenticated_client.get(URL, {"external_id_contains": "123"})

    mock_offers_container.list_offers_usecase.return_value.execute.assert_called_once_with(
        GetFilteredOffersInput(active=True, external_id_contains=None)
    )


def test_category_filter_is_forwarded_to_usecase(
    mock_offers_container, authenticated_client
):
    _make_paginated_mock(mock_offers_container, num_offers=0, offers_slice=[])

    authenticated_client.get(URL, {"categorie": "A,B"})

    mock_offers_container.list_offers_usecase.return_value.execute.assert_called_once_with(
        GetFilteredOffersInput(
            active=True,
            external_id_contains=None,
            category=[Category.A, Category.B],
        )
    )


def test_invalid_category_returns_400(mock_offers_container, authenticated_client):
    _make_paginated_mock(mock_offers_container, num_offers=0, offers_slice=[])

    response = authenticated_client.get(URL, {"categorie": "INVALID"})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "INVALID" in response.json()["error"]
    assert "A, APLUS, B, C" in response.json()["error"]


def test_verse_filter_is_forwarded_to_usecase(
    mock_offers_container, authenticated_client
):
    _make_paginated_mock(mock_offers_container, num_offers=0, offers_slice=[])

    authenticated_client.get(URL, {"versant": "FPE,FPT"})

    mock_offers_container.list_offers_usecase.return_value.execute.assert_called_once_with(
        GetFilteredOffersInput(
            active=True,
            external_id_contains=None,
            verse=[Verse.FPE, Verse.FPT],
        )
    )


def test_invalid_verse_returns_400(mock_offers_container, authenticated_client):
    _make_paginated_mock(mock_offers_container, num_offers=0, offers_slice=[])

    response = authenticated_client.get(URL, {"versant": "INVALID"})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "INVALID" in response.json()["error"]
    assert "FPE, FPH, FPT" in response.json()["error"]


def test_contract_type_filter_is_forwarded_to_usecase(
    mock_offers_container, authenticated_client
):
    _make_paginated_mock(mock_offers_container, num_offers=0, offers_slice=[])

    authenticated_client.get(URL, {"type_contrat": "CONTRACTUELS,TERRITORIAL"})

    mock_offers_container.list_offers_usecase.return_value.execute.assert_called_once_with(
        GetFilteredOffersInput(
            active=True,
            external_id_contains=None,
            contract_type=[ContractType.CONTRACTUELS, ContractType.TERRITORIAL],
        )
    )


def test_invalid_contract_type_returns_400(mock_offers_container, authenticated_client):
    _make_paginated_mock(mock_offers_container, num_offers=0, offers_slice=[])

    response = authenticated_client.get(URL, {"type_contrat": "INVALID"})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "INVALID" in response.json()["error"]
    assert (
        "CONTRACTUELS, TERRITORIAL, TITULAIRE_CONTRACTUEL" in response.json()["error"]
    )


def test_experience_level_filter_is_forwarded_to_usecase(
    mock_offers_container, authenticated_client
):
    _make_paginated_mock(mock_offers_container, num_offers=0, offers_slice=[])

    authenticated_client.get(URL, {"niveau_experience": "DEBUTANT,EXPERT"})

    mock_offers_container.list_offers_usecase.return_value.execute.assert_called_once_with(
        GetFilteredOffersInput(
            active=True,
            external_id_contains=None,
            experience_level=[ExperienceLevel.DEBUTANT, ExperienceLevel.EXPERT],
        )
    )


def test_invalid_experience_level_returns_400(
    mock_offers_container, authenticated_client
):
    _make_paginated_mock(mock_offers_container, num_offers=0, offers_slice=[])

    response = authenticated_client.get(URL, {"niveau_experience": "INVALID"})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "INVALID" in response.json()["error"]
    assert "CONFIRME, DEBUTANT, EXPERT" in response.json()["error"]


def test_management_filter_is_forwarded_to_usecase(
    mock_offers_container, authenticated_client
):
    _make_paginated_mock(mock_offers_container, num_offers=0, offers_slice=[])

    authenticated_client.get(URL, {"management": "SANS,AVEC"})

    mock_offers_container.list_offers_usecase.return_value.execute.assert_called_once_with(
        GetFilteredOffersInput(
            active=True,
            external_id_contains=None,
            management=[Management.SANS, Management.AVEC],
        )
    )


def test_invalid_management_returns_400(mock_offers_container, authenticated_client):
    _make_paginated_mock(mock_offers_container, num_offers=0, offers_slice=[])

    response = authenticated_client.get(URL, {"management": "INVALID"})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "INVALID" in response.json()["error"]
    assert "AVEC, SANS" in response.json()["error"]


def test_working_place_filter_is_forwarded_to_usecase(
    mock_offers_container, authenticated_client
):
    _make_paginated_mock(mock_offers_container, num_offers=0, offers_slice=[])

    authenticated_client.get(URL, {"lieu_de_travail": "SUR_SITE,TELETRAVAIL"})

    mock_offers_container.list_offers_usecase.return_value.execute.assert_called_once_with(
        GetFilteredOffersInput(
            active=True,
            external_id_contains=None,
            working_place=[WorkingPlace.SUR_SITE, WorkingPlace.TELETRAVAIL],
        )
    )


def test_invalid_working_place_returns_400(mock_offers_container, authenticated_client):
    _make_paginated_mock(mock_offers_container, num_offers=0, offers_slice=[])

    response = authenticated_client.get(URL, {"lieu_de_travail": "INVALID"})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "INVALID" in response.json()["error"]
    assert "NON_DEFINI, SUR_SITE, TELETRAVAIL" in response.json()["error"]


def test_region_filter_is_forwarded_to_usecase(
    mock_offers_container, authenticated_client
):
    _make_paginated_mock(mock_offers_container, num_offers=0, offers_slice=[])

    authenticated_client.get(URL, {"region": "11,84"})

    mock_offers_container.list_offers_usecase.return_value.execute.assert_called_once_with(
        GetFilteredOffersInput(
            active=True,
            external_id_contains=None,
            region=[Region(code="11"), Region(code="84")],
        )
    )


def test_invalid_region_returns_400(mock_offers_container, authenticated_client):
    _make_paginated_mock(mock_offers_container, num_offers=0, offers_slice=[])

    response = authenticated_client.get(URL, {"region": "INVALID"})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "INVALID" in response.json()["error"]


def test_departement_filter_is_forwarded_to_usecase(
    mock_offers_container, authenticated_client
):
    _make_paginated_mock(mock_offers_container, num_offers=0, offers_slice=[])

    authenticated_client.get(URL, {"departement": "75,69"})

    mock_offers_container.list_offers_usecase.return_value.execute.assert_called_once_with(
        GetFilteredOffersInput(
            active=True,
            external_id_contains=None,
            department=[Department(code="75"), Department(code="69")],
        )
    )


def test_invalid_departement_returns_400(mock_offers_container, authenticated_client):
    _make_paginated_mock(mock_offers_container, num_offers=0, offers_slice=[])

    response = authenticated_client.get(URL, {"departement": "INVALID"})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "INVALID" in response.json()["error"]


def test_pays_filter_is_forwarded_to_usecase(
    mock_offers_container, authenticated_client
):
    _make_paginated_mock(mock_offers_container, num_offers=0, offers_slice=[])

    authenticated_client.get(URL, {"pays": "fra,bel"})

    mock_offers_container.list_offers_usecase.return_value.execute.assert_called_once_with(
        GetFilteredOffersInput(
            active=True,
            external_id_contains=None,
            country=[Country("FRA"), Country("BEL")],
        )
    )


def test_invalid_pays_returns_400(mock_offers_container, authenticated_client):
    _make_paginated_mock(mock_offers_container, num_offers=0, offers_slice=[])

    response = authenticated_client.get(URL, {"pays": "INVALID"})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "INVALID" in response.json()["error"]


def test_zone_filter_is_forwarded_to_usecase(
    mock_offers_container, authenticated_client
):
    _make_paginated_mock(mock_offers_container, num_offers=0, offers_slice=[])

    authenticated_client.get(URL, {"zone": "EUROPE,AFRIQUE"})

    mock_offers_container.list_offers_usecase.return_value.execute.assert_called_once_with(
        GetFilteredOffersInput(
            active=True,
            external_id_contains=None,
            area=[GeographicalArea.EUROPE, GeographicalArea.AFRIQUE],
        )
    )


def test_invalid_zone_returns_400(mock_offers_container, authenticated_client):
    _make_paginated_mock(mock_offers_container, num_offers=0, offers_slice=[])

    response = authenticated_client.get(URL, {"zone": "INVALID"})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "INVALID" in response.json()["error"]


def test_domaine_filter_is_forwarded_to_usecase(
    mock_offers_container, authenticated_client
):
    _make_paginated_mock(mock_offers_container, num_offers=0, offers_slice=[])

    authenticated_client.get(URL, {"domaine": "NUM,ACH"})

    mock_offers_container.list_offers_usecase.return_value.execute.assert_called_once_with(
        GetFilteredOffersInput(
            active=True,
            external_id_contains=None,
            domain=[DomaineFonctionnel.NUMERIQUE.value, DomaineFonctionnel.ACHAT.value],
        )
    )


def test_invalid_domaine_returns_400(mock_offers_container, authenticated_client):
    _make_paginated_mock(mock_offers_container, num_offers=0, offers_slice=[])

    response = authenticated_client.get(URL, {"domaine": "INVALID"})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "INVALID" in response.json()["error"]


def test_organisme_filter_is_forwarded_to_usecase(
    mock_offers_container, authenticated_client
):
    _make_paginated_mock(mock_offers_container, num_offers=0, offers_slice=[])

    authenticated_client.get(URL, [("organisme", "Mairie de Paris")])

    mock_offers_container.list_offers_usecase.return_value.execute.assert_called_once_with(
        GetFilteredOffersInput(
            active=True,
            external_id_contains=None,
            organization=["Mairie de Paris"],
        )
    )


def test_organisme_filter_with_multiple_values_is_forwarded_to_usecase(
    mock_offers_container, authenticated_client
):
    _make_paginated_mock(mock_offers_container, num_offers=0, offers_slice=[])

    authenticated_client.get(
        URL,
        [
            ("organisme", "Mairie de Paris"),
            ("organisme", "Société Générale, SA"),
        ],
    )

    mock_offers_container.list_offers_usecase.return_value.execute.assert_called_once_with(
        GetFilteredOffersInput(
            active=True,
            external_id_contains=None,
            organization=["Mairie de Paris", "Société Générale, SA"],
        )
    )


def test_keywords_filter_is_forwarded_to_usecase(
    mock_offers_container, authenticated_client
):
    _make_paginated_mock(mock_offers_container, num_offers=0, offers_slice=[])

    authenticated_client.get(URL, {"mots_cles": "développeur informatique"})

    mock_offers_container.list_offers_usecase.return_value.execute.assert_called_once_with(
        GetFilteredOffersInput(
            active=True,
            external_id_contains=None,
            keywords="développeur informatique",
        )
    )


def test_blank_keywords_is_treated_as_not_provided(
    mock_offers_container, authenticated_client
):
    _make_paginated_mock(mock_offers_container, num_offers=0, offers_slice=[])

    response = authenticated_client.get(URL, {"mots_cles": ""})

    assert response.status_code == status.HTTP_200_OK
    mock_offers_container.list_offers_usecase.return_value.execute.assert_called_once_with(
        GetFilteredOffersInput(active=True, external_id_contains=None)
    )


def test_date_publication_filter_is_forwarded_to_usecase(
    mock_offers_container, authenticated_client
):
    _make_paginated_mock(mock_offers_container, num_offers=0, offers_slice=[])

    authenticated_client.get(URL, {"date_publication": "-7"})

    mock_offers_container.list_offers_usecase.return_value.execute.assert_called_once_with(
        GetFilteredOffersInput(
            active=True,
            external_id_contains=None,
            published_within_days=-7,
        )
    )


def test_positive_date_publication_returns_400(
    mock_offers_container, authenticated_client
):
    _make_paginated_mock(mock_offers_container, num_offers=0, offers_slice=[])

    response = authenticated_client.get(URL, {"date_publication": "7"})

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_geo_filter_is_forwarded_to_usecase(
    mock_offers_container, authenticated_client
):
    _make_paginated_mock(mock_offers_container, num_offers=0, offers_slice=[])

    authenticated_client.get(
        URL, {"latitude": "48.8566", "longitude": "2.3522", "radius": "10"}
    )

    mock_offers_container.list_offers_usecase.return_value.execute.assert_called_once_with(
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
    mock_offers_container, authenticated_client, params
):
    _make_paginated_mock(mock_offers_container, num_offers=0, offers_slice=[])

    response = authenticated_client.get(URL, params)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_radius_below_one_returns_400(mock_offers_container, authenticated_client):
    _make_paginated_mock(mock_offers_container, num_offers=0, offers_slice=[])

    response = authenticated_client.get(
        URL, {"latitude": "48.8566", "longitude": "2.3522", "radius": "0"}
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_non_integer_radius_returns_400(mock_offers_container, authenticated_client):
    _make_paginated_mock(mock_offers_container, num_offers=0, offers_slice=[])

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
    mock_offers_container, authenticated_client, params
):
    _make_paginated_mock(mock_offers_container, num_offers=0, offers_slice=[])

    response = authenticated_client.get(URL, params)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_returns_error_500(mock_offers_container, authenticated_client):
    mock_usecase = MagicMock()
    mock_usecase.execute.side_effect = Exception("db error")
    mock_offers_container.list_offers_usecase.return_value = mock_usecase

    response = authenticated_client.get(URL)
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR


@patch("presentation.ingestion.views.offers.WebPagination.page_size", new=2)
def test_pagination_page_arg(mock_offers_container, authenticated_client):
    num_offers = 5
    offers = [OfferFactory.create_entity() for _ in range(num_offers)]

    _make_paginated_mock(
        mock_offers_container, num_offers=len(offers), offers_slice=offers[2:4]
    )

    response = authenticated_client.get(URL, {"page": 2, "dummy": "arg", "actif": 1})

    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert data["count"] == num_offers
    assert len(data["results"]) == 2  # noqa

    parsed_previous = urlparse(data["previous"])
    assert parsed_previous.path == URL
    assert parse_qs(parsed_previous.query) == {
        "page": ["1"],
        "dummy": ["arg"],
        "actif": ["1"],
        "taille": ["2"],
    }

    parsed_next = urlparse(data["next"])
    assert parsed_next.path == URL
    assert parse_qs(parsed_next.query) == {
        "page": ["3"],
        "dummy": ["arg"],
        "actif": ["1"],
        "taille": ["2"],
    }


@patch("presentation.ingestion.views.offers.WebPagination.page_size", new=2)
def test_pagination_out_of_bond(mock_offers_container, authenticated_client):
    num_offers = 3
    offers = [OfferFactory.create_entity() for _ in range(num_offers)]

    _make_paginated_mock(mock_offers_container, num_offers=len(offers), offers_slice=[])

    response = authenticated_client.get(URL, {"page": 3})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert data["count"] == num_offers
    assert data["results"] == []

    parsed = urlparse(data["previous"])
    assert parsed.path == URL
    assert parse_qs(parsed.query) == {
        "page": ["2"],
        "taille": ["2"],
    }

    assert data["next"] is None
