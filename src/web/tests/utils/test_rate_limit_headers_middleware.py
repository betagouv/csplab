from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

import pytest
import time_machine
from django.contrib.auth.models import AnonymousUser
from django.core.cache import cache
from django.http import HttpResponse
from django.test import RequestFactory
from rest_framework.throttling import AnonRateThrottle
from rest_framework_simplejwt.tokens import RefreshToken

from infrastructure.authentication.api_key_authentication import (
    ApiKeyRateThrottle,
    ApiKeyRateThrottleDaily,
    _IngestionApiKeyUser,
)
from presentation.middleware.rate_limit_headers import RateLimitHeadersMiddleware


@pytest.fixture
def rf():
    return RequestFactory()


@pytest.fixture(autouse=True)
def clear_cache():
    cache.clear()


@pytest.fixture
def mock_response():
    return HttpResponse()


def make_middleware(mock_response):
    get_response = MagicMock(return_value=mock_response)
    middleware = RateLimitHeadersMiddleware(get_response=get_response)
    return middleware, get_response


class TestRateLimitHeadersMiddleware:
    def test_adds_headers_for_valid_api_key_request(self, rf, mock_response, settings):
        settings.INGESTION_API_KEY = "secret-key"
        middleware, _ = make_middleware(mock_response)
        request = rf.get("/api/v1/offres/", HTTP_AUTHORIZATION="Api-Key secret-key")

        middleware(request)

        assert "X-RateLimit-Limit" in mock_response.headers
        assert "X-RateLimit-Remaining" in mock_response.headers
        assert "X-RateLimit-Reset" in mock_response.headers

    def test_does_not_add_headers_for_invalid_api_key(
        self, rf, mock_response, settings
    ):
        settings.INGESTION_API_KEY = "secret-key"
        middleware, _ = make_middleware(mock_response)
        request = rf.get("/api/v1/offres/", HTTP_AUTHORIZATION="Api-Key wrong-key")

        middleware(request)

        assert "X-RateLimit-Limit" not in mock_response.headers

    def test_does_not_add_headers_for_invalid_jwt(self, rf, mock_response, settings):
        settings.INGESTION_API_KEY = "secret-key"
        middleware, _ = make_middleware(mock_response)
        request = rf.get("/api/v1/offres/", HTTP_AUTHORIZATION="Bearer some-token")

        middleware(request)

        assert "X-RateLimit-Limit" not in mock_response.headers

    def test_adds_headers_for_valid_jwt_request(self, rf, mock_response, test_user):
        middleware, _ = make_middleware(mock_response)
        refresh = RefreshToken.for_user(test_user)
        request = rf.get(
            "/api/v1/offres/", HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}"
        )

        middleware(request)

        assert mock_response.headers["X-RateLimit-Limit"] == "120"
        assert "X-RateLimit-Remaining" in mock_response.headers
        assert "X-RateLimit-Reset" in mock_response.headers

    def test_does_not_add_headers_for_non_api_request_without_authorization(
        self, rf, mock_response
    ):
        middleware, _ = make_middleware(mock_response)
        request = rf.get("/candidate/upload/")

        middleware(request)

        assert "X-RateLimit-Limit" not in mock_response.headers

    def test_adds_headers_for_anonymous_api_request(self, rf, mock_response):
        middleware, _ = make_middleware(mock_response)
        request = rf.get("/api/v1/offres/", REMOTE_ADDR="203.0.113.5")

        middleware(request)

        assert "X-RateLimit-Limit" in mock_response.headers
        assert "X-RateLimit-Remaining" in mock_response.headers
        assert "X-RateLimit-Reset" in mock_response.headers

    @patch.object(AnonRateThrottle, "THROTTLE_RATES", {"anon": "3/minute"})
    def test_anon_remaining_decreases_as_quota_is_consumed(self, rf, mock_response):
        request = rf.get("/api/v1/offres/", REMOTE_ADDR="203.0.113.9")
        request.user = AnonymousUser()
        AnonRateThrottle().allow_request(request, view=None)
        AnonRateThrottle().allow_request(request, view=None)

        middleware, _ = make_middleware(mock_response)
        header_request = rf.get("/api/v1/offres/", REMOTE_ADDR="203.0.113.9")

        middleware(header_request)

        assert mock_response.headers["X-RateLimit-Limit"] == "3"
        assert mock_response.headers["X-RateLimit-Remaining"] == "1"

    @patch.object(ApiKeyRateThrottle, "THROTTLE_RATES", {"api_key": "1000/hour"})
    @patch.object(ApiKeyRateThrottleDaily, "THROTTLE_RATES", {"api_key_daily": "3/day"})
    @time_machine.travel(
        datetime(2026, 7, 29, 12, 0, 0, tzinfo=timezone.utc), tick=False
    )
    def test_reset_reflects_oldest_request_plus_window_duration(
        self, rf, mock_response, settings
    ):
        settings.INGESTION_API_KEY = "secret-key"

        request = rf.get("/")
        request.user = _IngestionApiKeyUser()
        ApiKeyRateThrottleDaily().allow_request(request, view=None)

        middleware, _ = make_middleware(mock_response)
        header_request = rf.get(
            "/api/v1/offres/", HTTP_AUTHORIZATION="Api-Key secret-key"
        )

        middleware(header_request)

        expected_reset = int(
            datetime(2026, 7, 29, 12, 0, 0, tzinfo=timezone.utc).timestamp()
            + 86400  # 1 day, in seconds
        )
        assert mock_response.headers["X-RateLimit-Reset"] == str(expected_reset)

    @patch.object(ApiKeyRateThrottle, "THROTTLE_RATES", {"api_key": "1000/hour"})
    @patch.object(ApiKeyRateThrottleDaily, "THROTTLE_RATES", {"api_key_daily": "3/day"})
    def test_remaining_decreases_as_daily_quota_is_consumed(
        self, rf, mock_response, settings
    ):
        settings.INGESTION_API_KEY = "secret-key"

        request = rf.get("/")
        request.user = _IngestionApiKeyUser()
        ApiKeyRateThrottleDaily().allow_request(request, view=None)
        ApiKeyRateThrottleDaily().allow_request(request, view=None)

        middleware, _ = make_middleware(mock_response)
        header_request = rf.get(
            "/api/v1/offres/", HTTP_AUTHORIZATION="Api-Key secret-key"
        )

        middleware(header_request)

        assert mock_response.headers["X-RateLimit-Limit"] == "3"
        assert mock_response.headers["X-RateLimit-Remaining"] == "1"

    @patch.object(ApiKeyRateThrottle, "THROTTLE_RATES", {"api_key": "1000/hour"})
    @patch.object(ApiKeyRateThrottleDaily, "THROTTLE_RATES", {"api_key_daily": "3/day"})
    def test_returns_most_restrictive_throttle(self, rf, mock_response, settings):
        settings.INGESTION_API_KEY = "secret-key"

        request = rf.get("/")
        request.user = _IngestionApiKeyUser()
        for _ in range(3):
            ApiKeyRateThrottleDaily().allow_request(request, view=None)

        middleware, _ = make_middleware(mock_response)
        header_request = rf.get(
            "/api/v1/offres/", HTTP_AUTHORIZATION="Api-Key secret-key"
        )

        middleware(header_request)

        assert mock_response.headers["X-RateLimit-Limit"] == "3"
        assert mock_response.headers["X-RateLimit-Remaining"] == "0"

    def test_passes_through_response_unchanged(self, rf, mock_response, settings):
        settings.INGESTION_API_KEY = "secret-key"
        middleware, get_response = make_middleware(mock_response)
        request = rf.get("/api/v1/offres/")

        result = middleware(request)

        assert result is mock_response
        get_response.assert_called_once_with(request)
