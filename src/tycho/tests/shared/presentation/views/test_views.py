from unittest.mock import patch

from django.urls import reverse
from pytest_django.asserts import (
    assertTemplateUsed,
)
from rest_framework import status


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
