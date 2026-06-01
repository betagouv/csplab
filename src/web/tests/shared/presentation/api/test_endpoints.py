from pathlib import Path

import pytest
import yaml
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


class TestJWTEndpoints:
    def test_token_obtain_endpoint_exists(
        self, api_client, test_user, user_credentials
    ):
        response = api_client.post(
            reverse("api:token_obtain_pair"),
            {
                "email": user_credentials["email"],
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


class TestSchemaEndpoint:
    @pytest.mark.parametrize(
        "name, expected_in_schema",
        [
            ("api:health_huey", False),
            ("ingestion:concours_upload", True),
            ("ingestion:offers_list, True"),
        ],
    )
    def tet_schema_path_visibility(self, name, expected_in_schema):
        schema_path = Path("presentation/static/api/schema.yaml")
        schema = yaml.safe_load(schema_path.read_text())
        paths = schema.get("paths", {})
        assert (reverse(name) in paths) == expected_in_schema
