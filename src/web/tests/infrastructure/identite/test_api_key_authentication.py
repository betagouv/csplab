from unittest.mock import patch

import pytest
from django.core.cache import cache
from django.test import RequestFactory

from infrastructure.authentication.api_key_authentication import (
    ApiKeyRateThrottle,
    _IngestionApiKeyUser,
)

API_KEY_USER = _IngestionApiKeyUser()


@pytest.fixture
def rf():
    return RequestFactory()


class TestApiKeyRateThrottle:
    def test_returns_cache_key_for_api_key_user(self, rf):
        request = rf.get("/")
        request.user = API_KEY_USER
        throttle = ApiKeyRateThrottle()
        cache_key = throttle.get_cache_key(request, view=None)
        assert cache_key is not None
        assert "ingestion-api-key" in cache_key

    def test_returns_none_for_non_api_key_user(self, rf):
        request = rf.get("/")
        request.user = object()
        throttle = ApiKeyRateThrottle()
        cache_key = throttle.get_cache_key(request, view=None)
        assert cache_key is None

    def test_all_api_key_requests_share_the_same_cache_key(self, rf):
        throttle = ApiKeyRateThrottle()
        request_a = rf.get("/foo")
        request_a.user = API_KEY_USER
        request_b = rf.post("/bar")
        request_b.user = API_KEY_USER
        assert throttle.get_cache_key(request_a, view=None) == throttle.get_cache_key(
            request_b, view=None
        )

    def test_scope_is_api_key(self):
        assert ApiKeyRateThrottle.scope == "api_key"

    @patch.object(ApiKeyRateThrottle, "THROTTLE_RATES", {"api_key": "3/hour"})
    def test_rate_limit_allows_requests_within_limit(self, rf):
        cache.clear()
        request = rf.get("/")
        request.user = API_KEY_USER
        for _ in range(3):
            assert ApiKeyRateThrottle().allow_request(request, view=None) is True

    @patch.object(ApiKeyRateThrottle, "THROTTLE_RATES", {"api_key": "3/hour"})
    def test_rate_limit_blocks_requests_over_limit(self, rf):
        cache.clear()
        request = rf.get("/")
        request.user = API_KEY_USER
        for _ in range(3):
            ApiKeyRateThrottle().allow_request(request, view=None)
        assert ApiKeyRateThrottle().allow_request(request, view=None) is False

    @patch.object(ApiKeyRateThrottle, "THROTTLE_RATES", {"api_key": "3/hour"})
    def test_rate_limit_is_not_applied_to_non_api_key_user(self, rf):
        cache.clear()
        request = rf.get("/")
        request.user = object()
        for _ in range(10):
            assert ApiKeyRateThrottle().allow_request(request, view=None) is True
