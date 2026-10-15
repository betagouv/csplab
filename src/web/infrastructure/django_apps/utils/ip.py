from ipaddress import IPv4Address, IPv6Address, ip_address, ip_network

IPAddressInput = str | IPv4Address | IPv6Address

# https://doc.scalingo.com/platform/networking/private/concepts
SCALINGO_PRIVATE_NETWORK = ip_network("10.240.0.0/22")


def parse_ip(raw: IPAddressInput | None) -> str | None:
    """Normalized IP string, or None when `raw` is empty or not an IP."""
    if not raw:
        return None
    try:
        return str(ip_address(str(raw).strip()))
    except ValueError:
        return None


def get_client_ip(request) -> str | None:
    # Private network traffic bypasses the router: trust the TCP peer, which
    # WireGuard authenticates. Assumes no proxy in front of gunicorn.
    # https://doc.scalingo.com/platform/networking/private/concepts
    remote_addr = parse_ip(request.META.get("REMOTE_ADDR"))
    if remote_addr and ip_address(remote_addr) in SCALINGO_PRIVATE_NETWORK:
        return remote_addr
    # Scalingo's router sets X-Real-IP; X-Forwarded-For is client-controlled.
    # https://doc.scalingo.com/platform/networking/public/routing
    return parse_ip(request.headers.get("X-Real-IP"))
