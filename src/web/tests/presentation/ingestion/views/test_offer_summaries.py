from unittest.mock import MagicMock

import pytest
from django.urls import reverse
from drf_spectacular.generators import SchemaGenerator
from referentiel.value_objects.category import Category
from referentiel.value_objects.contract_type import ContractType
from rest_framework import status

from application.ingestion.interfaces.list_offers_input import GetFilteredOffersInput
from infrastructure.factories.referentiel.offer_factory import OfferFactory

URL = reverse("ingestion_v2:offer_summaries")


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


def test_invalid_api_key_returns_401(api_client):
    api_client.credentials(HTTP_AUTHORIZATION="Api-Key wrong-key")
    response = api_client.get(URL)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_api_key_authentication_access(mock_offer_summaries_container, api_key_client):
    _make_paginated_mock(mock_offer_summaries_container, total=0, offers_slice=[])
    response = api_key_client.get(URL)
    assert response.status_code == status.HTTP_200_OK


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
    assert result["startPublicationDate"] == "2024-01-15T00:00:00+00:00"
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


def test_returns_error_500(mock_offer_summaries_container, authenticated_client):
    mock_usecase = MagicMock()
    mock_usecase.execute.side_effect = Exception("db error")
    mock_offer_summaries_container.list_offers_usecase.return_value = mock_usecase

    response = authenticated_client.get(URL)
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR


def test_is_excluded_from_openapi_schema():
    generator = SchemaGenerator()
    schema = generator.get_schema(request=None, public=True)
    assert "/api/v2/offersummaries" not in schema["paths"]
