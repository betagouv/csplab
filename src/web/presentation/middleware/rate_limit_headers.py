import time
from typing import Callable, Optional

from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.core.cache import cache
from django.http import HttpRequest, HttpResponse
from rest_framework.throttling import (
    AnonRateThrottle,
    SimpleRateThrottle,
    UserRateThrottle,
)
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed, TokenError

from infrastructure.authentication.api_key_authentication import (
    ApiKeyRateThrottle,
    ApiKeyRateThrottleDaily,
)

_API_KEY_THROTTLES = [ApiKeyRateThrottle(), ApiKeyRateThrottleDaily()]
_USER_THROTTLE = UserRateThrottle()
_ANON_THROTTLE = AnonRateThrottle()
_jwt_auth = JWTAuthentication()


def _is_authenticated_api_key_request(request: HttpRequest) -> bool:
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Api-Key "):
        return False
    return auth_header[len("Api-Key ") :] == settings.INGESTION_API_KEY


def _authenticate_jwt_user(request: HttpRequest) -> Optional[AbstractBaseUser]:
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return None
    try:
        header = _jwt_auth.get_header(request)
        if header is None:
            return None
        raw_token = _jwt_auth.get_raw_token(header)
        if raw_token is None:
            return None
        validated_token = _jwt_auth.get_validated_token(raw_token)
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


def _collect_rate_limit_states(request: HttpRequest) -> list[tuple[int, int, int]]:
    if _is_authenticated_api_key_request(request):
        return [
            _rate_limit_state(throttle, "ingestion-api-key")
            for throttle in _API_KEY_THROTTLES
        ]
    user = _authenticate_jwt_user(request)
    if user is not None:
        return [_rate_limit_state(_USER_THROTTLE, str(user.pk))]
    if not request.headers.get("Authorization") and request.path.startswith(
        settings.PUBLIC_API_PREFIX
    ):
        ident = _ANON_THROTTLE.get_ident(request)
        return [_rate_limit_state(_ANON_THROTTLE, ident)]
    return []


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
