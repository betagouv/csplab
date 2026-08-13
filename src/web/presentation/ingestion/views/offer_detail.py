from drf_spectacular.utils import extend_schema
from referentiel.exceptions.offer_errors import OfferDoesNotExist
from rest_framework import status
from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from application.ingestion.interfaces.get_offer_by_reference_input import (
    GetOfferByReferenceInput,
)
from infrastructure.di.ingestion.ingestion_factory import create_ingestion_container
from presentation.api.serializers import GenericErrorSerializer
from presentation.ingestion.mappers import OfferDetailOutputMapper
from presentation.ingestion.serializers import OfferDetailQuerySerializer


@extend_schema(exclude=True)
class OfferDetailView(APIView):
    authentication_classes = [JWTAuthentication]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.container = create_ingestion_container()
        self.logger = self.container.logger_service()
        self.usecase = self.container.get_offer_by_reference_usecase()
        self.mapper = OfferDetailOutputMapper()

    def get(self, request):
        try:
            query = OfferDetailQuerySerializer(data=request.query_params)
            query.is_valid(raise_exception=True)

            offer = self.usecase.execute(
                GetOfferByReferenceInput(
                    reference=query.validated_data["reference"],
                )
            )

            return Response(self.mapper.to_dict(offer))
        except DRFValidationError as e:
            serializer = GenericErrorSerializer({"error": str(e)})
            return Response(
                serializer.data,
                status=status.HTTP_400_BAD_REQUEST,
            )
        except OfferDoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            self.logger.error("Unexpected error in OfferDetailView: %s", str(e))
            serializer = GenericErrorSerializer({"error": "Unexpected error"})
            return Response(
                serializer.data, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
