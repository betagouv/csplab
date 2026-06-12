from unittest.mock import MagicMock
from uuid import UUID

import pytest
from django.urls import reverse
from referentiel.exceptions.offer_errors import OfferDoesNotExist
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from application.ingestion.interfaces.archive_offer_by_reference_input import (
    ArchiveOfferByReferenceInput,
)
from domain.ingestion.exceptions.source_authorization_error import (
    SourceAuthorizationError,
)
from tests.factories.ingestion.source_factory import SourceFactory

API_KEY = "test-ingestion-api-key"
REFERENCE = "12345"
SOURCE_ID = UUID("12345678-1234-4234-b234-123456789abc")

URL = reverse("ingestion:offers_archive")
VALID_BODY = {"reference": REFERENCE, "source_id": str(SOURCE_ID)}


@pytest.fixture
def use_case():
    return MagicMock()


@pytest.fixture(autouse=True)
def mock_container(mock_offers_container, use_case):
    mock_offers_container.archive_offer_by_reference_usecase.return_value = use_case


@pytest.fixture
def source():
    return SourceFactory.create_model(source_id=SOURCE_ID)


@pytest.fixture
def authenticated_client_with_source(api_client, test_user, source):
    test_user.sources.add(source)
    refresh = RefreshToken.for_user(test_user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    return api_client


class TestArchiveOffersView:
    def test_unauthenticated_returns_401(self, api_client):
        response = api_client.post(URL, VALID_BODY, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_invalid_api_key_returns_401(self, api_client):
        api_client.credentials(HTTP_AUTHORIZATION="Api-Key wrong-key")
        response = api_client.post(URL, VALID_BODY, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_missing_body_returns_400(self, api_client):
        api_client.credentials(HTTP_AUTHORIZATION=f"Api-Key {API_KEY}")
        response = api_client.post(URL, {}, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_unknown_reference_returns_404(self, api_client, use_case):
        use_case.execute.side_effect = OfferDoesNotExist("unknown-ref")
        api_client.credentials(HTTP_AUTHORIZATION=f"Api-Key {API_KEY}")
        response = api_client.post(
            URL,
            {"reference": "unknown-ref", "source_id": str(SOURCE_ID)},
            format="json",
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_jwt_authentication_archives_offer(
        self, authenticated_client_with_source, test_user, use_case
    ):
        response = authenticated_client_with_source.post(URL, VALID_BODY, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {"status": "ok"}
        use_case.execute.assert_called_once_with(
            ArchiveOfferByReferenceInput(
                reference=REFERENCE,
                source_id=SOURCE_ID,
                user=test_user,
            )
        )

    def test_jwt_authentication_forbidden_source_id_returns_403(
        self, authenticated_client, use_case
    ):
        use_case.execute.side_effect = SourceAuthorizationError({SOURCE_ID})
        response = authenticated_client.post(URL, VALID_BODY, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_api_key_authentication_archives_offer(self, api_client, use_case):
        api_client.credentials(HTTP_AUTHORIZATION=f"Api-Key {API_KEY}")
        response = api_client.post(URL, VALID_BODY, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {"status": "ok"}
        use_case.execute.assert_called_once_with(
            ArchiveOfferByReferenceInput(reference=REFERENCE, source_id=SOURCE_ID)
        )
