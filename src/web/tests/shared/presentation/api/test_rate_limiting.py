from unittest.mock import patch

import pytest
from django.core.cache import cache
from rest_framework import status
from rest_framework.throttling import UserRateThrottle

HEALTH_HUEY_URL = "/api/health/huey"


@pytest.fixture(autouse=True)
def clear_cache():
    cache.clear()


class TestRateLimitingIntegration:
    @patch.object(UserRateThrottle, "THROTTLE_RATES", {"user": "2/minute"})
    def test_returns_429_once_rate_limit_is_exceeded(self, authenticated_client):
        for _ in range(2):
            response = authenticated_client.get(HEALTH_HUEY_URL)
            assert response.status_code != status.HTTP_429_TOO_MANY_REQUESTS

        response = authenticated_client.get(HEALTH_HUEY_URL)

        assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS
        assert "Retry-After" in response.headers
        assert response.data["detail"].code == "throttled"
