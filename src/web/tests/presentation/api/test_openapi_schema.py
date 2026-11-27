from pathlib import Path
from unittest.mock import patch

import pytest
import yaml
from rest_framework.authentication import SessionAuthentication
from rest_framework.throttling import ScopedRateThrottle, SimpleRateThrottle
from rest_framework.views import APIView

from presentation.api.authentication import UnauthenticatedMixin
from presentation.api.openapi_schema import format_rate, rate_limits_markdown
from presentation.api.token_views import TokenRefreshView
from presentation.api.views import ChangelogJsonView
from presentation.ingestion.views.offers import OffersListView
from presentation.ingestion.views.organismes import OrganismesUpsertView

_RATES = {
    "anon": "5/minute",
    "documentation": "60/minute",
    "user": "120/minute",
    "api_key": "70000/hour",
    "api_key_daily": "100000/day",
    "auth_rejection": "10/minute",
}


_CUMULATIVE_NOTE = (
    "Les limites d'un même mode d'authentification se cumulent : "
    "la première atteinte bloque l'appel."
)


def _table(*rows: str, note: str | None = None) -> str:
    lines = [
        "**Limites d'appels**",
        "",
        "| Appel | Limite | Décompte |",
        "|---|---|---|",
        *rows,
    ]
    if note:
        lines += ["", note]
    return "\n".join(lines)


class TestFormatRate:
    @pytest.mark.parametrize(
        "rate, expected",
        [
            ("5/minute", "5 appels par minute"),
            ("1/second", "1 appel par seconde"),
            ("70000/hour", "70 000 appels par heure"),
            ("100000/day", "100 000 appels par jour"),
        ],
    )
    def test_formats_drf_rate_in_french(self, rate, expected):
        assert format_rate(rate) == expected


@patch.object(SimpleRateThrottle, "THROTTLE_RATES", _RATES)
class TestRateLimitsMarkdown:
    def test_jwt_and_api_key_view(self):
        assert rate_limits_markdown(OffersListView()) == _table(
            "| Avec un jeton JWT | 120 appels par minute | par utilisateur |",
            "| Avec une clé d'API | 70 000 appels par heure | par clé d'API |",
            "| Avec une clé d'API | 100 000 appels par jour | par clé d'API |",
            "| Authentification refusée | 10 appels par minute | par adresse IP |",
            note=_CUMULATIVE_NOTE,
        )

    def test_api_key_only_view(self):
        assert rate_limits_markdown(OrganismesUpsertView()) == _table(
            "| Avec une clé d'API | 70 000 appels par heure | par clé d'API |",
            "| Avec une clé d'API | 100 000 appels par jour | par clé d'API |",
            "| Authentification refusée | 10 appels par minute | par adresse IP |",
            note=_CUMULATIVE_NOTE,
        )

    def test_documentation_view(self):
        assert rate_limits_markdown(ChangelogJsonView()) == _table(
            "| Sans authentification | 60 appels par minute | par adresse IP |",
        )

    def test_unauthenticated_view_rejecting_authentication(self):
        assert rate_limits_markdown(TokenRefreshView()) == _table(
            "| Sans authentification | 5 appels par minute | par adresse IP |",
            "| Authentification refusée | 10 appels par minute | par adresse IP |",
        )

    def test_omits_disabled_rate(self):
        rates = {**_RATES, "auth_rejection": None}

        with patch.object(SimpleRateThrottle, "THROTTLE_RATES", rates):
            markdown = rate_limits_markdown(OrganismesUpsertView())

        assert "Authentification refusée" not in markdown

    def test_rejects_undocumented_throttle(self):
        class View(UnauthenticatedMixin, APIView):
            throttle_classes = [ScopedRateThrottle]

        with pytest.raises(ValueError, match="ScopedRateThrottle"):
            rate_limits_markdown(View())

    def test_rejects_undocumented_authentication(self):
        class View(APIView):
            authentication_classes = [SessionAuthentication]

        with pytest.raises(ValueError, match="SessionAuthentication"):
            rate_limits_markdown(View())


def _public_schema():
    return yaml.safe_load(
        Path("presentation/static/api/schema.yaml").read_text(encoding="utf-8")
    )


_TOKEN_OR_DETAIL = {
    "anyOf": [
        {"$ref": "#/components/schemas/TokenError"},
        {"$ref": "#/components/schemas/DetailError"},
    ]
}
_DETAIL = {"$ref": "#/components/schemas/DetailError"}
_JWT = ["Error-InvalidJWT", "Error-JWTIPNotAllowed"]
_API_KEY = ["Error-InvalidAPIKey", "Error-APIKeyIPNotAllowed"]


@pytest.mark.parametrize(
    "method, path, schema, examples",
    [
        ("get", "/api/v1/organismes", _TOKEN_OR_DETAIL, _JWT),
        ("put", "/api/v1/organismes", _DETAIL, [*_API_KEY, "Error-JWTOnAPIKeyRoute"]),
        ("get", "/api/v1/offres", _TOKEN_OR_DETAIL, [*_JWT, *_API_KEY]),
    ],
)
def test_401_follows_authentication_modes(method, path, schema, examples):
    content = _public_schema()["paths"][path][method]["responses"]["401"]["content"]

    assert content["application/json"]["schema"] == schema
    assert list(content["application/json"]["examples"]) == examples


def test_unauthenticated_operation_has_no_401():
    assert "401" not in _public_schema()["paths"]["/api/guide.md"]["get"]["responses"]


def test_every_authenticated_public_operation_documents_its_401():
    undocumented = [
        f"{method.upper()} {path}"
        for path, operations in _public_schema()["paths"].items()
        for method, operation in operations.items()
        if any(operation.get("security", []))
        and not operation["responses"]
        .get("401", {})
        .get("content", {})
        .get("application/json", {})
        .get("examples")
    ]

    assert undocumented == []


def test_every_public_operation_documents_its_rate_limits():
    schema = _public_schema()

    undocumented = [
        f"{method.upper()} {path}"
        for path, operations in schema["paths"].items()
        for method, operation in operations.items()
        if "**Limites d'appels**" not in operation.get("description", "")
    ]

    assert undocumented == []
