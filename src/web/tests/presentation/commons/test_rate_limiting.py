import time
from typing import cast

import pytest
from django.conf import settings
from django.core.cache import cache
from django.urls import reverse
from rest_framework import status

RATES = cast(dict[str, str], settings.REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"])
ANON_LIMIT = int(RATES["anon"].split("/")[0])
USER_LIMIT = int(RATES["user"].split("/")[0])
API_KEY = int(RATES["api_key"].split("/")[0])
API_KEY_DAILY = int(RATES["api_key_daily"].split("/")[0])


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

    @pytest.mark.parametrize(
        "scope,limit", [("api_key", API_KEY), ("api_key_daily", API_KEY_DAILY)]
    )
    def test_api_key_limit_is_enforced_at_configured_rate(
        self, api_key_client, scope, limit
    ):
        URL = reverse("ingestion:organismes_upsert")
        fill_throttle_history(scope, "ingestion-api-key", limit - 1)

        # Throttles run before the handler lookup, so a GET on a POST-only
        # endpoint counts toward the limit without reaching the view.
        response = api_key_client.get(URL)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

        response = api_key_client.get(URL)

        assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS
        assert "Retry-After" in response.headers
        assert response.data["detail"].code == "throttled"
