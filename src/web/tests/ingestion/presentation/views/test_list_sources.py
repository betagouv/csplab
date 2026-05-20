from unittest.mock import patch

from django.urls import reverse
from rest_framework import status

from domain.value_objects.source_type import SourceType
from tests.factories.source_factory import SourceFactory

URL = reverse("ingestion:sources_list")


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


@patch("presentation.ingestion.views.create_ingestion_container")
def test_empty_list(mock_container, api_key_client):
    usecase = mock_container.return_value.list_sources_usecase.return_value
    usecase.execute.return_value = []

    response = api_key_client.get(URL)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


@patch("presentation.ingestion.views.create_ingestion_container")
def test_returns_all_sources(mock_container, api_key_client):
    sources = [SourceFactory.create_entity() for _ in range(2)]
    usecase = mock_container.return_value.list_sources_usecase.return_value
    usecase.execute.return_value = sources

    response = api_key_client.get(URL)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 2  # noqa: PLR2004


@patch("presentation.ingestion.views.create_ingestion_container")
def test_response_shape(mock_container, api_key_client):
    source = SourceFactory.create_entity(
        source_type=SourceType.TALENTSOFT,
        client_id_front="front_x",
        client_id_back="back_x",
        base_url="https://example.talentsoft.com",
    )
    usecase = mock_container.return_value.list_sources_usecase.return_value
    usecase.execute.return_value = [source]

    response = api_key_client.get(URL)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()[0] == {
        "source_id": str(source.source_id),
        "type": SourceType.TALENTSOFT.value,
        "client_id_front": "front_x",
        "client_id_back": "back_x",
        "base_url": "https://example.talentsoft.com",
    }


@patch("presentation.ingestion.views.create_ingestion_container")
def test_returns_500_on_error(mock_container, api_key_client):
    usecase = mock_container.return_value.list_sources_usecase.return_value
    usecase.execute.side_effect = Exception("db error")

    response = api_key_client.get(URL)

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
