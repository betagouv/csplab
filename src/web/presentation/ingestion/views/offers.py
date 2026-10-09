from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    inline_serializer,
)
from referentiel.exceptions.offer_errors import OfferDoesNotExist
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from application.ingestion.interfaces.archive_offer_by_reference_input import (
    ArchiveOfferByReferenceInput,
)
from application.ingestion.interfaces.get_offers_by_source_input import (
    GetOffersBySourceInput,
)
from application.ingestion.interfaces.list_offers_input import GetFilteredOffersInput
from application.ingestion.interfaces.upsert_offers_input import UpsertOffersInput
from application.ingestion.services.offer_references import (
    unknown_generated_references,
)
from domain.ingestion.exceptions.source_authorization_error import (
    SourceAuthorizationError,
)
from infrastructure.di.ingestion.ingestion_factory import create_ingestion_container
from infrastructure.django_apps.users.models import UserModel
from presentation.api.authentication import PublicApiMixin
from presentation.api.serializers import (
    ErreurApiSerializer,
    ErreurAuthentificationSerializer,
    api_v1_response_format,
)
from presentation.commons.pagination import ApiV1Pagination
from presentation.ingestion.mappers import OfferInputMapper
from presentation.ingestion.openapi import (
    ARCHIVE_OFFER_DESCRIPTION,
    ARCHIVE_OFFER_EXAMPLES,
    LIST_OFFERS_DESCRIPTION,
    LIST_OFFERS_EXAMPLES,
    OFFERS_BY_SOURCE_DESCRIPTION,
    UPSERT_OFFERS_DESCRIPTION,
    UPSERT_OFFERS_EXAMPLES,
)
from presentation.ingestion.serializers import (
    ArchiveOfferRequestSerializer,
    ArchiveOfferSuccessSerializer,
    ListOffersFiltersSerializer,
    ListOffersResponseSerializer,
    OfferDetailResponseSerializer,
    OffersInputSerializer,
    UpsertOffersRequestSerializer,
    UpsertOffersResponseSerializer,
)

UNKNOWN_GENERATED_REFERENCE = (
    "Aucune offre de cette source ne porte cette référence. Les références au "
    "format CSP-AAAA-NNNNNN sont générées par CSPLab : utilisez `auto` pour créer "
    "une offre."
)

STATUTS_OFFRE = {"created": "creee", "updated": "mise_a_jour"}


@extend_schema(
    summary="Liste des offres",
    description=LIST_OFFERS_DESCRIPTION,
    examples=LIST_OFFERS_EXAMPLES,
    tags=["offres"],
    parameters=[ListOffersFiltersSerializer],
    responses={
        200: ListOffersResponseSerializer(many=True),
        400: ErreurApiSerializer,
        **api_v1_response_format,
    },
)
class OffersListView(PublicApiMixin, APIView):
    serializer_class = ListOffersResponseSerializer
    pagination_class = ApiV1Pagination
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

            paginator = ApiV1Pagination()
            items = paginator.paginate(result, request)
            return paginator.get_paginated_response(
                ListOffersResponseSerializer(items, many=True).data
            )
        except DRFValidationError as e:
            serializer = ErreurApiSerializer({"erreur": str(e)})
            return Response(
                serializer.data,
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            self.logger.error("Unexpected error in OffersListView: %s", str(e))
            serializer = ErreurApiSerializer({"erreur": "Unexpected error"})
            return Response(
                serializer.data, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@extend_schema(
    summary="Liste des offres d'une source",
    description=OFFERS_BY_SOURCE_DESCRIPTION,
    tags=["offres"],
    responses={
        200: OfferDetailResponseSerializer(many=True),
        **api_v1_response_format,
    },
)
class OffersBySourceView(PublicApiMixin, APIView):
    serializer_class = OfferDetailResponseSerializer
    pagination_class = ApiV1Pagination

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.container = create_ingestion_container()
        self.logger = self.container.logger_service()

    def get(self, request, source_id):
        utilisateur_username = (
            request.user.username if isinstance(request.user, UserModel) else None
        )
        try:
            usecase = self.container.get_offers_by_source_usecase()
            result = usecase.execute(
                GetOffersBySourceInput(
                    source_id=source_id,
                    utilisateur_username=utilisateur_username,
                )
            )
            paginator = ApiV1Pagination()
            items = paginator.paginate(result, request)
            return paginator.get_paginated_response(
                OfferDetailResponseSerializer(items, many=True).data
            )
        except SourceAuthorizationError as e:
            source_ids = sorted(str(sid) for sid in e.source_ids)
            return Response(
                {"erreur": f"Not authorized to access this source: {source_ids}."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        except Exception as e:
            self.logger.error("Unexpected error in OffersBySourceView: %s", str(e))
            return Response(
                {"erreur": "Unexpected error"},
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
            400: ErreurApiSerializer,
            401: ErreurAuthentificationSerializer,
            403: ErreurApiSerializer,
            404: ErreurApiSerializer,
        },
    )
)
class ArchiveOffersView(PublicApiMixin, APIView):
    serializer_class = ArchiveOfferSuccessSerializer

    def post(self, request):
        serializer = ArchiveOfferRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        utilisateur_username = (
            request.user.username if isinstance(request.user, UserModel) else None
        )
        container = create_ingestion_container()
        use_case = container.archive_offer_by_reference_usecase()
        try:
            use_case.execute(
                ArchiveOfferByReferenceInput(
                    reference=serializer.validated_data["reference"],
                    source_id=serializer.validated_data["source_id"],
                    utilisateur_username=utilisateur_username,
                )
            )
        except SourceAuthorizationError as e:
            source_ids = sorted(str(sid) for sid in e.source_ids)
            return Response(
                {"erreur": f"Cannot edit this source: {source_ids}."},
                status=status.HTTP_403_FORBIDDEN,
            )
        except OfferDoesNotExist:
            return Response({"erreur": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response({"statut": "ok"}, status=status.HTTP_200_OK)


@extend_schema(
    summary="Ajouter/mettre à jour une offre d'emploi",
    description=UPSERT_OFFERS_DESCRIPTION,
    examples=UPSERT_OFFERS_EXAMPLES,
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
        201: UpsertOffersResponseSerializer,
        400: ErreurApiSerializer,
        403: ErreurApiSerializer,
        **api_v1_response_format,
    },
)
class OffersUpsertView(PublicApiMixin, APIView):
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
        valid_indexes = []
        errors = []
        offer_mapper = OfferInputMapper()

        for index, offer_data in enumerate(request.data["offres"]):
            serializer = OffersInputSerializer(
                data=offer_data,
                context={"metiers_repository": container.metiers_repository()},
            )
            if not serializer.is_valid():
                errors.append(
                    {
                        "index": index,
                        "offre": offer_data.get("identification", {}),
                        "erreur": serializer.errors,
                    }
                )
                continue
            try:
                valid_offers.append(
                    offer_mapper.to_domain(serializer.validated_data, source_id)
                )
                valid_indexes.append(index)
            except Exception as e:
                errors.append(
                    {
                        "index": index,
                        "offre": offer_data.get("identification", {}),
                        "erreur": str(e),
                    }
                )

        unknown = unknown_generated_references(
            source_id, [offer.reference for offer in valid_offers]
        )
        if unknown:
            kept = []
            for index, offer in zip(valid_indexes, valid_offers, strict=True):
                if offer.reference in unknown:
                    errors.append(
                        {
                            "index": index,
                            "offre": request.data["offres"][index]["identification"],
                            "erreur": {"reference": [UNKNOWN_GENERATED_REFERENCE]},
                        }
                    )
                else:
                    kept.append((index, offer))
            valid_indexes = [index for index, _ in kept]
            valid_offers = [offer for _, offer in kept]

        utilisateur_username = (
            request.user.username if isinstance(request.user, UserModel) else None
        )
        try:
            usecase = container.upsert_offers_usecase()
            result = usecase.execute(
                UpsertOffersInput(
                    source_id=source_id,
                    offers=valid_offers,
                    utilisateur_username=utilisateur_username,
                )
            )
            erreurs = sorted(errors, key=lambda erreur: erreur["index"])
            offres = [
                {
                    "index": index,
                    "reference": offer_status["reference"],
                    "statut": STATUTS_OFFRE[offer_status["statut"]],
                }
                for index, offer_status in zip(
                    valid_indexes, result["offres"], strict=True
                )
            ]
            return Response(
                {
                    "creees": result["created"],
                    "mises_a_jour": result["updated"],
                    "offres": offres,
                    "erreurs": [*result["errors"], *erreurs],
                },
                status=status.HTTP_201_CREATED,
            )
        except SourceAuthorizationError as e:
            source_ids = sorted(str(sid) for sid in e.source_ids)
            return Response(
                {"erreur": f"Cannot edit offers with this source: {source_ids}."},
                status=status.HTTP_403_FORBIDDEN,
            )
        except Exception as e:
            logger.error("OffersUpsertView: unexpected error %s", str(e))
            return Response(
                {"erreur": "Unexpected error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
