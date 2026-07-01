from unittest.mock import patch

import pytest
from django.core.cache import cache
from django.test import RequestFactory
from rest_framework.exceptions import AuthenticationFailed

from infrastructure.authentication.api_key_authentication import (
    ApiKeyAuthentication,
    ApiKeyRateThrottle,
    _IngestionApiKeyUser,
    _ip_is_allowed,
)

API_KEY_USER = _IngestionApiKeyUser()


@pytest.fixture
def rf():
    return RequestFactory()


@pytest.mark.parametrize(
    "ip, allowed_ranges, expected",
    [
        ("1.2.3.4", [], True),
        ("192.168.1.50", ["192.168.1.0/24"], True),
        ("10.0.0.1", ["192.168.1.0/24"], False),
        ("10.0.0.1", ["192.168.1.0/24", "10.0.0.0/8"], True),
        ("172.16.0.1", ["192.168.1.0/24", "10.0.0.0/8"], False),
        ("1.2.3.4", ["1.2.3.4/32"], True),
        ("1.2.3.5", ["1.2.3.4/32"], False),
        ("not-an-ip", ["192.168.1.0/24"], False),
        ("::1", ["::1/128"], True),
        ("::2", ["::1/128"], False),
    ],
    ids=[
        "no_restriction_when_list_is_empty",
        "ip_in_allowed_range",
        "ip_not_in_allowed_range",
        "ip_matched_by_one_of_multiple_ranges",
        "ip_not_matched_by_any_range",
        "exact_host_cidr_match",
        "exact_host_cidr_no_match",
        "invalid_ip_returns_false",
        "ipv6_in_allowed_range",
        "ipv6_not_in_allowed_range",
    ],
)
class TestIpIsAllowed:
    def test_ip_is_allowed(self, ip, allowed_ranges, expected):
        assert _ip_is_allowed(ip, allowed_ranges) is expected


class TestApiKeyAuthenticationIpRestriction:
    @pytest.fixture
    def rf(self):
        return RequestFactory()

    def _make_request(self, rf, ip="1.2.3.4", forwarded_for=None):
        request = rf.get("/", REMOTE_ADDR=ip)
        if forwarded_for:
            request.META["HTTP_X_FORWARDED_FOR"] = forwarded_for
        request.META["HTTP_AUTHORIZATION"] = "Api-Key test-ingestion-api-key"
        return request

    @patch(
        "django.conf.settings.INGESTION_API_KEY_ALLOWED_IP_RANGES", ["192.168.1.0/24"]
    )
    def test_rejects_ip_outside_allowed_range(self, rf):
        auth = ApiKeyAuthentication()
        request = self._make_request(rf, ip="10.0.0.1")
        with pytest.raises(AuthenticationFailed, match="IP address not allowed"):
            auth.authenticate(request)

    @patch(
        "django.conf.settings.INGESTION_API_KEY_ALLOWED_IP_RANGES", ["192.168.1.0/24"]
    )
    def test_accepts_ip_inside_allowed_range(self, rf):
        auth = ApiKeyAuthentication()
        request = self._make_request(rf, ip="192.168.1.42")
        result = auth.authenticate(request)
        assert result is not None
        assert isinstance(result[0], _IngestionApiKeyUser)

    @patch("django.conf.settings.INGESTION_API_KEY_ALLOWED_IP_RANGES", [])
    def test_accepts_any_ip_when_no_restriction(self, rf):
        auth = ApiKeyAuthentication()
        request = self._make_request(rf, ip="1.2.3.4")
        result = auth.authenticate(request)
        assert result is not None

    @patch(
        "django.conf.settings.INGESTION_API_KEY_ALLOWED_IP_RANGES", ["192.168.1.0/24"]
    )
    def test_uses_first_forwarded_for_ip(self, rf):
        auth = ApiKeyAuthentication()
        request = self._make_request(
            rf, ip="192.168.1.1", forwarded_for="10.0.0.1, 192.168.1.1"
        )
        with pytest.raises(AuthenticationFailed, match="IP address not allowed"):
            auth.authenticate(request)

    @patch(
        "django.conf.settings.INGESTION_API_KEY_ALLOWED_IP_RANGES",
        ["10.0.0.0/8", "192.168.1.0/24"],
    )
    def test_accepts_ip_matched_by_any_range(self, rf):
        auth = ApiKeyAuthentication()
        request = self._make_request(rf, ip="192.168.1.5")
        result = auth.authenticate(request)
        assert result is not None


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
