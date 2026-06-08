import base64
import hashlib
import json
from datetime import datetime, timezone
from typing import Callable, Optional
from uuid import uuid4

from django.http import HttpRequest, HttpResponse
from referentiel.entities.api_log import ApiLog
from referentiel.repositories.api_log_repository_interface import IApiLogRepository

from infrastructure.di.shared.shared_container import SharedContainer

_API_PREFIX = "/api/"


def _get_ip_address(request: HttpRequest) -> str:
    forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "")


_JWT_PARTS_COUNT = 3


def _decode_jwt_user_id(raw_token: str) -> Optional[str]:
    """Extract user_id from JWT payload without signature verification."""
    try:
        parts = raw_token.split(".")
        if len(parts) != _JWT_PARTS_COUNT:
            return None
        padding = "=" * (4 - len(parts[1]) % 4)
        payload = json.loads(base64.urlsafe_b64decode(parts[1] + padding))
        user_id = payload.get("user_id")
        return str(user_id) if user_id is not None else None
    except Exception:
        return None


def _extract_token_info(
    request: HttpRequest,
) -> tuple[Optional[str], Optional[str]]:
    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        raw_token = auth_header[len("Bearer ") :]
        return _decode_jwt_user_id(raw_token), "jwt"
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
