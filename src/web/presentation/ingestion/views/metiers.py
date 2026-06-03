from drf_spectacular.utils import (
    extend_schema,
)
from rest_framework import status
from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from application.ingestion.interfaces.list_metiers_input import GetFilteredMetiersInput
from infrastructure.di.ingestion.ingestion_factory import create_ingestion_container
from presentation.ingestion.openapi import (
    LIST_METIERS_DESCRIPTION,
    LIST_METIERS_EXAMPLES,
)
from presentation.ingestion.pagination import IngestionPagination
from presentation.ingestion.serializers import (
    GenericErrorSerializer,
    ListMetiersFiltersSerializer,
    ListMetiersResponseSerializer,
    TokenErrorSerializer,
)


@extend_schema(
    summary="Liste des métiers",
    description=LIST_METIERS_DESCRIPTION,
    examples=LIST_METIERS_EXAMPLES,
    tags=["metiers"],
    parameters=[ListMetiersFiltersSerializer],
    responses={
        200: ListMetiersResponseSerializer,
        400: GenericErrorSerializer,
        401: TokenErrorSerializer,
        500: GenericErrorSerializer,
    },
)
class MetiersListView(APIView):
    serializer_class = ListMetiersResponseSerializer
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

            paginator = IngestionPagination()
            items = paginator.paginate(result, request)
            return paginator.get_paginated_response(
                ListMetiersResponseSerializer(items, many=True).data
            )
        except DRFValidationError as e:
            serializer = GenericErrorSerializer({"error": str(e)})
            return Response(
                serializer.data,
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            self.logger.error("Unexpected error in MetiersListView: %s", str(e))
            serializer = GenericErrorSerializer({"error": "Unexpected error"})
            return Response(
                serializer.data, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
