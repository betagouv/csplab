from unittest.mock import MagicMock, patch

import pytest
from django.urls import reverse
from rest_framework import status

from domain.exceptions.offer_errors import OfferDoesNotExist

API_KEY = "test-ingestion-api-key"
REFERENCE = "12345"


def make_url(reference: str = REFERENCE) -> str:
    return reverse("api:offers_archive", kwargs={"reference": reference})


@pytest.fixture
def use_case():
    return MagicMock()


@pytest.fixture(autouse=True)
def mock_container(use_case):
    container = MagicMock()
    container.archive_offer_by_reference_usecase.return_value = use_case
    with patch(
        "presentation.api.views.create_ingestion_container", return_value=container
    ):
        yield container


class TestArchiveOffersView:
    def test_unauthenticated_returns_401(self, api_client):
        response = api_client.post(make_url())
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_invalid_api_key_returns_401(self, api_client):
        api_client.credentials(HTTP_AUTHORIZATION="Api-Key wrong-key")
        response = api_client.post(make_url())
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_unknown_reference_returns_404(self, api_client, use_case):
        use_case.execute.side_effect = OfferDoesNotExist("unknown-ref")
        api_client.credentials(HTTP_AUTHORIZATION=f"Api-Key {API_KEY}")
        response = api_client.post(make_url("unknown-ref"))
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_jwt_authentication_archives_offer(self, authenticated_client, use_case):
        response = authenticated_client.post(make_url())
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {"status": "ok"}
        use_case.execute.assert_called_once_with(REFERENCE)

    def test_api_key_authentication_archives_offer(self, api_client, use_case):
        api_client.credentials(HTTP_AUTHORIZATION=f"Api-Key {API_KEY}")
        response = api_client.post(make_url())
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {"status": "ok"}
        use_case.execute.assert_called_once_with(REFERENCE)
