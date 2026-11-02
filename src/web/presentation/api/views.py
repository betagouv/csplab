import logging
from functools import cache

import yaml
from django.conf import settings
from django.http import JsonResponse
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView
from drf_spectacular.utils import extend_schema
from huey.contrib.djhuey import HUEY
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from config.logger_names import LoggerName
from presentation.api.authentication import PublicApiMixin
from presentation.api.changelog_api import changelog_markdown

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
