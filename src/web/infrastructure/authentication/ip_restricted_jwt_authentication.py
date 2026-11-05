import logging
from typing import cast

from drf_spectacular.contrib.rest_framework_simplejwt import SimpleJWTScheme
from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from infrastructure.authentication.rejection import reject
from infrastructure.django_apps.commons.enums import Canal
from infrastructure.django_apps.users.models import UserModel
from infrastructure.django_apps.utils.ip import get_client_ip

REJECTION_MESSAGE = "Authentication failed."


def ensure_api_ip_allowed(
    user: UserModel,
    request: Request,
    *,
    message: str = REJECTION_MESSAGE,
    throttled: bool = True,
) -> None:
    if user.api_ip_is_allowed(get_client_ip(request)):
        return
    raise reject(
        request,
        canal=Canal.JWT,
        subject=f"JWT for user {user.pk}",
        reason="IP not allowed",
        message=message,
        utilisateur_id=user.username,
        # ERROR so Sentry raises an event: usually a partner whose IP changed.
        level=logging.ERROR,
        throttled=throttled,
    )


def ensure_refresh_ip_allowed(refresh: str, request: Request) -> None:
    token = RefreshToken(refresh)  # type: ignore[arg-type]  # stubs say Token
    user = IpRestrictedJWTAuthentication().get_user(token)
    ensure_api_ip_allowed(cast(UserModel, user), request)


class IpRestrictedJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        result = super().authenticate(request)
        if result is not None:
            ensure_api_ip_allowed(result[0], request)
        return result


class IpRestrictedJWTScheme(SimpleJWTScheme):
    target_class = (
        "infrastructure.authentication.ip_restricted_jwt_authentication"
        ".IpRestrictedJWTAuthentication"
    )
