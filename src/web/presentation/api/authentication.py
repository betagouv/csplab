from rest_framework.authentication import BaseAuthentication, SessionAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from infrastructure.authentication.api_key_authentication import (
    ApiKeyAuthentication,
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
