from unittest.mock import MagicMock, patch
from urllib.parse import parse_qs, urlparse

import pytest
from django.urls import reverse
from faker import Faker
from rest_framework import status

from application.ingestion.interfaces.list_metiers_input import GetFilteredMetiersInput
from tests.factories.metier_factory import MetierFactory

fake = Faker()
URL = reverse("ingestion:metiers_list")


def test_unauthenticated_access(api_client):
    response = api_client.get(URL)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_post_not_allowed(authenticated_client):
    response = authenticated_client.post(URL)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def _make_paginated_mock(mock_container, num_metiers, metiers_slice):
    mock_page = MagicMock()
    mock_page.count.return_value = num_metiers
    mock_page.slice.return_value = iter(metiers_slice)

    mock_usecase = MagicMock()
    mock_usecase.execute.return_value = mock_page
    mock_container.return_value.list_metiers_usecase.return_value = mock_usecase


@patch("presentation.ingestion.views.create_ingestion_container")
def test_empty_result(mock_container, authenticated_client):
    _make_paginated_mock(mock_container, num_metiers=0, metiers_slice=[])

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
    metiers = [MetierFactory.create_entity() for _ in range(2)]

    _make_paginated_mock(
        mock_container, num_metiers=len(metiers), metiers_slice=metiers
    )

    response = authenticated_client.get(URL, {})

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data["count"] == len(metiers)
    assert data["next"] is None
    assert data["previous"] is None

    for result, metier in zip(data["results"], metiers, strict=True):
        assert result["libelle"] == metier.libelle
        assert result["description"] == metier.description
        assert result["domaine_fonctionnel_code"] == metier.domaine_fonctionnel_code
        assert result["offer_family_code"] == metier.offer_family_code
        assert result["versants"] == [versant.value for versant in metier.versants]
        assert result["activites"] == metier.activites
        assert result["conditions_particulieres"] == metier.conditions_particulieres


@pytest.mark.parametrize("domain", [None, "TRE"])
@patch("presentation.ingestion.views.create_ingestion_container")
def test_call_with_args(mock_container, authenticated_client, domain):
    _make_paginated_mock(mock_container, num_metiers=0, metiers_slice=[])

    params = {"domain": domain} if domain else {}
    authenticated_client.get(URL, params)

    mock_container.return_value.list_metiers_usecase.return_value.execute.assert_called_once_with(
        GetFilteredMetiersInput(domain=domain)
    )


@patch("presentation.ingestion.views.create_ingestion_container")
def test_returns_error_500(mock_container, authenticated_client):
    mock_usecase = MagicMock()
    mock_usecase.execute.side_effect = Exception("db error")
    mock_container.return_value.list_metiers_usecase.return_value = mock_usecase

    response = authenticated_client.get(URL)
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR


@patch("presentation.ingestion.views.IngestionPagination.page_size", new=2)
@patch("presentation.ingestion.views.create_ingestion_container")
def test_pagination_page_arg(mock_container, authenticated_client):
    num_metiers = 5
    metiers = [MetierFactory.create_entity() for _ in range(num_metiers)]

    _make_paginated_mock(
        mock_container, num_metiers=len(metiers), metiers_slice=metiers[2:4]
    )

    response = authenticated_client.get(URL, {"page": 2, "dummy": "arg"})

    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert data["count"] == num_metiers
    assert len(data["results"]) == 2  # noqa

    parsed_previous = urlparse(data["previous"])
    assert parsed_previous.path == URL
    assert parse_qs(parsed_previous.query) == {
        "page": ["1"],
        "dummy": ["arg"],
        "size": ["2"],
    }

    parsed_next = urlparse(data["next"])
    assert parsed_next.path == URL
    assert parse_qs(parsed_next.query) == {
        "page": ["3"],
        "dummy": ["arg"],
        "size": ["2"],
    }


@patch("presentation.ingestion.views.IngestionPagination.page_size", new=2)
@patch("presentation.ingestion.views.create_ingestion_container")
def test_pagination_out_of_bond(mock_container, authenticated_client):
    num_metiers = 3
    metiers = [MetierFactory.create_entity() for _ in range(num_metiers)]

    _make_paginated_mock(mock_container, num_metiers=len(metiers), metiers_slice=[])

    response = authenticated_client.get(URL, {"page": 3})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert data["count"] == num_metiers
    assert data["results"] == []

    parsed = urlparse(data["previous"])
    assert parsed.path == URL
    assert parse_qs(parsed.query) == {
        "page": ["2"],
        "size": ["2"],
    }

    assert data["next"] is None


@patch("presentation.ingestion.views.create_ingestion_container")
def test_invalid_payload(mock_container, authenticated_client):
    _make_paginated_mock(mock_container, num_metiers=0, metiers_slice=[])

    response = authenticated_client.get(URL, {"domain": "ABCD"})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "error" in response.json().keys()
