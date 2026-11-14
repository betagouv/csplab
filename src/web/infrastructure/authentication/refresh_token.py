from drf_spectacular.contrib.rest_framework_simplejwt import (
    TokenObtainPairSerializerExtension,
)
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer as BaseTokenObtainPairSerializer,
)
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from rest_framework_simplejwt.tokens import BlacklistMixin, RefreshToken
from rest_framework_simplejwt.utils import datetime_from_epoch


class UnstoredRefreshToken(RefreshToken):
    @classmethod
    def for_user(cls, user):
        return super(BlacklistMixin, cls).for_user(user)


def track_refresh_token(user, refresh: str) -> None:
    token = RefreshToken(refresh, verify=False)  # type: ignore[arg-type]
    OutstandingToken.objects.create(
        user=user,
        jti=token[api_settings.JTI_CLAIM],
        token="",
        created_at=token.current_time,
        expires_at=datetime_from_epoch(token["exp"]),
    )


class TokenObtainPairSerializer(BaseTokenObtainPairSerializer):
    token_class = UnstoredRefreshToken


class UnstoredTokenObtainPairSerializerExtension(TokenObtainPairSerializerExtension):
    target_class = (
        "infrastructure.authentication.refresh_token.TokenObtainPairSerializer"
    )
