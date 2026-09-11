from django.urls import reverse
from rest_framework import status

from infrastructure.factories.ingestion.source_django_factory import (
    SourceDjangoFactory,
)
from infrastructure.factories.ingestion.source_factory import SourceFactory

URL = reverse("ingestion:sources_list")

NOMBRE_REQUETES_ATTENDU = (
    1  # usecase: source_repository.get_all()
    + 2  # logging: DJ tries an UPDATE (manually-assigned pk) then falls back to INSERT
)


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


def test_empty_list(mock_sources_container, api_key_client):
    usecase = mock_sources_container.list_sources_usecase.return_value
    usecase.execute.return_value = []

    response = api_key_client.get(URL)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


def test_returns_all_sources(mock_sources_container, api_key_client):
    sources = [SourceFactory.create_entity() for _ in range(2)]
    usecase = mock_sources_container.list_sources_usecase.return_value
    usecase.execute.return_value = sources

    response = api_key_client.get(URL)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 2  # noqa: PLR2004


def test_response_shape(mock_sources_container, api_key_client):
    source = SourceFactory.create_entity()
    usecase = mock_sources_container.list_sources_usecase.return_value
    usecase.execute.return_value = [source]

    response = api_key_client.get(URL)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()[0] == {
        "source_id": str(source.source_id),
        "slug": source.slug,
        "type": source.type.value,
        "client_id_front": source.client_id_front,
        "client_id_back": source.client_id_back,
        "base_url_front": source.base_url_front,
        "base_url_back": source.base_url_back,
    }


def test_returns_500_on_error(mock_sources_container, api_key_client):
    usecase = mock_sources_container.list_sources_usecase.return_value
    usecase.execute.side_effect = Exception("db error")

    response = api_key_client.get(URL)

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR


class TestSourcesListViewDbVerified:
    def test_response_matches_db_record_field_by_field(self, api_key_client):
        source = SourceDjangoFactory()

        response = api_key_client.get(URL)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == [
            {
                "source_id": str(source.source_id),
                "slug": source.slug,
                "type": source.type,
                "client_id_front": source.client_id_front,
                "client_id_back": source.client_id_back,
                "base_url_front": source.base_url_front,
                "base_url_back": source.base_url_back,
            }
        ]

    def test_does_not_trigger_n_plus_one_queries(
        self, api_key_client, django_assert_num_queries
    ):
        SourceDjangoFactory.create_batch(5)

        with django_assert_num_queries(NOMBRE_REQUETES_ATTENDU):
            response = api_key_client.get(URL)

        assert response.status_code == status.HTTP_200_OK
