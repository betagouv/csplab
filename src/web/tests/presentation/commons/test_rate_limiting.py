import time

import pytest
from django.core.cache import cache
from django.urls import reverse
from rest_framework import status

USER_LIMIT = 120
ANON_LIMIT = 5

@pytest.fixture(autouse=True)
def clear_cache():
    cache.clear()


def fill_throttle_history(scope, ident, count):
    cache.set(f"throttle_{scope}_{ident}", [time.time()] * count)


class TestRateLimitingIntegration:
    def test_returns_429_once_rate_limit_is_exceeded(self, jwt_client, test_user):
        URL = reverse("api:health_huey")
        fill_throttle_history("user", test_user.pk, USER_LIMIT - 1)

        response = jwt_client.get(URL)
        assert response.status_code != status.HTTP_429_TOO_MANY_REQUESTS

        response = jwt_client.get(URL)

        assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS
        assert "Retry-After" in response.headers
        assert response.data["detail"].code == "throttled"

    def test_anon_limit_ignores_forwarded_for(self, api_client):
        fill_throttle_history("anon", "203.0.113.7", ANON_LIMIT)

        response = api_client.post(
            reverse("api:token_refresh"),
            {"refresh": "invalid"},
            format="json",
            HTTP_X_REAL_IP="203.0.113.7",
            HTTP_X_FORWARDED_FOR="198.51.100.1",
        )

        assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS
        assert "Retry-After" in response.headers
        assert response.data["detail"].code == "throttled"

    def test_token_obtain_is_limited_by_default_anon_rate(self, api_client):
        fill_throttle_history("anon", "203.0.113.8", ANON_LIMIT - 1)

        def obtain():
            return api_client.post(
                reverse("api:token_obtain_pair"),
                {"email": "nobody@example.com", "password": "wrong"},
                format="json",
                HTTP_X_REAL_IP="203.0.113.8",
            )

        assert obtain().status_code == status.HTTP_401_UNAUTHORIZED

        response = obtain()

        assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS
        assert "Retry-After" in response.headers
        assert response.data["detail"].code == "throttled"
