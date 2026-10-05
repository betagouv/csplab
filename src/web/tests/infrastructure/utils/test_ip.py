from ipaddress import IPv4Address, IPv6Address

import pytest
from django.test import RequestFactory

from infrastructure.django_apps.utils.ip import get_client_ip, parse_ip


@pytest.mark.parametrize(
    ("meta", "expected"),
    [
        ({"HTTP_X_REAL_IP": "203.0.113.7"}, "203.0.113.7"),
        ({"HTTP_X_REAL_IP": " 2001:db8::1 "}, "2001:db8::1"),
        ({"HTTP_X_REAL_IP": "x"}, None),
        ({"HTTP_X_REAL_IP": ""}, None),
        ({}, None),
        # Client-controlled / router-owned values are never used.
        ({"HTTP_X_FORWARDED_FOR": "1.2.3.4", "REMOTE_ADDR": "10.0.0.1"}, None),
        (
            {"HTTP_X_REAL_IP": "203.0.113.7", "HTTP_X_FORWARDED_FOR": "1.2.3.4"},
            "203.0.113.7",
        ),
    ],
    ids=[
        "ipv4",
        "ipv6_stripped",
        "garbage",
        "empty",
        "missing",
        "ignores_forwarded_for_and_remote_addr",
        "prefers_real_ip_over_forwarded_for",
    ],
)
def test_get_client_ip(meta, expected):
    request = RequestFactory().get("/", **meta)

    assert get_client_ip(request) == expected


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("203.0.113.7", "203.0.113.7"),
        (" 203.0.113.7 ", "203.0.113.7"),
        ("2001:db8::1", "2001:db8::1"),
        (IPv4Address("203.0.113.7"), "203.0.113.7"),
        (IPv6Address("2001:db8::1"), "2001:db8::1"),
        ("", None),
        (None, None),
        ("not-an-ip", None),
    ],
)
def test_parse_ip(raw, expected):
    assert parse_ip(raw) == expected
