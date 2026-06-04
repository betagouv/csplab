from drf_spectacular.utils import (
    PolymorphicProxySerializer,
    extend_schema,
    extend_schema_view,
    inline_serializer,
)
from referentiel.exceptions.offer_errors import OfferDoesNotExist
from rest_framework import serializers, status
from rest_framework import serializers as drf_serializers
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from application.ingestion.interfaces.archive_offer_by_reference_input import (
    ArchiveOfferByReferenceInput,
)
from application.ingestion.interfaces.list_offers_input import GetFilteredOffersInput
from application.ingestion.interfaces.upsert_offers_input import UpsertOffersInput
from infrastructure.authentication.api_key_authentication import (
    ApiKeyAuthentication,
    UserRateThrottleExceptApiKey,
)
from infrastructure.di.ingestion.ingestion_factory import create_ingestion_container
from presentation.ingestion.mappers import OfferInputMapper
from presentation.ingestion.openapi import (
    ARCHIVE_OFFER_DESCRIPTION,
    ARCHIVE_OFFER_EXAMPLES,
    LIST_OFFERS_DESCRIPTION,
    LIST_OFFERS_EXAMPLES,
    UPSERT_OFFERS_DESCRIPTION,
)
from presentation.ingestion.pagination import IngestionPagination
from presentation.ingestion.serializers import (
    ArchiveOfferRequestSerializer,
    ArchiveOfferSuccessSerializer,
    GenericErrorSerializer,
    IdentityInputSerializer,
    ListOffersFiltersSerializer,
    ListOffersResponseSerializer,
    OffersInputSerializer,
    TokenErrorSerializer,
    UpsertOffersRequestSerializer,
)


@extend_schema(
    summary="Liste des offres",
    description=LIST_OFFERS_DESCRIPTION,
    examples=LIST_OFFERS_EXAMPLES,
    tags=["offres"],
    responses={
        200: ListOffersResponseSerializer,
        400: GenericErrorSerializer,
        401: TokenErrorSerializer,
        500: GenericErrorSerializer,
    },
)
class OffersListView(APIView):
    serializer_class = ListOffersResponseSerializer
    usecase = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.container = create_ingestion_container()
        self.logger = self.container.logger_service()
        if self.usecase is None:
            self.usecase = self.container.list_offers_usecase()

    def get(self, request):
        try:
            filters = ListOffersFiltersSerializer(data=self.request.query_params)
            filters.is_valid(raise_exception=True)
            input_data = GetFilteredOffersInput(**filters.validated_data)

            result = self.usecase.execute(input_data)

            paginator = IngestionPagination()
            items = paginator.paginate(result, request)
            return paginator.get_paginated_response(
                ListOffersResponseSerializer(items, many=True).data
            )
        except Exception as e:
            self.logger.error("Unexpected error in OffersListView: %s", str(e))
            serializer = GenericErrorSerializer({"error": "Unexpected error"})
            return Response(
                serializer.data, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@extend_schema_view(
    post=extend_schema(
        request={"application/json": ArchiveOfferRequestSerializer},
        summary="Archiver une offre par référence",
        description=ARCHIVE_OFFER_DESCRIPTION,
        examples=ARCHIVE_OFFER_EXAMPLES,
        tags=["offres"],
        responses={
            200: ArchiveOfferSuccessSerializer,
            400: inline_serializer(
                name="ArchiveOfferBadRequest",
                fields={"detail": drf_serializers.CharField()},
            ),
            401: PolymorphicProxySerializer(
                component_name="ArchiveOffer401Error",
                serializers=[
                    TokenErrorSerializer,
                    inline_serializer(
                        name="ArchiveOfferUnauthorized",
                        fields={"detail": drf_serializers.CharField()},
                    ),
                ],
                resource_type_field_name=None,
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
    throttle_classes = [UserRateThrottleExceptApiKey]

    serializer_class = ArchiveOfferSuccessSerializer

    def post(self, request):
        serializer = ArchiveOfferRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        container = create_ingestion_container()
        use_case = container.archive_offer_by_reference_usecase()
        try:
            use_case.execute(
                ArchiveOfferByReferenceInput(
                    reference=serializer.validated_data["reference"],
                    source_id=serializer.validated_data["source_id"],
                )
            )
        except OfferDoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response({"status": "ok"}, status=status.HTTP_200_OK)


@extend_schema(
    summary="Ajouter/mettre à jour une offre d'emploi",
    description=UPSERT_OFFERS_DESCRIPTION,
    tags=["offres"],
    request=inline_serializer(
        name="UpsertOffersRequest",
        fields={
            "offres": serializers.ListField(
                child=OffersInputSerializer(),
                min_length=1,
                max_length=100,
                help_text="Liste d'offres à créer ou mettre à jour (min: 1, max: 100)",
            )
        },
    ),
    responses={
        201: inline_serializer(
            name="UpsertOffersResponse",
            fields={
                "created": serializers.IntegerField(help_text="Nombre d'offres créées"),
                "updated": serializers.IntegerField(
                    help_text="Nombre d'offres mises à jour"
                ),
                "errors": serializers.ListField(
                    help_text="Offres rejetées avec le détail de l'erreur",
                    child=inline_serializer(
                        name="UpsertOfferError",
                        fields={
                            "offer": IdentityInputSerializer(
                                help_text="Identification de l'offre rejetée"
                            ),
                            "error": serializers.DictField(
                                help_text="Détail de l'erreur de validation"
                            ),
                        },
                    ),
                ),
            },
        ),
        400: GenericErrorSerializer,
        401: TokenErrorSerializer,
        500: GenericErrorSerializer,
    },
)
class OffersUpsertView(APIView):
    authentication_classes = [JWTAuthentication, ApiKeyAuthentication]
    parser_classes = [JSONParser]
    serializer_class = UpsertOffersRequestSerializer

    def post(self, request):
        container = create_ingestion_container()
        logger = container.logger_service()

        # catch mini / maxi items number
        serializer = UpsertOffersRequestSerializer(data=request.data)
        if not serializer.is_valid():
            logger.warning("OffersUpsertView: validation errors %s", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # iterate over offers, to handle only valid ones
        valid_offers = []
        errors = []
        offer_mapper = OfferInputMapper()

        for _, offer_data in enumerate(request.data["offres"]):
            serializer = OffersInputSerializer(data=offer_data)
            if not serializer.is_valid():
                errors.append(
                    {
                        "offer": offer_data.get("identification", {}),
                        "error": serializer.errors,
                    }
                )
                continue
            try:
                valid_offers.append(offer_mapper.to_domain(serializer.validated_data))
            except Exception as e:
                errors.append(
                    {
                        "offer": offer_data.get("identification", {}),
                        "error": str(e),
                    }
                )

        try:
            usecase = container.upsert_offers_usecase()
            result = usecase.execute(UpsertOffersInput(offers=valid_offers))
            result["errors"].extend(errors)
            return Response(result, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error("OffersUpsertView: unexpected error %s", str(e))
            return Response(
                {"error": "Unexpected error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
