from dataclasses import dataclass
from enum import Enum

from drf_spectacular.openapi import AutoSchema as SpectacularAutoSchema
from drf_spectacular.plumbing import build_examples_list
from rest_framework.authentication import BaseAuthentication
from rest_framework.serializers import Serializer
from rest_framework.throttling import BaseThrottle, SimpleRateThrottle
from rest_framework.views import APIView

from infrastructure.authentication.api_key_authentication import (
    ApiKeyAuthentication,
    ApiKeyRateThrottle,
    NonApiKeyUserRateThrottle,
)
from infrastructure.authentication.ip_restricted_jwt_authentication import (
    IpRestrictedJWTAuthentication,
)
from infrastructure.authentication.rate_throttle import (
    ClientIpAnonRateThrottle,
    DocumentationRateThrottle,
)
from infrastructure.authentication.rejection import AuthRejectionRateThrottle
from presentation.api.openapi_examples import (
    API_KEY_IP_NOT_ALLOWED,
    INVALID_API_KEY,
    INVALID_JWT,
    JWT_IP_NOT_ALLOWED,
    JWT_ON_API_KEY_ROUTE,
)
from presentation.api.openapi_hooks import PUBLIC_PATH
from presentation.api.serializers import DetailErrorSerializer, TokenErrorSerializer


class Caller(Enum):
    JWT = "Avec un jeton JWT"
    API_KEY = "Avec une clé d'API"
    ANONYMOUS = "Sans authentification"


@dataclass(frozen=True)
class _ThrottleDoc:
    throttle_class: type[SimpleRateThrottle]
    callers: frozenset[Caller]
    counted: str


# Subclasses first: the first isinstance match wins.
_THROTTLE_DOCS = [
    _ThrottleDoc(DocumentationRateThrottle, frozenset(Caller), "par adresse IP"),
    _ThrottleDoc(
        ClientIpAnonRateThrottle, frozenset({Caller.ANONYMOUS}), "par adresse IP"
    ),
    _ThrottleDoc(NonApiKeyUserRateThrottle, frozenset({Caller.JWT}), "par utilisateur"),
    _ThrottleDoc(ApiKeyRateThrottle, frozenset({Caller.API_KEY}), "par clé d'API"),
]

_AUTHENTICATION_CALLERS = {
    IpRestrictedJWTAuthentication: Caller.JWT,
    ApiKeyAuthentication: Caller.API_KEY,
}


_UNAUTHORIZED_EXAMPLES = {
    Caller.JWT: [INVALID_JWT, JWT_IP_NOT_ALLOWED],
    Caller.API_KEY: [INVALID_API_KEY, API_KEY_IP_NOT_ALLOWED],
}

_CUMULATIVE_NOTE = (
    "Les limites d'un même mode d'authentification se cumulent : "
    "la première atteinte bloque l'appel."
)

_PERIODS = {"s": "seconde", "m": "minute", "h": "heure", "d": "jour"}


def format_rate(rate: str) -> str:
    count, period = rate.split("/")
    formatted_count = f"{int(count):,}".replace(",", " ")
    noun = "appel" if int(count) == 1 else "appels"
    return f"{formatted_count} {noun} par {_PERIODS[period[0]]}"


def _throttle_doc(throttle: BaseThrottle) -> _ThrottleDoc:
    for doc in _THROTTLE_DOCS:
        if isinstance(throttle, doc.throttle_class):
            return doc
    raise ValueError(
        f"{type(throttle).__name__} is not documented: add it to _THROTTLE_DOCS."
    )


def _callers(authenticators: list[BaseAuthentication]) -> list[Caller]:
    if not authenticators:
        return [Caller.ANONYMOUS]
    callers = []
    for authenticator in authenticators:
        caller = _AUTHENTICATION_CALLERS.get(type(authenticator))
        if caller is None:
            raise ValueError(
                f"{type(authenticator).__name__} is not documented: "
                "add it to _AUTHENTICATION_CALLERS."
            )
        callers.append(caller)
    return callers


def rate_limits_markdown(view: APIView) -> str:
    authenticators = view.get_authenticators()
    throttles = view.get_throttles()
    rows = []
    for caller in _callers(authenticators):
        for throttle in throttles:
            doc = _throttle_doc(throttle)
            if caller in doc.callers and throttle.rate:
                rows.append((caller.value, format_rate(throttle.rate), doc.counted))
    # Raised by reject() itself, before the view throttles.
    rejection_rate = AuthRejectionRateThrottle.THROTTLE_RATES.get(
        AuthRejectionRateThrottle.scope
    )
    rejects = authenticators or getattr(view, "throttles_auth_rejection", False)
    if rejects and rejection_rate:
        rows.append(
            ("Authentification refusée", format_rate(rejection_rate), "par adresse IP")
        )
    if not rows:
        return ""
    lines = [
        "**Limites d'appels**",
        "",
        "| Appel | Limite | Décompte |",
        "|---|---|---|",
        *(f"| {caller} | {rate} | {counted} |" for caller, rate, counted in rows),
    ]
    callers = [caller for caller, _, _ in rows]
    if len(set(callers)) < len(callers):
        lines += ["", _CUMULATIVE_NOTE]
    return "\n".join(lines)


class AutoSchema(SpectacularAutoSchema):
    def get_operation(self, path, path_regex, path_prefix, method, registry):
        operation = super().get_operation(
            path, path_regex, path_prefix, method, registry
        )
        if operation is None or not path.startswith(PUBLIC_PATH):
            return operation
        description = operation.get("description", "").rstrip()
        operation["description"] = "\n\n".join(
            part for part in (description, rate_limits_markdown(self.view)) if part
        )
        callers = _callers(self.view.get_authenticators())
        if callers != [Caller.ANONYMOUS]:
            responses = {**operation["responses"], "401": self._unauthorized(callers)}
            operation["responses"] = dict(sorted(responses.items()))
        return operation

    def _unauthorized(self, callers: list[Caller]) -> dict:
        examples = [e for caller in callers for e in _UNAUTHORIZED_EXAMPLES[caller]]
        serializers: list[type[Serializer]] = [DetailErrorSerializer]
        if Caller.JWT in callers:
            serializers.insert(0, TokenErrorSerializer)
        else:
            examples.append(JWT_ON_API_KEY_ROUTE)
        refs = [self.resolve_serializer(s, "response").ref for s in serializers]
        return {
            "description": "Authentification absente ou refusée.",
            "content": {
                "application/json": {
                    "schema": refs[0] if len(refs) == 1 else {"anyOf": refs},
                    "examples": build_examples_list(examples),
                }
            },
        }
