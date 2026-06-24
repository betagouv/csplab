from uuid import UUID

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
from application.ingestion.interfaces.get_offers_by_source_input import (
    GetOffersBySourceInput,
)
from application.ingestion.interfaces.list_offers_input import GetFilteredOffersInput
from application.ingestion.interfaces.upsert_offers_input import UpsertOffersInput
from domain.ingestion.exceptions.source_authorization_error import (
    SourceAuthorizationError,
)
from infrastructure.authentication.api_key_authentication import (
    ApiKeyAuthentication,
    UserRateThrottleExceptApiKey,
)
from infrastructure.di.ingestion.ingestion_factory import create_ingestion_container
from infrastructure.django_apps.users.models import UserModel
from presentation.api.serializers import GenericErrorSerializer, TokenErrorSerializer
from presentation.commons.pagination import WebPagination
from presentation.ingestion.mappers import OfferInputMapper
from presentation.ingestion.openapi import (
    ARCHIVE_OFFER_DESCRIPTION,
    ARCHIVE_OFFER_EXAMPLES,
    LIST_OFFERS_DESCRIPTION,
    LIST_OFFERS_EXAMPLES,
    OFFERS_BY_SOURCE_DESCRIPTION,
    UPSERT_OFFERS_DESCRIPTION,
)
from presentation.ingestion.serializers import (
    ArchiveOfferRequestSerializer,
    ArchiveOfferSuccessSerializer,
    IdentityInputSerializer,
    ListOffersFiltersSerializer,
    ListOffersResponseSerializer,
    OfferDetailResponseSerializer,
    OffersInputSerializer,
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

            paginator = WebPagination()
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


@extend_schema(
    summary="Liste des offres d'une source",
    description=OFFERS_BY_SOURCE_DESCRIPTION,
    tags=["offres"],
    responses={
        200: inline_serializer(
            name="OffersBySourceResponse",
            fields={
                "count": drf_serializers.IntegerField(),
                "next": drf_serializers.CharField(allow_null=True),
                "previous": drf_serializers.CharField(allow_null=True),
                "results": OfferDetailResponseSerializer(many=True),
            },
        ),
        401: PolymorphicProxySerializer(
            component_name="OffersBySource401Error",
            serializers=[
                TokenErrorSerializer,
                inline_serializer(
                    name="OffersBySourceUnauthorized",
                    fields={"detail": drf_serializers.CharField()},
                ),
            ],
            resource_type_field_name=None,
        ),
        500: GenericErrorSerializer,
    },
)
class OffersBySourceView(APIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = OfferDetailResponseSerializer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.container = create_ingestion_container()
        self.logger = self.container.logger_service()

    def get(self, request, source_id):
        utilisateur_entity_id = UUID(request.user.username)
        try:
            usecase = self.container.get_offers_by_source_usecase()
            result = usecase.execute(
                GetOffersBySourceInput(
                    source_id=source_id,
                    utilisateur_entity_id=utilisateur_entity_id,
                )
            )
            paginator = WebPagination()
            items = paginator.paginate(result, request)
            return paginator.get_paginated_response(
                OfferDetailResponseSerializer(items, many=True).data
            )
        except SourceAuthorizationError as e:
            source_ids = sorted(str(sid) for sid in e.source_ids)
            return Response(
                {"detail": f"Not authorized to access this source: {source_ids}."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        except Exception as e:
            self.logger.error("Unexpected error in OffersBySourceView: %s", str(e))
            return Response(
                {"error": "Unexpected error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
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
            403: inline_serializer(
                name="ArchiveOfferForbidden",
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
    throttle_classes = [UserRateThrottleExceptApiKey]

    serializer_class = ArchiveOfferSuccessSerializer

    def post(self, request):
        serializer = ArchiveOfferRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        utilisateur_entity_id = (
            UUID(request.user.username) if isinstance(request.user, UserModel) else None
        )
        container = create_ingestion_container()
        use_case = container.archive_offer_by_reference_usecase()
        try:
            use_case.execute(
                ArchiveOfferByReferenceInput(
                    reference=serializer.validated_data["reference"],
                    source_id=serializer.validated_data["source_id"],
                    utilisateur_entity_id=utilisateur_entity_id,
                )
            )
        except SourceAuthorizationError as e:
            source_ids = sorted(str(sid) for sid in e.source_ids)
            return Response(
                {"detail": f"Cannot edit this source: {source_ids}."},
                status=status.HTTP_403_FORBIDDEN,
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
            "source_id": serializers.UUIDField(
                help_text="Identifiant de la source des offres"
            ),
            "offres": serializers.ListField(
                child=OffersInputSerializer(),
                min_length=1,
                max_length=100,
                help_text="Liste d'offres à créer ou mettre à jour (min: 1, max: 100)",
            ),
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
        403: inline_serializer(
            name="UpsertOffersForbidden",
            fields={"detail": drf_serializers.CharField()},
        ),
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

        source_id = serializer.validated_data["source_id"]

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
                valid_offers.append(
                    offer_mapper.to_domain(serializer.validated_data, source_id)
                )
            except Exception as e:
                errors.append(
                    {
                        "offer": offer_data.get("identification", {}),
                        "error": str(e),
                    }
                )

        utilisateur_entity_id = (
            UUID(request.user.username) if isinstance(request.user, UserModel) else None
        )
        try:
            usecase = container.upsert_offers_usecase()
            result = usecase.execute(
                UpsertOffersInput(
                    source_id=source_id,
                    offers=valid_offers,
                    utilisateur_entity_id=utilisateur_entity_id,
                )
            )
            result["errors"].extend(errors)
            return Response(result, status=status.HTTP_201_CREATED)
        except SourceAuthorizationError as e:
            source_ids = sorted(str(sid) for sid in e.source_ids)
            return Response(
                {"detail": f"Cannot edit offers with this source: {source_ids}."},
                status=status.HTTP_403_FORBIDDEN,
            )
        except Exception as e:
            logger.error("OffersUpsertView: unexpected error %s", str(e))
            return Response(
                {"error": "Unexpected error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
