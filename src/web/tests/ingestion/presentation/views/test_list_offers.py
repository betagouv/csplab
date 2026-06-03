from datetime import datetime
from unittest.mock import MagicMock, patch
from urllib.parse import parse_qs, urlparse

import pytest
from django.urls import reverse
from faker import Faker
from rest_framework import status

from application.ingestion.interfaces.list_offers_input import GetFilteredOffersInput
from domain.value_objects.contract_type import ContractType
from tests.factories.offer_factory import OfferFactory

fake = Faker()
URL = reverse("ingestion:offers_list")


@pytest.fixture
def mock_container():
    with patch("presentation.ingestion.views.create_ingestion_container") as mock:
        yield mock


def test_unauthenticated_access(api_client):
    response = api_client.get(URL)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_post_not_allowed(authenticated_client):
    response = authenticated_client.post(URL)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def _make_paginated_mock(mock_container, num_offers, offers_slice):
    mock_page = MagicMock()
    mock_page.count.return_value = num_offers
    mock_page.slice.return_value = iter(offers_slice)

    mock_usecase = MagicMock()
    mock_usecase.execute.return_value = mock_page
    mock_container.return_value.list_offers_usecase.return_value = mock_usecase

    return mock_usecase


def test_empty_result(mock_container, authenticated_client, list_offers_usecase):
    _make_paginated_mock(mock_container, num_offers=0, offers_slice=[])

    response = authenticated_client.get(URL)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "count": 0,
        "next": None,
        "previous": None,
        "results": [],
    }


def test_call_without_arg(mock_container, authenticated_client):
    first_offer = OfferFactory.create_entity(
        contract_type=ContractType.TERRITORIAL,
        offer_url=fake.url(),
        archived_at=datetime.now(),
    )
    second_offer = OfferFactory.create_entity()
    offers = [first_offer, second_offer]

    _make_paginated_mock(mock_container, num_offers=len(offers), offers_slice=offers)

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


@pytest.mark.parametrize("active,external_id_contains", [(True, None), (False, "123")])
def test_call_with_args(
    mock_container, authenticated_client, active, external_id_contains
):
    _make_paginated_mock(mock_container, num_offers=0, offers_slice=[])

    params = {"active": active}
    if external_id_contains is not None:
        params["external_id_contains"] = external_id_contains

    authenticated_client.get(URL, params)

    mock_container.return_value.list_offers_usecase.return_value.execute.assert_called_once_with(
        GetFilteredOffersInput(active=active, external_id_contains=external_id_contains)
    )


def test_returns_error_500(mock_container, authenticated_client):
    mock_usecase = MagicMock()
    mock_usecase.execute.side_effect = Exception("db error")
    mock_container.return_value.list_offers_usecase.return_value = mock_usecase

    response = authenticated_client.get(URL)
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR


@patch("presentation.ingestion.views.IngestionPagination.page_size", new=2)
def test_pagination_page_arg(mock_container, authenticated_client):
    num_offers = 5
    offers = [OfferFactory.create_entity() for _ in range(num_offers)]

    _make_paginated_mock(
        mock_container, num_offers=len(offers), offers_slice=offers[2:4]
    )

    response = authenticated_client.get(URL, {"page": 2, "dummy": "arg", "active": 1})

    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert data["count"] == num_offers
    assert len(data["results"]) == 2  # noqa

    parsed_previous = urlparse(data["previous"])
    assert parsed_previous.path == URL
    assert parse_qs(parsed_previous.query) == {
        "page": ["1"],
        "dummy": ["arg"],
        "active": ["1"],
        "size": ["2"],
    }

    parsed_next = urlparse(data["next"])
    assert parsed_next.path == URL
    assert parse_qs(parsed_next.query) == {
        "page": ["3"],
        "dummy": ["arg"],
        "active": ["1"],
        "size": ["2"],
    }


@patch("presentation.ingestion.views.IngestionPagination.page_size", new=2)
def test_pagination_out_of_bond(mock_container, authenticated_client):
    num_offers = 3
    offers = [OfferFactory.create_entity() for _ in range(num_offers)]

    _make_paginated_mock(mock_container, num_offers=len(offers), offers_slice=[])

    response = authenticated_client.get(URL, {"page": 3})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert data["count"] == num_offers
    assert data["results"] == []

    parsed = urlparse(data["previous"])
    assert parsed.path == URL
    assert parse_qs(parsed.query) == {
        "page": ["2"],
        "size": ["2"],
    }

    assert data["next"] is None
