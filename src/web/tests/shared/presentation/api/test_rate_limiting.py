from unittest.mock import patch

import pytest
from django.core.cache import cache
from django.urls import reverse
from rest_framework import status
from rest_framework.throttling import UserRateThrottle

from infrastructure.authentication.anon_rate_throttle import ClientIpAnonRateThrottle

HEALTH_HUEY_URL = "/api/health/huey"


@pytest.fixture(autouse=True)
def clear_cache():
    cache.clear()


class TestRateLimitingIntegration:
    @patch.object(UserRateThrottle, "THROTTLE_RATES", {"user": "2/minute"})
    def test_returns_429_once_rate_limit_is_exceeded(self, jwt_client):
        for _ in range(2):
            response = jwt_client.get(HEALTH_HUEY_URL)
            assert response.status_code != status.HTTP_429_TOO_MANY_REQUESTS

        response = jwt_client.get(HEALTH_HUEY_URL)

        assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS
        assert "Retry-After" in response.headers
        assert response.data["detail"].code == "throttled"

    @patch.object(ClientIpAnonRateThrottle, "THROTTLE_RATES", {"anon": "5/minute"})
    def test_anon_limit_ignores_forwarded_for(self, api_client):
        def refresh(i):
            return api_client.post(
                reverse("api:token_refresh"),
                {"refresh": "invalid"},
                format="json",
                HTTP_X_REAL_IP="203.0.113.7",
                HTTP_X_FORWARDED_FOR=f"198.51.100.{i}",
            )

        for i in range(5):
            assert refresh(i).status_code != status.HTTP_429_TOO_MANY_REQUESTS

        assert refresh(5).status_code == status.HTTP_429_TOO_MANY_REQUESTS
