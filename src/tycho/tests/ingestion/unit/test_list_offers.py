from datetime import datetime, timezone
from http import HTTPStatus
from unittest.mock import MagicMock, patch
from urllib.parse import urlencode

import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from faker import Faker
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from application.ingestion.usecases.list_offers import (
    GetOffersCommand,
    ListOffersUseCase,
)
from tests.factories.offer_factory import OfferFactory

fake = Faker()

OFFERS_COUNT = 5


@pytest.fixture(name="mock_repository")
def mock_repository_fixture():
    mock = MagicMock()
    mock.get_by_status_and_period.return_value = [
        OfferFactory.build() for _ in range(OFFERS_COUNT)
    ]
    return mock


@pytest.fixture(name="api_client")
def api_client_fixture():
    return APIClient()


@pytest.fixture(name="user")
def user_fixture(db):
    return User.objects.create_user(
        username=fake.name(), email=fake.email(), password=fake.password()
    )


@pytest.fixture(name="authenticated_client")
def authenticated_client_fixture(api_client, user):
    refresh = RefreshToken.for_user(user)
    token = str(refresh.access_token)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return api_client


@pytest.fixture(name="offers_url")
def offers_url_fixture():
    return reverse("ingestion:offers_list")


@pytest.fixture(name="patched_repository")
def patched_repository_fixture(mock_repository):
    with patch("presentation.ingestion.views.PostgresOffersRepository") as patched:
        patched.return_value = mock_repository
        yield mock_repository


class TestListOffersUseCase:
    def test_returns_list_of_offers(self, mock_repository):
        usecase = ListOffersUseCase(offers_repository=mock_repository)
        result = usecase.execute(GetOffersCommand(active=True, after=None, before=None))
        assert result.offers == mock_repository.get_by_status_and_period.return_value


class TestOffersListView:
    def test_returns_401_when_not_authenticated(self, api_client, offers_url):
        response = api_client.get(offers_url)
        assert response.status_code == HTTPStatus.UNAUTHORIZED

    def test_returns_200_when_authenticated(
        self, authenticated_client, offers_url, patched_repository
    ):
        response = authenticated_client.get(offers_url)

        assert response.status_code == HTTPStatus.OK
        assert "results" in response.data
        assert "count" in response.data
        assert response.data["count"] == OFFERS_COUNT
        assert len(response.data["results"]) == OFFERS_COUNT
        patched_repository.get_by_status_and_period.assert_called_once_with(
            active=True, after=None, before=None
        )

    @pytest.mark.parametrize("param", ["after", "before"])
    def test_invalid_after_returns_400(self, authenticated_client, offers_url, param):
        response = authenticated_client.get(offers_url, {param: "not-a-date"})
        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_after_is_more_recent_than_before(self, authenticated_client, offers_url):
        response = authenticated_client.get(
            offers_url,
            {
                "after": datetime(2026, 5, 5, 12, 12, 12),
                "before": datetime(2026, 5, 5, 12, 12, 11),
            },
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_after_param(self, authenticated_client, offers_url, patched_repository):
        response = authenticated_client.get(
            offers_url, {"after": "2026-01-15T10:30:00Z"}
        )

        assert response.status_code == HTTPStatus.OK
        patched_repository.get_by_status_and_period.assert_called_once_with(
            active=True,
            after=datetime(2026, 1, 15, 10, 30, tzinfo=timezone.utc),
            before=None,
        )

    def test_before_param(self, authenticated_client, offers_url, patched_repository):
        response = authenticated_client.get(
            offers_url, {"before": "2026-06-01T00:00:00Z"}
        )

        assert response.status_code == HTTPStatus.OK
        patched_repository.get_by_status_and_period.assert_called_once_with(
            active=True,
            after=None,
            before=datetime(2026, 6, 1, tzinfo=timezone.utc),
        )

    @pytest.mark.parametrize("active", [True, False])
    def test_active_param(
        self, authenticated_client, offers_url, active, patched_repository
    ):
        response = authenticated_client.get(offers_url, {"active": active})

        assert response.status_code == HTTPStatus.OK
        patched_repository.get_by_status_and_period.assert_called_once_with(
            active=active, after=None, before=None
        )

    def test_pagination_and_size(
        self, authenticated_client, offers_url, patched_repository
    ):
        size = 2
        params = {"size": size, "page": 2}

        response = authenticated_client.get(offers_url, params)

        assert response.status_code == HTTPStatus.OK
        assert response.data["count"] == OFFERS_COUNT
        assert len(response.data["results"]) == size

        url = reverse("ingestion:offers_list")

        previous_url = f"{url}?{urlencode({'size': size})}"
        assert previous_url in response.data["previous"]

        next_url = f"{url}?{urlencode({'page': 3, 'size': size})}"
        assert next_url in response.data["next"]

    def test_serialization(self, authenticated_client, offers_url, patched_repository):
        response = authenticated_client.get(offers_url)

        assert response.status_code == HTTPStatus.OK

        result = response.data["results"][0]
        assert list(result.keys()) == [
            "external_id",
            "title",
            "organization",
            "contract_type",
            "category",
            "publication_date",
            "offer_url",
        ]
        assert isinstance(datetime.fromisoformat(result["publication_date"]), datetime)
