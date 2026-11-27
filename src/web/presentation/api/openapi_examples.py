from drf_spectacular.utils import OpenApiExample

from infrastructure.authentication.ip_restricted_jwt_authentication import (
    REJECTION_MESSAGE,
)

INVALID_JWT = OpenApiExample(
    "Error - invalid JWT",
    summary="Jeton JWT invalide ou expiré",
    description=(
        "Le jeton JWT du header `Authorization` est invalide ou expiré. "
        "Un jeton expiré renvoie le même corps, avec le message "
        "`Token is expired`."
    ),
    value={
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
    response_only=True,
    status_codes=["401"],
)

JWT_IP_NOT_ALLOWED = OpenApiExample(
    "Error - JWT IP not allowed",
    summary="Adresse IP non autorisée (jeton JWT)",
    description=(
        "Le compte n'accepte que certaines adresses IP, et l'appel vient d'une "
        "autre adresse."
    ),
    value={"detail": REJECTION_MESSAGE},
    response_only=True,
    status_codes=["401"],
)

INVALID_API_KEY = OpenApiExample(
    "Error - invalid API key",
    summary="Clé d'API invalide",
    description="La clé d'API du header `Authorization` est inconnue.",
    value={"detail": "Invalid API key."},
    response_only=True,
    status_codes=["401"],
)

API_KEY_IP_NOT_ALLOWED = OpenApiExample(
    "Error - API key IP not allowed",
    summary="Adresse IP non autorisée (clé d'API)",
    description="La clé d'API est utilisée depuis une adresse IP non autorisée.",
    value={"detail": "IP address not allowed."},
    response_only=True,
    status_codes=["401"],
)

JWT_ON_API_KEY_ROUTE = OpenApiExample(
    "Error - JWT on API key route",
    summary="Appel avec un jeton JWT",
    description=(
        "La route n'accepte que la clé d'API de CSPLab : un jeton JWT n'est "
        "pas reconnu."
    ),
    value={"detail": "Informations d'authentification non fournies."},
    response_only=True,
    status_codes=["401"],
)
