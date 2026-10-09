from drf_spectacular.utils import (
    extend_schema,
)
from rest_framework import status
from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from application.ingestion.interfaces.list_metiers_input import GetFilteredMetiersInput
from infrastructure.di.ingestion.ingestion_factory import create_ingestion_container
from presentation.api.authentication import PublicApiMixin
from presentation.api.serializers import (
    ErreurApiSerializer,
    api_v1_response_format,
)
from presentation.commons.pagination import ApiV1Pagination
from presentation.ingestion.openapi import (
    LIST_METIERS_DESCRIPTION,
    LIST_METIERS_EXAMPLES,
)
from presentation.ingestion.serializers import (
    ListMetiersFiltersSerializer,
    ListMetiersResponseSerializer,
)


@extend_schema(
    summary="Liste des métiers",
    description=LIST_METIERS_DESCRIPTION,
    examples=LIST_METIERS_EXAMPLES,
    tags=["metiers"],
    parameters=[ListMetiersFiltersSerializer],
    responses={
        200: ListMetiersResponseSerializer(many=True),
        400: ErreurApiSerializer,
        **api_v1_response_format,
    },
)
class MetiersListView(PublicApiMixin, APIView):
    serializer_class = ListMetiersResponseSerializer
    pagination_class = ApiV1Pagination
    usecase = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.container = create_ingestion_container()
        self.logger = self.container.logger_service()
        if self.usecase is None:
            self.usecase = self.container.list_metiers_usecase()

    def get(self, request):
        try:
            filters = ListMetiersFiltersSerializer(data=self.request.query_params)
            filters.is_valid(raise_exception=True)
            input_data = GetFilteredMetiersInput(**filters.validated_data)

            result = self.usecase.execute(input_data)

            paginator = ApiV1Pagination()
            items = paginator.paginate(result, request)
            return paginator.get_paginated_response(
                ListMetiersResponseSerializer(items, many=True).data
            )
        except DRFValidationError as e:
            serializer = ErreurApiSerializer({"erreur": str(e)})
            return Response(
                serializer.data,
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            self.logger.error("Unexpected error in MetiersListView: %s", str(e))
            serializer = ErreurApiSerializer({"erreur": "Unexpected error"})
            return Response(
                serializer.data, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
