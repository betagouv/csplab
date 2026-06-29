from unittest.mock import MagicMock
from uuid import UUID

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from application.ingestion.interfaces.get_offers_by_source_input import (
    GetOffersBySourceInput,
)
from domain.ingestion.exceptions.source_authorization_error import (
    SourceAuthorizationError,
)
from tests.factories.ingestion.source_factory import SourceFactory
from tests.factories.referentiel.offer_factory import OfferFactory

SOURCE_ID = UUID("12345678-1234-4234-b234-123456789abc")

URL = reverse("ingestion:offers_by_source", kwargs={"source_id": SOURCE_ID})


@pytest.fixture
def use_case():
    return MagicMock()


@pytest.fixture(autouse=True)
def mock_container(mock_offers_container, use_case):
    mock_offers_container.get_offers_by_source_usecase.return_value = use_case


@pytest.fixture
def source():
    return SourceFactory.create_model(source_id=SOURCE_ID)


@pytest.fixture
def authenticated_client_with_source(api_client, test_user, source):
    test_user.sources.add(source)
    refresh = RefreshToken.for_user(test_user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    return api_client


def _make_paginated_mock(use_case, num_offers, offers_slice):
    mock_page = MagicMock()
    mock_page.count.return_value = num_offers
    mock_page.slice.return_value = iter(offers_slice)
    use_case.execute.return_value = mock_page
    return use_case


class TestOffersBySourceView:
    def test_unauthenticated_returns_401(self, api_client):
        response = api_client.get(URL)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_invalid_api_key_returns_401(self, api_client):
        api_client.credentials(HTTP_AUTHORIZATION="Api-Key wrong-key")
        response = api_client.get(URL)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_api_key_authentication_returns_offers(self, api_key_client, use_case):
        offer = OfferFactory.create_entity(source_id=SOURCE_ID)
        _make_paginated_mock(use_case, num_offers=1, offers_slice=[offer])

        response = api_key_client.get(URL)

        assert response.status_code == status.HTTP_200_OK
        use_case.execute.assert_called_once_with(
            GetOffersBySourceInput(source_id=SOURCE_ID, utilisateur_entity_id=None)
        )

    def test_post_not_allowed(self, authenticated_client):
        response = authenticated_client.post(URL)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_jwt_authentication_returns_offers(
        self, authenticated_client_with_source, test_user, use_case
    ):
        offer = OfferFactory.create_entity(source_id=SOURCE_ID)
        _make_paginated_mock(use_case, num_offers=1, offers_slice=[offer])

        response = authenticated_client_with_source.get(URL)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["count"] == 1
        assert data["results"][0]["external_id"] == offer.external_id
        assert data["results"][0]["source_id"] == str(SOURCE_ID)

        use_case.execute.assert_called_once_with(
            GetOffersBySourceInput(
                source_id=SOURCE_ID,
                utilisateur_entity_id=UUID(test_user.username),
            )
        )

    def test_jwt_authentication_returns_offer_without_localisation(
        self, authenticated_client_with_source, use_case
    ):
        offer = OfferFactory.create_entity(source_id=SOURCE_ID)
        offer.localisation = None
        _make_paginated_mock(use_case, num_offers=1, offers_slice=[offer])

        response = authenticated_client_with_source.get(URL)

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["results"][0]["localisation"] is None

    def test_jwt_authentication_forbidden_source_returns_401(
        self, authenticated_client, use_case
    ):
        use_case.execute.side_effect = SourceAuthorizationError({SOURCE_ID})
        response = authenticated_client.get(URL)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_returns_error_500(self, authenticated_client, use_case):
        use_case.execute.side_effect = Exception("db error")

        response = authenticated_client.get(URL)
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
