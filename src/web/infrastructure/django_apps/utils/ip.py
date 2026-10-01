from ipaddress import IPv4Address, IPv6Address, ip_address

IPAddressInput = str | IPv4Address | IPv6Address


def parse_ip(raw: IPAddressInput | None) -> str | None:
    """Normalized IP string, or None when `raw` is empty or not an IP."""
    if not raw:
        return None
    try:
        return str(ip_address(str(raw).strip()))
    except ValueError:
        return None


def get_client_ip(request) -> str | None:
    # Scalingo's router sets X-Real-IP to the connecting client's IP, whereas
    # X-Forwarded-For is client-controlled and REMOTE_ADDR is the router's.
    # https://doc.scalingo.com/platform/networking/public/routing
    return parse_ip(request.headers.get("X-Real-IP"))
