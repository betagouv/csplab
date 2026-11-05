import logging
from datetime import datetime, time
from functools import cache
from zoneinfo import ZoneInfo

import yaml
from django.conf import settings
from django.contrib.syndication.views import Feed
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.urls import reverse
from django.utils.feedgenerator import Atom1Feed
from django.views import View
from django.views.generic import TemplateView
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiExample, OpenApiParameter, extend_schema
from huey.contrib.djhuey import HUEY
from rest_framework import status
from rest_framework.negotiation import BaseContentNegotiation
from rest_framework.response import Response
from rest_framework.views import APIView

from config.logger_names import LoggerName
from infrastructure.authentication.rate_throttle import DocumentationRateThrottle
from presentation.api.authentication import PublicApiMixin, UnauthenticatedMixin
from presentation.api.changelog_api import (
    TYPE_LABELS,
    Filters,
    Fragment,
    assemble,
    changelog_markdown,
    entry_html,
    published_fragments,
    published_routes,
)
from presentation.api.serializers import ChangelogErrorSerializer, ChangelogSerializer

logger = logging.getLogger(LoggerName.WEB.value)


class RedocView(TemplateView):
    template_name = "api/redoc.html"

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            title="ReDoc", schema_url=reverse("api:public_schema"), **kwargs
        )


@cache
def _public_schema() -> dict:
    schema = yaml.safe_load((settings.STATIC_DIR / "api" / "schema.yaml").read_text())
    for tag in schema["tags"]:
        if tag["name"] == "changelog":
            tag["description"] = changelog_markdown()
    return schema


class PublicSchemaView(View):
    def get(self, request):
        return JsonResponse(_public_schema())


_MARKDOWN = "text/markdown; charset=utf-8"
_TEXT = "text/plain; charset=utf-8"

_FILTER_PARAMETERS = [
    OpenApiParameter(
        "type",
        str,
        enum=list(TYPE_LABELS),
        many=True,
        explode=True,
        description="Type de changement, répétable : `?type=ajoute&type=corrige`.",
    ),
    OpenApiParameter(
        "route",
        str,
        description=(
            "Route citée par le changement, avec sa méthode. Une route citée par "
            "aucun changement renvoie une erreur `400`."
        ),
        examples=[
            OpenApiExample(
                "Créer ou modifier des offres",
                value="POST /api/v1/offres/creer_modifier",
            )
        ],
    ),
    OpenApiParameter(
        "depuis",
        OpenApiTypes.DATE,
        description="Changements publiés à partir de cette date (AAAA-MM-JJ).",
    ),
]


class _IgnoreClientContentNegotiation(BaseContentNegotiation):
    def select_parser(self, request, parsers):
        return parsers[0]

    def select_renderer(self, request, renderers, format_suffix=None):
        return renderers[0], renderers[0].media_type


class _PublicDocumentationView(UnauthenticatedMixin, APIView):
    throttle_classes = [DocumentationRateThrottle]
    content_negotiation_class = _IgnoreClientContentNegotiation
    log_api_request = False


def _invalid_filters(filters: Filters) -> HttpResponse:
    return HttpResponse(
        "\n".join(filters.errors),
        status=status.HTTP_400_BAD_REQUEST,
        content_type=_TEXT,
    )


class ChangelogMarkdownView(_PublicDocumentationView):
    @extend_schema(
        tags=["documentation"],
        operation_id="changelog_markdown",
        summary="Changelog en Markdown",
        description=(
            "Le changelog de l'API en Markdown, du plus récent au plus ancien, "
            "avec des liens absolus. Une note rappelle les filtres actifs."
        ),
        parameters=_FILTER_PARAMETERS,
        responses={
            (200, "text/markdown"): OpenApiTypes.STR,
            (400, "text/plain"): OpenApiTypes.STR,
        },
    )
    def get(self, request):
        filters = Filters.from_query(request.GET, published_routes())
        if filters.errors:
            return _invalid_filters(filters)
        markdown = assemble(
            filters.apply(published_fragments()),
            base_url=request.build_absolute_uri("/").rstrip("/"),
            note=filters.describe(),
        )
        return HttpResponse(markdown, content_type=_MARKDOWN)


class ChangelogJsonView(_PublicDocumentationView):
    @extend_schema(
        tags=["documentation"],
        operation_id="changelog_json",
        summary="Changelog en JSON",
        description=(
            "Une entrée par changement, du plus récent au plus ancien, avec ses "
            "routes, sa PR et ses tickets."
        ),
        parameters=_FILTER_PARAMETERS,
        responses={200: ChangelogSerializer, 400: ChangelogErrorSerializer},
    )
    def get(self, request):
        filters = Filters.from_query(request.GET, published_routes())
        if filters.errors:
            return Response(
                ChangelogErrorSerializer({"erreurs": filters.errors}).data,
                status=status.HTTP_400_BAD_REQUEST,
            )
        fragments = filters.apply(published_fragments())
        serializer = ChangelogSerializer(
            {"nombre": len(fragments), "entrees": fragments},
            context={
                "page_url": request.build_absolute_uri(reverse("pages:api_changelog"))
            },
        )
        return Response(serializer.data)


ATOM_ID_PREFIX = "tag:csplab.beta.gouv.fr:changelog-api"


class ChangelogFeed(Feed):
    # Built per request, for absolute links from the request instead of Site.

    feed_type = Atom1Feed
    title = "Changelog de l'API CSPLab"
    subtitle = "Changements de l'API publique CSPLab qui concernent ses partenaires."

    def __init__(self, request: HttpRequest, filters: Filters):
        super().__init__()
        self.filters = filters
        self.page_url = request.build_absolute_uri(reverse("pages:api_changelog"))
        self.self_url = request.build_absolute_uri()

    def link(self) -> str:
        return self.page_url

    def feed_url(self) -> str:
        return self.self_url

    def items(self) -> list[Fragment]:
        return self.filters.apply(published_fragments())

    def item_title(self, fragment: Fragment) -> str:
        return f"{TYPE_LABELS[fragment.type]} : {', '.join(fragment.routes)}"

    def item_description(self, fragment: Fragment) -> str:
        return entry_html(fragment)

    def item_link(self, fragment: Fragment) -> str:
        return f"{self.page_url}#{fragment.slug}"

    def item_guid(self, fragment: Fragment) -> str:
        return f"{ATOM_ID_PREFIX}:{fragment.slug}"

    def item_pubdate(self, fragment: Fragment) -> datetime:
        return datetime.combine(fragment.date, time(), ZoneInfo("Europe/Paris"))

    def item_categories(self, fragment: Fragment) -> tuple[str, ...]:
        return (fragment.type, *fragment.routes)


class ChangelogAtomView(_PublicDocumentationView):
    @extend_schema(
        tags=["documentation"],
        operation_id="changelog_atom",
        summary="Changelog en flux Atom",
        description="Une entrée par changement, pour être prévenu des nouveaux.",
        parameters=_FILTER_PARAMETERS,
        responses={
            (200, "application/atom+xml"): OpenApiTypes.STR,
            (400, "text/plain"): OpenApiTypes.STR,
        },
    )
    def get(self, request):
        filters = Filters.from_query(request.GET, published_routes())
        if filters.errors:
            return _invalid_filters(filters)
        return ChangelogFeed(request._request, filters)(request._request)


@extend_schema(exclude=True)
class HueyHealthView(PublicApiMixin, APIView):
    def get(self, request):
        try:
            HUEY.storage.conn.ping()  # pings the Redis connection used by Huey
            return Response({"status": "ok"}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error("Huey health check failed: %s", str(e))
            return Response(
                {"status": "Huey health check failed"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
