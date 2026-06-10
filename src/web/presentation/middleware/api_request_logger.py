import hashlib
from datetime import datetime, timezone
from typing import Callable, Optional
from uuid import uuid4

from django.http import HttpRequest, HttpResponse
from referentiel.entities.api_log import ApiLog
from referentiel.repositories.api_log_repository_interface import IApiLogRepository
from rest_framework_simplejwt.authentication import JWTStatelessUserAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

from infrastructure.di.shared.shared_container import SharedContainer

_API_PREFIX = "/api/"


def _get_ip_address(request: HttpRequest) -> str:
    forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "")


_jwt_auth = JWTStatelessUserAuthentication()


def _decode_jwt_user_id(request: HttpRequest) -> Optional[str]:
    try:
        header = _jwt_auth.get_header(request)
        if header is None:
            return None
        raw_token = _jwt_auth.get_raw_token(header)
        if raw_token is None:
            return None
        validated_token = _jwt_auth.get_validated_token(raw_token)
        user = _jwt_auth.get_user(validated_token)
        return str(user.pk)
    except (InvalidToken, TokenError):
        return None


def _extract_token_info(
    request: HttpRequest,
) -> tuple[Optional[str], Optional[str]]:
    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        return _decode_jwt_user_id(request), "jwt"
    if auth_header.startswith("Api-Key "):
        raw_key = auth_header[len("Api-Key ") :]
        return hashlib.sha256(raw_key.encode()).hexdigest(), "api_key"
    return None, None


class ApiRequestLoggerMiddleware:
    def __init__(
        self,
        get_response: Callable[[HttpRequest], HttpResponse],
        repository: Optional[IApiLogRepository] = None,
    ) -> None:
        self.get_response = get_response
        self._repository = repository or SharedContainer().api_log_repository()

    def __call__(self, request: HttpRequest) -> HttpResponse:
        response = self.get_response(request)

        if request.path.startswith(_API_PREFIX):
            token, token_type = _extract_token_info(request)
            api_log = ApiLog(
                id=uuid4(),
                timestamp=datetime.now(tz=timezone.utc),
                path=request.path,
                ip_address=_get_ip_address(request),
                method=request.method or "",
                status_code=response.status_code,
                auth_token=token,
                token_type=token_type,
            )
            self._repository.save(api_log)

        return response
