import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from faker import Faker
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


class TestJWTEndpoints:
    def test_token_obtain_endpoint_exists(
        self, api_client, test_user, user_credentials
    ):
        response = api_client.post(
            reverse("token_obtain_pair"),
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
            reverse("token_refresh"), {"refresh": str(refresh)}, format="json"
        )

        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data
