import ipaddress
import logging

from django.conf import settings
from drf_spectacular.extensions import OpenApiAuthenticationExtension
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed, Throttled
from rest_framework.throttling import SimpleRateThrottle, UserRateThrottle

from config.logger_names import LoggerName
from infrastructure.django_apps.commons.enums import Canal, Resultat
from infrastructure.django_apps.commons.models import AuditLoginLogModel
from infrastructure.django_apps.utils.ip import get_client_ip

logger = logging.getLogger(LoggerName.IDENTITE)


class _IngestionApiKeyUser:
    is_authenticated = True
    pk = "ingestion-api-key"


def _ip_is_allowed(ip: str | None, allowed_ranges: list[str]) -> bool:
    if not allowed_ranges:
        return True
    if ip is None:
        return False
    try:
        client_ip = ipaddress.ip_address(ip)
        return any(
            client_ip in ipaddress.ip_network(cidr, strict=False)
            for cidr in allowed_ranges
        )
    except ValueError:
        return False


class ApiKeyRejectionRateThrottle(SimpleRateThrottle):
    """
    Counts rejected API key attempts per client IP. DRF authenticates before
    running DEFAULT_THROTTLE_CLASSES, so a rejected key never reaches them:
    without this, every rejection would write an audit row with no limit.
    """

    scope = "api_key_rejection"

    def get_cache_key(self, request, view):
        return self.cache_format % {
            "scope": self.scope,
            "ident": get_client_ip(request),
        }


def _reject(reason: str, message: str, request) -> AuthenticationFailed | Throttled:
    throttle = ApiKeyRejectionRateThrottle()
    if not throttle.allow_request(request, view=None):
        return Throttled(wait=throttle.wait())
    _log_rejection(reason, request)
    return AuthenticationFailed(message)


def _log_rejection(reason: str, request) -> None:
    # Never log the submitted key.
    ip_address = get_client_ip(request)
    logger.warning("Ingestion API key rejected (%s) from %s.", reason, ip_address)
    AuditLoginLogModel.objects.record_attempt(
        canal=Canal.APIKEY, resultat=Resultat.ECHEC, ip_address=ip_address
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
        if allowed_ranges and not _ip_is_allowed(
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
