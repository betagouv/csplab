from ipaddress import IPv4Address, IPv6Address

import pytest
from django.test import RequestFactory

from infrastructure.django_apps.utils.ip import (
    get_client_ip,
    ip_in_networks,
    normalize_network,
    parse_ip,
)


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
        ({"REMOTE_ADDR": "10.240.1.2"}, "10.240.1.2"),
        ({"REMOTE_ADDR": "10.240.1.2", "HTTP_X_REAL_IP": "203.0.113.7"}, "10.240.1.2"),
        ({"REMOTE_ADDR": "10.240.4.1", "HTTP_X_REAL_IP": "203.0.113.7"}, "203.0.113.7"),
        ({"REMOTE_ADDR": "172.17.0.5", "HTTP_X_REAL_IP": "10.240.1.2"}, "10.240.1.2"),
    ],
    ids=[
        "ipv4",
        "ipv6_stripped",
        "garbage",
        "empty",
        "missing",
        "ignores_forwarded_for_and_remote_addr",
        "prefers_real_ip_over_forwarded_for",
        "private_network_remote_addr",
        "private_network_ignores_forged_real_ip",
        "outside_private_network_range_uses_real_ip",
        "public_router_uses_real_ip",
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


@pytest.mark.parametrize(
    ("ip", "networks", "expected"),
    [
        ("192.168.1.50", ["192.168.1.0/24"], True),
        ("10.0.0.1", ["192.168.1.0/24"], False),
        ("10.0.0.1", ["192.168.1.0/24", "10.0.0.0/8"], True),
        ("172.16.0.1", ["192.168.1.0/24", "10.0.0.0/8"], False),
        ("1.2.3.4", ["1.2.3.4/32"], True),
        ("1.2.3.5", ["1.2.3.4/32"], False),
        ("2001:db8::1", ["2001:db8::/48"], True),
        ("2001:db9::1", ["2001:db8::/48"], False),
        ("::1", ["::1/128"], True),
        # An IPv4 client never matches an IPv6 range, and vice versa.
        ("1.2.3.4", ["::/0"], False),
        (IPv4Address("1.2.3.4"), ["1.2.3.0/24"], True),
        ("1.2.3.4", [], False),
        (None, ["0.0.0.0/0"], False),
        ("", ["0.0.0.0/0"], False),
        ("not-an-ip", ["0.0.0.0/0"], False),
        ("1.2.3.4", ["garbage", "1.2.3.0/24"], True),
        ("1.2.3.4", [" 1.2.3.0/24 "], True),
    ],
    ids=[
        "ipv4_in_range",
        "ipv4_outside_range",
        "matched_by_one_of_several_ranges",
        "matched_by_no_range",
        "host_range_match",
        "host_range_no_match",
        "ipv6_in_range",
        "ipv6_outside_range",
        "ipv6_host_range",
        "ip_version_mismatch",
        "ip_address_object",
        "empty_networks_never_match",
        "unknown_ip_never_matches",
        "empty_ip_never_matches",
        "invalid_ip_never_matches",
        "invalid_network_is_skipped",
        "network_is_stripped",
    ],
)
def test_ip_in_networks(ip, networks, expected):
    assert ip_in_networks(ip, networks) is expected


def test_ip_in_networks_logs_invalid_network(caplog):
    ip_in_networks("1.2.3.4", ["garbage", "1.2.3.0/24"])

    assert "Invalid network 'garbage' skipped." in caplog.text


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("203.0.113.10", "203.0.113.10/32"),
        (" 203.0.113.0/24 ", "203.0.113.0/24"),
        ("203.0.113.7/24", "203.0.113.0/24"),
        ("2001:db8::1", "2001:db8::1/128"),
        ("2001:DB8::/48", "2001:db8::/48"),
    ],
    ids=[
        "single_ipv4",
        "stripped",
        "host_bits_cleared",
        "single_ipv6",
        "ipv6_lowercased",
    ],
)
def test_normalize_network(value, expected):
    assert normalize_network(value) == expected


@pytest.mark.parametrize("value", ["", "not-an-ip", "203.0.113.0/33", "1.2.3"])
def test_normalize_network_rejects_invalid_values(value):
    with pytest.raises(ValueError):
        normalize_network(value)
