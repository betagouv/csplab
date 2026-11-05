from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTAuthentication

from infrastructure.authentication.rejection import reject
from infrastructure.django_apps.commons.enums import Canal
from infrastructure.django_apps.users.models import UserModel
from infrastructure.django_apps.utils.ip import get_client_ip

REJECTION_MESSAGE = "Authentication failed."


def ensure_api_ip_allowed(
    user: UserModel, request: Request, *, message: str = REJECTION_MESSAGE
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
    )


class IpRestrictedJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        result = super().authenticate(request)
        if result is not None:
            ensure_api_ip_allowed(result[0], request)
        return result
