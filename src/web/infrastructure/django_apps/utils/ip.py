from ipaddress import IPv4Address, IPv6Address, ip_address, ip_network

IPAddressInput = str | IPv4Address | IPv6Address

# Fixed address range of Scalingo private networks.
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
    # Requests from the Scalingo private network bypass the router: X-Real-IP
    # is then missing or forged by the caller, and REMOTE_ADDR is the peer.
    # REMOTE_ADDR is trusted because gunicorn sets it from the TCP socket and
    # WireGuard only accepts a 10.240.x.y source from an authenticated peer.
    # This breaks if gunicorn runs with --proxy-protocol, if a middleware
    # rewrites REMOTE_ADDR from a header, or if a proxy (e.g. nginx) sits in
    # front of gunicorn in the container.
    # https://doc.scalingo.com/platform/networking/private/concepts
    remote_addr = parse_ip(request.META.get("REMOTE_ADDR"))
    if remote_addr and ip_address(remote_addr) in SCALINGO_PRIVATE_NETWORK:
        return remote_addr
    # Otherwise, Scalingo's router sets X-Real-IP to the connecting client's
    # IP, whereas X-Forwarded-For is client-controlled and REMOTE_ADDR is the
    # router's.
    # https://doc.scalingo.com/platform/networking/public/routing
    return parse_ip(request.headers.get("X-Real-IP"))
