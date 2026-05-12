import logging

from django.views.generic import TemplateView
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    inline_serializer,
)
from huey.contrib.djhuey import HUEY
from rest_framework import serializers as drf_serializers
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from domain.exceptions.offer_errors import OfferDoesNotExist
from infrastructure.authentication.api_key_authentication import (
    ApiKeyAuthentication,
    UserRateThrottleExceptApiKey,
)
from infrastructure.di.ingestion.ingestion_factory import create_ingestion_container

logger = logging.getLogger(__name__)


class RedocView(TemplateView):
    template_name = "api/redoc.html"

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            title="ReDoc", schema_url="/static/api/schema.yaml", **kwargs
        )


class ArchiveOfferSuccessSerializer(drf_serializers.Serializer):
    status = drf_serializers.CharField()


@extend_schema_view(
    post=extend_schema(
        request=None,
        summary="Archiver une offre par référence",
        description=(
            "Archive une offre selon sa référence. "
            "Accepte une authentification JWT ou par clé d'API."
        ),
        tags=["offres"],
        responses={
            200: ArchiveOfferSuccessSerializer,
            401: inline_serializer(
                name="ArchiveOfferUnauthorized",
                fields={"detail": drf_serializers.CharField()},
            ),
            404: inline_serializer(
                name="ArchiveOfferNotFound",
                fields={"detail": drf_serializers.CharField()},
            ),
        },
    )
)
class ArchiveOffersView(APIView):
    authentication_classes = [JWTAuthentication, ApiKeyAuthentication]
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottleExceptApiKey]

    def get_serializer_class(self):
        return ArchiveOfferSuccessSerializer

    def post(self, request, reference: str):
        container = create_ingestion_container()
        offers_repository = container.offers_repository()
        try:
            offer = offers_repository.get_by_reference(reference)
        except OfferDoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        offers_repository.mark_as_archived([offer])
        return Response({"status": "ok"}, status=status.HTTP_200_OK)


@extend_schema(exclude=True)
class HueyHealthView(APIView):
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
