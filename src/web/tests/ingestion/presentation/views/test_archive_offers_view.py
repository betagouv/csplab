from unittest.mock import MagicMock, patch

import pytest
from django.urls import reverse
from rest_framework import status

from tests.factories.offer_factory import OfferFactory
from tests.utils.in_memory_offers_repository import InMemoryOffersRepository

API_KEY = "test-ingestion-api-key"
REFERENCE = "12345"


def make_url(reference: str = REFERENCE) -> str:
    return reverse("api:offers_archive", kwargs={"reference": reference})


@pytest.fixture
def offers_repository():
    return InMemoryOffersRepository()


@pytest.fixture(autouse=True)
def mock_container(offers_repository):
    container = MagicMock()
    container.offers_repository.return_value = offers_repository
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

    def test_unknown_reference_returns_404(self, api_client):
        api_client.credentials(HTTP_AUTHORIZATION=f"Api-Key {API_KEY}")
        response = api_client.post(make_url("unknown-ref"))
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_jwt_authentication_archives_offer(
        self, authenticated_client, offers_repository
    ):
        offers_repository.upsert_batch(
            [OfferFactory.create_entity(external_id=f"Versant_FPE-{REFERENCE}")]
        )
        response = authenticated_client.post(make_url())
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {"status": "ok"}
        offer = offers_repository.get_by_reference(REFERENCE)
        assert offer.archived_at is not None

    def test_api_key_authentication_archives_offer(self, api_client, offers_repository):
        offers_repository.upsert_batch(
            [OfferFactory.create_entity(external_id=f"Versant_FPE-{REFERENCE}")]
        )
        api_client.credentials(HTTP_AUTHORIZATION=f"Api-Key {API_KEY}")
        response = api_client.post(make_url())
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {"status": "ok"}
        offer = offers_repository.get_by_reference(REFERENCE)
        assert offer.archived_at is not None
