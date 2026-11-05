from rest_framework.authentication import BaseAuthentication
from rest_framework.permissions import SAFE_METHODS, AllowAny, IsAuthenticated

from infrastructure.authentication.api_key_authentication import (
    ApiKeyAuthentication,
)
from infrastructure.authentication.ip_restricted_jwt_authentication import (
    IpRestrictedJWTAuthentication,
)
from infrastructure.authentication.session_authentication import (
    SessionApiAuthentication,
)


class PublicApiMixin:
    authentication_classes = [IpRestrictedJWTAuthentication, ApiKeyAuthentication]
    permission_classes = [IsAuthenticated]


class PublicJwtOnlyMixin:
    authentication_classes = [IpRestrictedJWTAuthentication]
    permission_classes = [IsAuthenticated]


class PublicApiKeyOnlyMixin:
    authentication_classes = [ApiKeyAuthentication]
    permission_classes = [IsAuthenticated]


class PublicJwtReadApiKeyWriteMixin:
    permission_classes = [IsAuthenticated]

    def get_authenticators(self):
        request = getattr(self, "request", None)
        if request is not None and request.method not in SAFE_METHODS:
            return [ApiKeyAuthentication()]
        return [IpRestrictedJWTAuthentication()]


class SessionApiMixin:
    authentication_classes = [SessionApiAuthentication]
    permission_classes = [IsAuthenticated]


class UnauthenticatedMixin:
    authentication_classes: list[type[BaseAuthentication]] = []
    permission_classes = [AllowAny]
