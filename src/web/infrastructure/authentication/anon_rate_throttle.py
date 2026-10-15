from rest_framework.throttling import AnonRateThrottle

from infrastructure.django_apps.utils.ip import get_client_ip

# Shared bucket for requests without a usable X-Real-IP. Scalingo's router
# always sets it, so this only happens outside the router (local, tests):
# such requests share one counter instead of escaping the limit.
UNKNOWN_CLIENT_IDENT = "unknown"


class ClientIpAnonRateThrottle(AnonRateThrottle):
    """
    AnonRateThrottle keyed on get_client_ip(). DRF's default get_ident() uses
    the whole X-Forwarded-For header when NUM_PROXIES is unset: the router
    appends to it but keeps client-sent values, so changing it on every
    request would get a fresh counter each time.
    """

    def get_ident(self, request):
        return get_client_ip(request) or UNKNOWN_CLIENT_IDENT
