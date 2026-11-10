from django.conf import settings
from drf_spectacular.extensions import OpenApiAuthenticationExtension
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed, Throttled
from rest_framework.throttling import SimpleRateThrottle, UserRateThrottle

from infrastructure.authentication.rejection import reject
from infrastructure.django_apps.commons.enums import Canal
from infrastructure.django_apps.utils.ip import get_client_ip, ip_in_networks


class _IngestionApiKeyUser:
    is_authenticated = True
    pk = "ingestion-api-key"


def _reject(reason: str, message: str, request) -> AuthenticationFailed | Throttled:
    # Never log the submitted key.
    return reject(
        request,
        canal=Canal.APIKEY,
        subject="Ingestion API key",
        reason=reason,
        message=message,
    )


class ApiKeyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Api-Key "):
            return None
        key = auth_header[len("Api-Key ") :]
        if key != settings.INGESTION_API_KEY:
            raise _reject("invalid key", "Invalid API key.", request)
        allowed_ranges = settings.INGESTION_API_KEY_ALLOWED_IP_RANGES
        if allowed_ranges and not ip_in_networks(
            get_client_ip(request), allowed_ranges
        ):
            raise _reject("IP not allowed", "IP address not allowed.", request)
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


class ApiKeyRateThrottleDaily(ApiKeyRateThrottle):
    scope = "api_key_daily"


class NonApiKeyUserRateThrottle(UserRateThrottle):
    """
    UserRateThrottle that skips ingestion API key requests, which are rate-limited
    by ApiKeyRateThrottle / ApiKeyRateThrottleDaily instead.
    """

    def get_cache_key(self, request, view):
        if isinstance(request.user, _IngestionApiKeyUser):
            return None
        return super().get_cache_key(request, view)
