from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView as SimpleJWTTokenRefreshView

from application.identite.context_services.login_log import (
    log_login_failed,
    log_login_succeeded,
)
from infrastructure.django_apps.commons.enums import Canal
from infrastructure.django_apps.utils.ip import get_client_ip
from presentation.api.authentication import UnauthenticatedMixin


class LoggedTokenObtainPairView(  # type: ignore[misc]
    UnauthenticatedMixin, TokenObtainPairView
):
    def post(self, request: Request, *args, **kwargs) -> Response:
        email = str(request.data.get("email", ""))
        ip_address = get_client_ip(request)
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except AuthenticationFailed:
            log_login_failed(canal=Canal.JWT, email=email, ip_address=ip_address)
            raise
        except TokenError as e:
            raise InvalidToken(e.args[0]) from e
        log_login_succeeded(
            canal=Canal.JWT, user=serializer.user, ip_address=ip_address
        )
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class TokenRefreshView(  # type: ignore[misc]
    UnauthenticatedMixin, SimpleJWTTokenRefreshView
):
    pass
