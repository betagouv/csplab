import ipaddress

from django.conf import settings
from drf_spectacular.extensions import OpenApiAuthenticationExtension
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.throttling import SimpleRateThrottle, UserRateThrottle


class _IngestionApiKeyUser:
    is_authenticated = True
    pk = "ingestion-api-key"


def _get_client_ip(request) -> str:
    forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "")


def _ip_is_allowed(ip: str, allowed_ranges: list[str]) -> bool:
    if not allowed_ranges:
        return True
    try:
        client_ip = ipaddress.ip_address(ip)
        return any(
            client_ip in ipaddress.ip_network(cidr, strict=False)
            for cidr in allowed_ranges
        )
    except ValueError:
        return False


class ApiKeyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Api-Key "):
            return None
        key = auth_header[len("Api-Key ") :]
        if key != settings.INGESTION_API_KEY:
            raise AuthenticationFailed("Invalid API key.")
        allowed_ranges = settings.INGESTION_API_KEY_ALLOWED_IP_RANGES
        if allowed_ranges and not _ip_is_allowed(
            _get_client_ip(request), allowed_ranges
        ):
            raise AuthenticationFailed("IP address not allowed.")
        return (_IngestionApiKeyUser(), None)

    def authenticate_header(self, request):
        # See https://www.django-rest-framework.org/api-guide/authentication/#custom-authentication
        return "Api-Key"


class ApiKeyAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = ApiKeyAuthentication
    name = "ApiKeyAuth"

    def get_security_definition(self, auto_schema):
        return {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": "API key authentication. Use the format: `Api-Key <key>`.",
        }


class ApiKeyRateThrottle(SimpleRateThrottle):
    scope = "api_key"

    def get_cache_key(self, request, view):
        if isinstance(request.user, _IngestionApiKeyUser):
            return self.cache_format % {
                "scope": self.scope,
                "ident": "ingestion-api-key",
            }
        return None


class UserRateThrottleExceptApiKey(UserRateThrottle):
    def allow_request(self, request, view):
        if isinstance(request.user, _IngestionApiKeyUser):
            return True
        return super().allow_request(request, view)
