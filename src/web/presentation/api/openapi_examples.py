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
    "Erreur - jeton JWT invalide",
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
    "Erreur - IP interdite avec JWT",
    "Adresse IP non autorisée (jeton JWT)",
    {"detail": REJECTION_MESSAGE},
)
INVALID_API_KEY = _unauthorized(
    "Erreur - cle API invalide",
    "Clé d'API invalide",
    {"detail": INVALID_API_KEY_MESSAGE},
)
API_KEY_IP_NOT_ALLOWED = _unauthorized(
    "Erreur - IP interdite avec cle API",
    "Adresse IP non autorisée (clé d'API)",
    {"detail": IP_NOT_ALLOWED_MESSAGE},
)
JWT_ON_API_KEY_ROUTE = _unauthorized(
    "Erreur - JWT sur route cle API",
    "Appel avec un jeton JWT sur une route réservée à la clé d'API",
    {"detail": "Informations d'authentification non fournies."},
)
