from rest_framework.authentication import BaseAuthentication
from rest_framework.permissions import SAFE_METHODS, AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from infrastructure.authentication.api_key_authentication import (
    ApiKeyAuthentication,
)
from infrastructure.authentication.session_authentication import (
    SessionApiAuthentication,
)


class PublicApiMixin:
    authentication_classes = [JWTAuthentication, ApiKeyAuthentication]
    permission_classes = [IsAuthenticated]


class PublicJwtOnlyMixin:
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


class PublicApiKeyOnlyMixin:
    authentication_classes = [ApiKeyAuthentication]
    permission_classes = [IsAuthenticated]


class PublicJwtReadApiKeyWriteMixin:
    """Reads (GET, HEAD, OPTIONS) by JWT, writes by API key."""

    permission_classes = [IsAuthenticated]

    def get_authenticators(self):
        request = getattr(self, "request", None)
        if request is not None and request.method not in SAFE_METHODS:
            return [ApiKeyAuthentication()]
        return [JWTAuthentication()]


class SessionApiMixin:
    authentication_classes = [SessionApiAuthentication]
    permission_classes = [IsAuthenticated]


class UnauthenticatedMixin:
    authentication_classes: list[type[BaseAuthentication]] = []
    permission_classes = [AllowAny]
