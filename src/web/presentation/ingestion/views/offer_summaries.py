from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from application.ingestion.interfaces.list_offers_input import GetFilteredOffersInput
from infrastructure.authentication.api_key_authentication import (
    ApiKeyAuthentication,
)
from infrastructure.di.ingestion.ingestion_factory import create_ingestion_container
from presentation.api.serializers import GenericErrorSerializer
from presentation.ingestion.mappers import OfferSummaryOutputMapper
from presentation.ingestion.serializers import OfferSummariesQuerySerializer


@extend_schema(exclude=True)
class OfferSummariesView(APIView):
    authentication_classes = [JWTAuthentication, ApiKeyAuthentication]

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
            start = query.validated_data["start"]
            count = query.validated_data["count"]

            page = self.usecase.execute(
                GetFilteredOffersInput(active=True, external_id_contains=None)
            )
            total = page.count()
            offers = list(page.slice(start, count))

            return Response(
                {
                    "data": [self.mapper.to_dict(offer) for offer in offers],
                    "_pagination": {
                        "start": start,
                        "count": len(offers),
                        "total": total,
                        "resultsPerPage": count,
                        "hasMore": start + len(offers) < total,
                    },
                }
            )
        except Exception as e:
            self.logger.error("Unexpected error in OfferSummariesView: %s", str(e))
            serializer = GenericErrorSerializer({"error": "Unexpected error"})
            return Response(
                serializer.data, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
