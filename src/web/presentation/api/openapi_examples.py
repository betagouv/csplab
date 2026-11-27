from drf_spectacular.utils import OpenApiExample

from infrastructure.authentication.api_key_authentication import (
    INVALID_API_KEY_MESSAGE,
    IP_NOT_ALLOWED_MESSAGE,
)
from infrastructure.authentication.ip_restricted_jwt_authentication import (
    REJECTION_MESSAGE,
)


def _unauthorized(name: str, summary: str, value: dict) -> OpenApiExample:
    return OpenApiExample(
        name, summary=summary, value=value, response_only=True, status_codes=["401"]
    )


INVALID_JWT = _unauthorized(
    "Error - invalid JWT",
    "Jeton JWT invalide ou expiré",
    {
        "detail": "Le type de jeton fourni n'est pas valide",
        "code": "token_not_valid",
        "messages": [
            {
                "token_class": "AccessToken",
                "token_type": "access",
                "message": "Token is invalid",
            }
        ],
    },
)
JWT_IP_NOT_ALLOWED = _unauthorized(
    "Error - JWT IP not allowed",
    "Adresse IP non autorisée (jeton JWT)",
    {"detail": REJECTION_MESSAGE},
)
INVALID_API_KEY = _unauthorized(
    "Error - invalid API key",
    "Clé d'API invalide",
    {"detail": INVALID_API_KEY_MESSAGE},
)
API_KEY_IP_NOT_ALLOWED = _unauthorized(
    "Error - API key IP not allowed",
    "Adresse IP non autorisée (clé d'API)",
    {"detail": IP_NOT_ALLOWED_MESSAGE},
)
JWT_ON_API_KEY_ROUTE = _unauthorized(
    "Error - JWT on API key route",
    "Appel avec un jeton JWT sur une route réservée à la clé d'API",
    {"detail": "Informations d'authentification non fournies."},
)
