from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from application.ingestion.interfaces.list_offers_input import GetFilteredOffersInput
from infrastructure.di.ingestion.ingestion_factory import create_ingestion_container
from presentation.api.serializers import GenericErrorSerializer
from presentation.commons.pagination import TalentsoftPagination
from presentation.ingestion.mappers import OfferSummaryOutputMapper
from presentation.ingestion.serializers import OfferSummariesQuerySerializer


@extend_schema(exclude=True)
class OfferSummariesView(APIView):
    authentication_classes = [JWTAuthentication]
    pagination_class = TalentsoftPagination

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.container = create_ingestion_container()
        self.logger = self.container.logger_service()
        self.usecase = self.container.list_offers_usecase()
        self.mapper = OfferSummaryOutputMapper()

    def get(self, request):
        try:
            query = OfferSummariesQuerySerializer(data=request.query_params)
            query.is_valid(raise_exception=True)

            page = self.usecase.execute(
                GetFilteredOffersInput(active=True, external_id_contains=None)
            )

            paginator = TalentsoftPagination()
            offers = paginator.paginate(page, request)

            return paginator.get_paginated_response(
                [self.mapper.to_dict(offer) for offer in offers]
            )
        except Exception as e:
            self.logger.error("Unexpected error in OfferSummariesView: %s", str(e))
            serializer = GenericErrorSerializer({"error": "Unexpected error"})
            return Response(
                serializer.data, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
