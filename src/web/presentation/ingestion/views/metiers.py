import logging

from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers as drf_serializers
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from application.ingestion.services.list_metiers import list_metiers
from config.logger_names import LoggerName
from presentation.api.authentication import PublicApiMixin
from presentation.api.serializers import GenericErrorSerializer, TokenErrorSerializer
from presentation.commons.pagination import TaillePageNumberPagination
from presentation.ingestion.openapi import (
    LIST_METIERS_DESCRIPTION,
    LIST_METIERS_EXAMPLES,
)
from presentation.ingestion.serializers import (
    ListMetiersFiltersSerializer,
    ListMetiersResponseSerializer,
)

logger = logging.getLogger(LoggerName.INGESTION.value)


@extend_schema(
    summary="Liste des métiers",
    description=LIST_METIERS_DESCRIPTION,
    examples=LIST_METIERS_EXAMPLES,
    tags=["metiers"],
    parameters=[ListMetiersFiltersSerializer],
    responses={
        200: ListMetiersResponseSerializer(many=True),
        400: GenericErrorSerializer,
        401: TokenErrorSerializer,
        404: inline_serializer(
            name="ListMetiersNotFound",
            fields={"detail": drf_serializers.CharField()},
        ),
        500: GenericErrorSerializer,
    },
)
class MetiersListView(PublicApiMixin, APIView):
    serializer_class = ListMetiersResponseSerializer
    pagination_class = TaillePageNumberPagination

    def get(self, request):
        try:
            filters = ListMetiersFiltersSerializer(data=self.request.query_params)
            filters.is_valid(raise_exception=True)
            result = list_metiers(**filters.validated_data)

            paginator = TaillePageNumberPagination()
            items = paginator.paginate_queryset(result, request, view=self)
            return paginator.get_paginated_response(
                ListMetiersResponseSerializer(items, many=True).data
            )
        except DRFValidationError as e:
            serializer = GenericErrorSerializer({"error": str(e)})
            return Response(
                serializer.data,
                status=status.HTTP_400_BAD_REQUEST,
            )
        except NotFound:
            raise
        except Exception as e:
            logger.error("Unexpected error in MetiersListView: %s", str(e))
            serializer = GenericErrorSerializer({"error": "Unexpected error"})
            return Response(
                serializer.data, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
