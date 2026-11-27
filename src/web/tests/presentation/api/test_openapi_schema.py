from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import pytest
import yaml
from rest_framework.authentication import SessionAuthentication
from rest_framework.throttling import ScopedRateThrottle, SimpleRateThrottle
from rest_framework.views import APIView

from presentation.api import openapi_examples
from presentation.api.authentication import UnauthenticatedMixin
from presentation.api.openapi_schema import (
    Caller,
    format_rate,
    rate_limits_markdown,
    unauthorized_doc,
)
from presentation.api.serializers import DetailErrorSerializer, TokenErrorSerializer
from presentation.api.token_views import TokenRefreshView
from presentation.api.views import ChangelogJsonView
from presentation.ingestion.views.offers import OffersListView
from presentation.ingestion.views.organisation_detail import OrganisationDetailView
from presentation.ingestion.views.organismes import OrganismesUpsertView, OrganismesView

_JWT_EXAMPLES = (openapi_examples.INVALID_JWT, openapi_examples.JWT_IP_NOT_ALLOWED)
_API_KEY_EXAMPLES = (
    openapi_examples.INVALID_API_KEY,
    openapi_examples.API_KEY_IP_NOT_ALLOWED,
)

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


def _view_for(view_class, method):
    view = view_class()
    view.request = SimpleNamespace(method=method)
    return view


class TestUnauthorizedDoc:
    def test_jwt_only_view(self):
        doc = unauthorized_doc(OrganisationDetailView())

        assert doc.serializers == (TokenErrorSerializer, DetailErrorSerializer)
        assert doc.examples == _JWT_EXAMPLES

    def test_api_key_only_view_adds_jwt_example(self):
        doc = unauthorized_doc(OrganismesUpsertView())

        assert doc.serializers == (DetailErrorSerializer,)
        assert doc.examples == (
            *_API_KEY_EXAMPLES,
            openapi_examples.JWT_ON_API_KEY_ROUTE,
        )

    def test_jwt_and_api_key_view(self):
        doc = unauthorized_doc(OffersListView())

        assert doc.serializers == (TokenErrorSerializer, DetailErrorSerializer)
        assert doc.examples == (*_JWT_EXAMPLES, *_API_KEY_EXAMPLES)

    def test_unauthenticated_view(self):
        assert unauthorized_doc(ChangelogJsonView()) is None

    @pytest.mark.parametrize(
        "method, serializers",
        [
            ("GET", (TokenErrorSerializer, DetailErrorSerializer)),
            ("PUT", (DetailErrorSerializer,)),
        ],
    )
    def test_follows_authenticators_of_the_method(self, method, serializers):
        doc = unauthorized_doc(_view_for(OrganismesView, method))

        assert doc.serializers == serializers

    def test_rejects_caller_without_example(self):
        with patch(
            "presentation.api.openapi_schema._UNAUTHORIZED_DOCS",
            {Caller.JWT: unauthorized_doc(OrganisationDetailView())},
        ):
            with pytest.raises(ValueError, match="API_KEY"):
                unauthorized_doc(OffersListView())


def _public_schema():
    return yaml.safe_load(
        Path("presentation/static/api/schema.yaml").read_text(encoding="utf-8")
    )


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
