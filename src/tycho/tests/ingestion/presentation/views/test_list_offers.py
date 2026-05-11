from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest
from django.urls import reverse
from faker import Faker
from rest_framework import status

from application.ingestion.interfaces.list_offers_input import GetFilteredOffersInput
from domain.value_objects.contract_type import ContractType
from tests.factories.offer_factory import OfferFactory

fake = Faker()
URL = reverse("ingestion:offers_list")


def test_unauthenticated_access(api_client):
    response = api_client.get(URL)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_post_not_allowed(authenticated_client):
    response = authenticated_client.post(URL)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@patch("presentation.ingestion.views.create_ingestion_container")
def test_empty_result(mock_container, authenticated_client, list_offers_usecase):
    mock_usecase = MagicMock()
    mock_usecase.execute.return_value = MagicMock(offers=[])
    mock_container.return_value.list_offers_usecase.return_value = mock_usecase

    response = authenticated_client.get(URL)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "count": 0,
        "next": None,
        "previous": None,
        "results": [],
    }


@patch("presentation.ingestion.views.create_ingestion_container")
def test_call_without_arg(mock_container, authenticated_client):
    first_offer = OfferFactory.create_entity(
        contract_type=ContractType.TERRITORIAL,
        offer_url=fake.url(),
        archived_at=datetime.now(),
    )
    second_offer = OfferFactory.create_entity()
    offers = [first_offer, second_offer]

    mock_usecase = MagicMock()
    mock_usecase.execute.return_value = MagicMock(offers=offers)
    mock_container.return_value.list_offers_usecase.return_value = mock_usecase

    response = authenticated_client.get(URL)

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data["count"] == len(offers)
    for result, offer in zip(data["results"], offers, strict=True):
        assert result["external_id"] == offer.external_id
        assert result["title"] == offer.title
        assert result["organization"] == offer.organization
        assert result["contract_type"] == (
            offer.contract_type.value if offer.contract_type else None
        )
        assert result["category"] == offer.category.value
        assert result["publication_date"] == "2024-01-15T00:00:00Z"
        assert result["offer_url"] == offer.offer_url
        if offer.archived_at:
            assert result["archived_at"] == offer.archived_at.isoformat() + "Z"
        else:
            assert result["archived_at"] is None


@pytest.mark.parametrize("active,external_id_contains", [(True, None), (False, "123")])
@patch("presentation.ingestion.views.create_ingestion_container")
def test_call_with_args(
    mock_container, authenticated_client, active, external_id_contains
):
    mock_usecase = MagicMock()
    mock_usecase.execute.return_value = MagicMock(offers=[])
    mock_container.return_value.list_offers_usecase.return_value = mock_usecase

    params = {"active": active}
    if external_id_contains is not None:
        params["external_id_contains"] = external_id_contains

    authenticated_client.get(URL, params)

    mock_usecase.execute.assert_called_once_with(
        GetFilteredOffersInput(active=active, external_id_contains=external_id_contains)
    )


@patch("presentation.ingestion.views.create_ingestion_container")
def test_returns_error_500(mock_container, authenticated_client):
    mock_usecase = MagicMock()
    mock_usecase.execute.side_effect = Exception("db error")
    mock_container.return_value.list_offers_usecase.return_value = mock_usecase

    response = authenticated_client.get(URL)
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR


@patch("presentation.ingestion.views.ListOffersPagination.page_size", new=2)
@patch("presentation.ingestion.views.ListOffersPagination.max_page_size", new=2)
@patch("presentation.ingestion.views.create_ingestion_container")
def test_pagination_page_arg(mock_container, authenticated_client):
    num_offers = 3
    offers = [OfferFactory.create_entity() for _ in range(num_offers)]

    mock_usecase = MagicMock()
    mock_usecase.execute.return_value = MagicMock(offers=offers)
    mock_container.return_value.list_offers_usecase.return_value = mock_usecase

    response = authenticated_client.get(URL, {"page": 2})

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["count"] == num_offers
    assert len(data["results"]) == 1
    assert data["previous"] is not None
    assert data["next"] is None

    response = authenticated_client.get(URL, {"page": 3})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {}
