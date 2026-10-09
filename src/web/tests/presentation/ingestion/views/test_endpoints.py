from pathlib import Path

import pytest
import yaml
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import NotAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from config.exception_handler import custom_exception_handler
from infrastructure.factories.identite.utilisateur_factory import DEFAULT_PASSWORD


class TestJWTEndpoints:
    def test_token_obtain_endpoint_updates_last_login(self, api_client, test_user):
        assert test_user.last_login is None

        response = api_client.post(
            reverse("api:token_obtain_pair"),
            {
                "email": test_user.email,
                "password": DEFAULT_PASSWORD,
            },
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data
        assert "refresh" in response.data

        test_user.refresh_from_db()
        assert test_user.last_login is not None

    def test_token_refresh_endpoint_exists(self, api_client, test_user):
        refresh = RefreshToken.for_user(test_user)

        response = api_client.post(
            reverse("api:token_refresh"), {"refresh": str(refresh)}, format="json"
        )

        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data


class TestSchemaEndpoint:
    @pytest.mark.parametrize(
        "name, expected_in_schema",
        [
            ("api:health_huey", False),
            ("ingestion:concours_upload", True),
            ("ingestion:offers_list", True),
        ],
    )
    def test_schema_path_visibility(self, name, expected_in_schema):
        schema_path = Path("presentation/static/api/schema.yaml")
        schema = yaml.safe_load(schema_path.read_text())
        paths = schema.get("paths", {})
        assert (reverse(name) in paths) == expected_in_schema


class TestApiV1ErrorFormat:
    def test_missing_credentials_returns_erreur(self, api_client):
        response = api_client.get(reverse("ingestion:offers_list"))

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert set(response.json()) == {"erreur"}

    def test_invalid_token_returns_erreur_and_code(self, api_client):
        api_client.credentials(HTTP_AUTHORIZATION="Bearer invalid")

        response = api_client.get(reverse("ingestion:offers_list"))

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json()["code"] == "token_not_valid"
        assert set(response.json()) == {"erreur", "code"}

    def test_errors_outside_api_v1_keep_drf_format(self, rf):
        request = rf.get("/api/token")

        response = custom_exception_handler(NotAuthenticated(), {"request": request})

        assert set(response.data) == {"detail"}
