from unittest.mock import patch

import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from faker import Faker
from pytest_django.asserts import assertTemplateUsed
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

fake = Faker()


@pytest.fixture(name="api_client")
def api_client_fixture():
    return APIClient()


@pytest.fixture(name="user_credentials")
def user_credentials_fixture():
    return {
        "username": fake.name(),
        "email": fake.email(),
        "password": fake.password(),
    }


@pytest.fixture(name="test_user")
def test_user_fixture(db, user_credentials):
    return User.objects.create_user(**user_credentials)


@pytest.fixture(name="authenticated_client")
def authenticated_client_fixture(api_client, test_user):
    refresh = RefreshToken.for_user(test_user)
    token = str(refresh.access_token)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return api_client


class TestJWTEndpoints:
    def test_token_obtain_endpoint_exists(
        self, api_client, test_user, user_credentials
    ):
        response = api_client.post(
            reverse("api:token_obtain_pair"),
            {
                "username": user_credentials["username"],
                "password": user_credentials["password"],
            },
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data
        assert "refresh" in response.data

    def test_token_refresh_endpoint_exists(self, api_client, test_user):
        refresh = RefreshToken.for_user(test_user)

        response = api_client.post(
            reverse("api:token_refresh"), {"refresh": str(refresh)}, format="json"
        )

        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data


class TestHueyHealthView:
    url = reverse("api:health_huey")

    def test_success_response(self, authenticated_client):
        response = authenticated_client.get(self.url)
        assert response.status_code == status.HTTP_200_OK

    def test_unauthenticated_access(self, api_client):
        response = api_client.get(self.url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_redis_unavailable(self, authenticated_client):
        with patch("huey.contrib.djhuey.HUEY.storage.conn.ping") as mocked_ping:
            mocked_ping.side_effect = Exception("Redis connection refused")
            response = authenticated_client.get(self.url)
            assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
            assert response.data == {"status": "Huey health check failed"}


class TestRedocView:
    def test_views(self, db, api_client):
        response = api_client.get(reverse("api:redoc"))

        assert response.status_code == status.HTTP_200_OK
        assertTemplateUsed(response, "api/redoc.html")
        assert response.context["title"] == "ReDoc"
        assert response.context["schema_url"] == reverse("api:schema")


class TestSchemaEndpoint:
    def test_health_huey_view_is_excluded_from_schema(self, api_client):
        response = api_client.get(reverse("api:schema"))

        assert response.status_code == status.HTTP_200_OK
        assert reverse("api:health_huey") not in response.data.get("paths", {})

    def test_offer_list_is_in_schema(self, api_client):
        response = api_client.get(reverse("api:schema"))

        expected_url = reverse("ingestion:offers_list")

        paths = response.data.get("paths", {})
        assert expected_url in paths

        operation = response.data["paths"][expected_url]["get"]
        assert "offres" in operation.get("tags", [])
