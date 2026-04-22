import logging

from django.urls import reverse_lazy
from django.views.generic import TemplateView
from drf_spectacular.utils import extend_schema
from huey.contrib.djhuey import HUEY
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

logger = logging.getLogger(__name__)


class RedocView(TemplateView):
    template_name = "api/redoc.html"

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            title="ReDoc", schema_url=reverse_lazy("api:schema"), **kwargs
        )


@extend_schema(exclude=True)
class HueyHealthView(APIView):
    def get(self, request):
        try:
            HUEY.storage.conn.ping()  # pings the Redis connection used by Huey
            return Response({"status": "ok"}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Huey health check failed: {str(e)}")
            return Response(
                {"status": "Huey health check failed"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
