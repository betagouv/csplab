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


class TestSchemaEndpoint:
    def test_health_huey_view_is_excluded_from_schema(self, api_client):
        response = api_client.get(reverse("api:schema"))

        assert response.status_code == status.HTTP_200_OK
        assert reverse("api:health_huey") not in response.data.get("paths", {})
