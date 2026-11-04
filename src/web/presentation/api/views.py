import logging
from datetime import datetime, time
from functools import cache
from zoneinfo import ZoneInfo

import yaml
from django.conf import settings
from django.contrib.syndication.views import Feed
from django.core.exceptions import BadRequest
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.urls import reverse
from django.utils.feedgenerator import Atom1Feed
from django.views import View
from django.views.generic import TemplateView
from drf_spectacular.utils import extend_schema
from huey.contrib.djhuey import HUEY
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from config.logger_names import LoggerName
from presentation.api.authentication import PublicApiMixin
from presentation.api.changelog_api import (
    TYPE_LABELS,
    Filters,
    Fragment,
    as_json,
    assemble,
    changelog_markdown,
    entry_html,
    published_fragments,
)

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


def _base_url(request: HttpRequest) -> str:
    return request.build_absolute_uri("/").rstrip("/")


class ChangelogMarkdownView(View):
    def get(self, request):
        filters = Filters.from_query(request.GET)
        if filters.errors:
            return HttpResponse(
                "\n".join(filters.errors),
                status=status.HTTP_400_BAD_REQUEST,
                content_type="text/plain; charset=utf-8",
            )
        markdown = assemble(
            filters.apply(published_fragments()),
            base_url=_base_url(request),
            note=filters.describe(),
        )
        return HttpResponse(markdown, content_type=_MARKDOWN)


class ChangelogJsonView(View):
    def get(self, request):
        filters = Filters.from_query(request.GET)
        if filters.errors:
            return JsonResponse(
                {"erreurs": list(filters.errors)},
                status=status.HTTP_400_BAD_REQUEST,
                json_dumps_params={"ensure_ascii": False},
            )
        page_url = request.build_absolute_uri(reverse("pages:api_changelog"))
        entries = [
            as_json(fragment, page_url)
            for fragment in filters.apply(published_fragments())
        ]
        return JsonResponse(
            {"nombre": len(entries), "entrees": entries},
            json_dumps_params={"ensure_ascii": False},
        )


class ChangelogFeed(Feed):
    """Built per request: absolute links come from the request, not from Site."""

    feed_type = Atom1Feed
    title = "Changelog de l'API CSPLab"
    subtitle = "Changements de l'API publique CSPLab qui concernent ses partenaires."

    def __init__(self, request: HttpRequest):
        super().__init__()
        self.page_url = request.build_absolute_uri(reverse("pages:api_changelog"))
        self.self_url = request.build_absolute_uri()

    @classmethod
    def view(cls, request: HttpRequest) -> HttpResponse:
        return cls(request)(request)

    def get_object(self, request, *args, **kwargs) -> Filters:
        filters = Filters.from_query(request.GET)
        if filters.errors:
            raise BadRequest(" ".join(filters.errors))
        return filters

    def link(self) -> str:
        return self.page_url

    def feed_url(self) -> str:
        return self.self_url

    def items(self, filters: Filters) -> list[Fragment]:
        return filters.apply(published_fragments())

    def item_title(self, fragment: Fragment) -> str:
        return f"{TYPE_LABELS[fragment.type]} : {', '.join(fragment.routes)}"

    def item_description(self, fragment: Fragment) -> str:
        return entry_html(fragment)

    def item_link(self, fragment: Fragment) -> str:
        return f"{self.page_url}#{fragment.slug}"

    def item_pubdate(self, fragment: Fragment) -> datetime:
        return datetime.combine(fragment.date, time(), ZoneInfo("Europe/Paris"))

    def item_categories(self, fragment: Fragment) -> tuple[str, ...]:
        return (fragment.type, *fragment.routes)


class GuideMarkdownView(View):
    def get(self, request):
        guide = (settings.STATIC_DIR / "api" / "guide_api.md").read_text()
        return HttpResponse(guide, content_type=_MARKDOWN)


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
