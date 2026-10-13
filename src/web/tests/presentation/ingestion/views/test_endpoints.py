from pathlib import Path

import pytest
import yaml
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

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

    def test_schema_contact_tag_is_last_in_redoc_menu(self):
        # Redoc affiche après les tags déclarés ceux utilisés par un endpoint sans
        # être déclarés : ils passeraient sous « Aide et contact ».
        schema_path = Path("presentation/static/api/schema.yaml")
        schema = yaml.safe_load(schema_path.read_text())
        declared_tags = [tag["name"] for tag in schema["tags"]]
        endpoint_tags = {
            tag
            for path_item in schema["paths"].values()
            for operation in path_item.values()
            for tag in operation.get("tags", [])
        }
        assert endpoint_tags - set(declared_tags) == set()
        assert declared_tags[-1] == "contact"
