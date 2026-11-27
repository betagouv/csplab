from datetime import timedelta

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiResponse,
    extend_schema,
    extend_schema_serializer,
)
from rest_framework import serializers
from rest_framework_simplejwt.settings import api_settings


def _format_lifetime(lifetime: timedelta) -> str:
    seconds = int(lifetime.total_seconds())
    for unit_seconds, singular, plural in (
        (86400, "jour", "jours"),
        (3600, "heure", "heures"),
        (60, "minute", "minutes"),
    ):
        if seconds % unit_seconds == 0:
            count = seconds // unit_seconds
            return f"{count} {singular if count == 1 else plural}"
    return f"{seconds} secondes"


_ACCESS_LIFETIME = _format_lifetime(api_settings.ACCESS_TOKEN_LIFETIME)
_REFRESH_LIFETIME = _format_lifetime(api_settings.REFRESH_TOKEN_LIFETIME)

_ACCESS_HELP = (
    f"Jeton d'accès, valable {_ACCESS_LIFETIME}. À envoyer dans l'en-tête "
    "`Authorization: Bearer <jeton>` des autres routes."
)


@extend_schema_serializer(component_name="TokenObtainPair")
class TokenObtainPairDocSerializer(serializers.Serializer):
    email = serializers.CharField(write_only=True, help_text="Email du compte.")
    password = serializers.CharField(
        write_only=True, help_text="Mot de passe du compte."
    )
    access = serializers.CharField(read_only=True, help_text=_ACCESS_HELP)
    refresh = serializers.CharField(
        read_only=True,
        help_text=(
            f"Jeton de rafraîchissement, valable {_REFRESH_LIFETIME}. À envoyer à "
            "`POST /api/token/refresh` pour obtenir un nouveau jeton d'accès."
        ),
    )


@extend_schema_serializer(component_name="TokenRefresh")
class TokenRefreshDocSerializer(serializers.Serializer):
    refresh = serializers.CharField(
        write_only=True,
        help_text="Jeton de rafraîchissement obtenu avec `POST /api/token`.",
    )
    access = serializers.CharField(read_only=True, help_text=_ACCESS_HELP)


def _missing_fields_response(fields: list[str]) -> OpenApiResponse:
    return OpenApiResponse(
        response=OpenApiTypes.OBJECT,
        description="Champ obligatoire manquant.",
        examples=[
            OpenApiExample(
                "Error - missing field",
                summary="Champ obligatoire manquant",
                value={field: ["Ce champ est obligatoire."] for field in fields},
                response_only=True,
                status_codes=["400"],
            )
        ],
    )


obtain_token_schema = extend_schema(
    summary="Obtenir un jeton",
    description=(
        "Échange l'email et le mot de passe d'un compte contre un jeton d'accès, "
        f"valable {_ACCESS_LIFETIME}, et un jeton de rafraîchissement, valable "
        f"{_REFRESH_LIFETIME}."
    ),
    request=TokenObtainPairDocSerializer,
    responses={
        200: OpenApiResponse(
            response=TokenObtainPairDocSerializer, description="Jetons obtenus."
        ),
        400: _missing_fields_response(["email", "password"]),
        401: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            description=(
                "Email ou mot de passe incorrect, compte désactivé, ou adresse IP "
                "non autorisée pour ce compte. Le message est le même dans tous "
                "les cas."
            ),
            examples=[
                OpenApiExample(
                    "Error - invalid credentials",
                    summary="Identifiants invalides",
                    value={
                        "detail": (
                            "Aucun compte actif n'a été trouvé avec les "
                            "identifiants fournis"
                        )
                    },
                    response_only=True,
                    status_codes=["401"],
                )
            ],
        ),
    },
)

refresh_token_schema = extend_schema(
    summary="Rafraîchir un jeton",
    description=(
        "Échange un jeton de rafraîchissement valide contre un nouveau jeton "
        f"d'accès, valable {_ACCESS_LIFETIME}. Le jeton de rafraîchissement reste "
        "le même : obtenez-en un nouveau avec `POST /api/token` quand il expire."
    ),
    request=TokenRefreshDocSerializer,
    responses={
        200: OpenApiResponse(
            response=TokenRefreshDocSerializer, description="Jeton d'accès obtenu."
        ),
        400: _missing_fields_response(["refresh"]),
        401: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            description=(
                "Jeton de rafraîchissement invalide, expiré ou révoqué, compte "
                "désactivé, ou adresse IP non autorisée pour ce compte."
            ),
            examples=[
                OpenApiExample(
                    "Error - invalid token",
                    summary="Jeton invalide ou expiré",
                    value={"detail": "Token is invalid", "code": "token_not_valid"},
                    response_only=True,
                    status_codes=["401"],
                )
            ],
        ),
    },
)
