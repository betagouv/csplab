import time
from typing import Callable, Optional

from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.core.cache import cache
from django.http import HttpRequest, HttpResponse
from rest_framework.throttling import SimpleRateThrottle, UserRateThrottle
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed, TokenError

from infrastructure.authentication.anon_rate_throttle import ClientIpAnonRateThrottle
from infrastructure.authentication.api_key_authentication import (
    ApiKeyRateThrottle,
    ApiKeyRateThrottleDaily,
)
from infrastructure.authentication.jwt_token import get_validated_jwt

_API_KEY_THROTTLES = [ApiKeyRateThrottle(), ApiKeyRateThrottleDaily()]
_USER_THROTTLE = UserRateThrottle()
_ANON_THROTTLE = ClientIpAnonRateThrottle()
_jwt_auth = JWTAuthentication()


def _is_authenticated_api_key_request(request: HttpRequest) -> bool:
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Api-Key "):
        return False
    return auth_header[len("Api-Key ") :] == settings.INGESTION_API_KEY


def _authenticate_jwt_user(request: HttpRequest) -> Optional[AbstractBaseUser]:
    validated_token = get_validated_jwt(request, _jwt_auth)
    if validated_token is None:
        return None
    try:
        return _jwt_auth.get_user(validated_token)
    except (AuthenticationFailed, TokenError):
        return None


def _rate_limit_state(throttle: SimpleRateThrottle, ident: str) -> tuple[int, int, int]:
    cache_key = throttle.cache_format % {"scope": throttle.scope, "ident": ident}
    num_requests, duration = throttle.parse_rate(throttle.get_rate())
    history = cache.get(cache_key, [])
    remaining = max(num_requests - len(history), 0)
    reset = int(history[-1] + duration) if history else int(time.time())
    return num_requests, remaining, reset


def _view_throttle_scopes(request: HttpRequest) -> set[str]:
    resolver_match = getattr(request, "resolver_match", None)
    if resolver_match is None:
        return set()
    view_class: type[APIView] | None = getattr(resolver_match.func, "cls", None)
    if view_class is None or not issubclass(view_class, APIView):
        return set()
    return {
        scope
        for throttle_class in view_class.throttle_classes
        if (scope := getattr(throttle_class, "scope", None))
    }


def _throttles_for_caller(
    request: HttpRequest,
) -> list[tuple[SimpleRateThrottle, str]]:
    if _is_authenticated_api_key_request(request):
        return [(throttle, "ingestion-api-key") for throttle in _API_KEY_THROTTLES]
    user = _authenticate_jwt_user(request)
    if user is not None:
        return [(_USER_THROTTLE, str(user.pk))]
    if not request.headers.get("Authorization") and request.path.startswith(
        settings.PUBLIC_API_PREFIX
    ):
        return [(_ANON_THROTTLE, _ANON_THROTTLE.get_ident(request))]
    return []


def _collect_rate_limit_states(request: HttpRequest) -> list[tuple[int, int, int]]:
    scopes = _view_throttle_scopes(request)
    if not scopes:
        return []
    return [
        _rate_limit_state(throttle, ident)
        for throttle, ident in _throttles_for_caller(request)
        if throttle.scope in scopes
    ]


class RateLimitHeadersMiddleware:
    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        response = self.get_response(request)

        states = _collect_rate_limit_states(request)
        if not states:
            return response

        limit, remaining, reset = min(states, key=lambda state: state[1])
        response["X-RateLimit-Limit"] = str(limit)
        response["X-RateLimit-Remaining"] = str(remaining)
        response["X-RateLimit-Reset"] = str(reset)

        return response
