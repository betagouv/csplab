from unittest.mock import patch

import pytest
from django.urls import reverse
from rest_framework import status

from tests.factories.source_factory import SourceFactory

URL = reverse("ingestion:sources_list")


@pytest.fixture
def mock_container():
    with patch("presentation.ingestion.views.create_ingestion_container") as mock:
        yield mock


def test_unauthenticated_returns_401(api_client):
    response = api_client.get(URL)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_jwt_auth_returns_401(authenticated_client):
    response = authenticated_client.get(URL)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_invalid_api_key_returns_401(api_client):
    api_client.credentials(HTTP_AUTHORIZATION="Api-Key wrong-key")
    response = api_client.get(URL)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_empty_list(mock_container, api_key_client):
    usecase = mock_container.return_value.list_sources_usecase.return_value
    usecase.execute.return_value = []

    response = api_key_client.get(URL)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


def test_returns_all_sources(mock_container, api_key_client):
    sources = [SourceFactory.create_entity() for _ in range(2)]
    usecase = mock_container.return_value.list_sources_usecase.return_value
    usecase.execute.return_value = sources

    response = api_key_client.get(URL)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 2  # noqa: PLR2004


def test_response_shape(mock_container, api_key_client):
    source = SourceFactory.create_entity()
    usecase = mock_container.return_value.list_sources_usecase.return_value
    usecase.execute.return_value = [source]

    response = api_key_client.get(URL)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()[0] == {
        "source_id": str(source.source_id),
        "type": source.type.value,
        "client_id_front": source.client_id_front,
        "client_id_back": source.client_id_back,
        "base_url_front": source.base_url_front,
        "base_url_back": source.base_url_back,
    }


def test_returns_500_on_error(mock_container, api_key_client):
    usecase = mock_container.return_value.list_sources_usecase.return_value
    usecase.execute.side_effect = Exception("db error")

    response = api_key_client.get(URL)

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
