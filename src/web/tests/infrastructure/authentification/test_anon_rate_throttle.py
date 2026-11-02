from unittest.mock import patch

import pytest
from django.contrib.auth.models import AnonymousUser
from django.core.cache import cache
from django.test import RequestFactory

from infrastructure.authentication.anon_rate_throttle import (
    UNKNOWN_CLIENT_IDENT,
    ClientIpAnonRateThrottle,
)


@pytest.fixture(autouse=True)
def clear_cache():
    cache.clear()


def _request(**meta):
    request = RequestFactory().get("/api/v1/", **meta)
    request.user = AnonymousUser()
    return request


@pytest.mark.parametrize(
    ("meta", "expected"),
    [
        (
            {"HTTP_X_REAL_IP": "203.0.113.7", "HTTP_X_FORWARDED_FOR": "1.2.3.4"},
            "203.0.113.7",
        ),
        ({"HTTP_X_REAL_IP": "not-an-ip"}, UNKNOWN_CLIENT_IDENT),
        (
            {"HTTP_X_FORWARDED_FOR": "1.2.3.4", "REMOTE_ADDR": "203.0.113.9"},
            UNKNOWN_CLIENT_IDENT,
        ),
    ],
    ids=["real_ip", "invalid_real_ip", "missing_real_ip"],
)
def test_get_ident(meta, expected):
    assert ClientIpAnonRateThrottle().get_ident(_request(**meta)) == expected


@patch.object(ClientIpAnonRateThrottle, "THROTTLE_RATES", {"anon": "2/minute"})
def test_forwarded_for_does_not_reset_the_counter():
    for i in range(2):
        request = _request(
            HTTP_X_REAL_IP="203.0.113.7", HTTP_X_FORWARDED_FOR=f"1.2.3.{i}"
        )
        assert ClientIpAnonRateThrottle().allow_request(request, view=None) is True

    request = _request(HTTP_X_REAL_IP="203.0.113.7", HTTP_X_FORWARDED_FOR="1.2.3.99")
    assert ClientIpAnonRateThrottle().allow_request(request, view=None) is False


@patch.object(ClientIpAnonRateThrottle, "THROTTLE_RATES", {"anon": "2/minute"})
def test_requests_without_real_ip_share_one_counter():
    for i in range(2):
        request = _request(HTTP_X_FORWARDED_FOR=f"1.2.3.{i}")
        assert ClientIpAnonRateThrottle().allow_request(request, view=None) is True

    request = _request(HTTP_X_REAL_IP="garbage")
    assert ClientIpAnonRateThrottle().allow_request(request, view=None) is False
