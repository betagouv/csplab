import logging

from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers, status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from application.ingestion.interfaces.supprimer_organismes_input import (
    OrganismeDeleteData,
    SupprimerOrganismesInput,
)
from application.ingestion.interfaces.upsert_organismes_input import (
    UpsertOrganismesInput,
)
from application.ingestion.usecases.supprimer_organismes import (
    SupprimerOrganismesUsecase,
)
from config.logger_names import LoggerName
from infrastructure.di.ingestion.ingestion_factory import create_ingestion_container
from infrastructure.repositories.identite.postgres_organisme_repository import (
    PostgresOrganismeRepository,
)
from presentation.api.authentication import PublicApiKeyOnlyMixin
from presentation.api.serializers import (
    ErreurApiSerializer,
    api_v1_response_format,
)
from presentation.ingestion.mappers import OrganismeInputMapper
from presentation.ingestion.serializers import (
    OrganismeUpsertInputSerializer,
    SupprimerOrganismesRequestSerializer,
    SupprimerOrganismesResponseSerializer,
    UpsertOrganismesRequestSerializer,
    UpsertOrganismesResponseSerializer,
)

logger = logging.getLogger(LoggerName.INGESTION.value)

UPSERT_ORGANISMES_DESCRIPTION = (
    "Créer ou mettre à jour, entre 1 et 100 organismes à la fois, via un payload "
    "JSON. L'upsert se base sur le couple (référentiel, external_id)."
)


@extend_schema(
    summary="Ajouter/mettre à jour des organismes",
    description=UPSERT_ORGANISMES_DESCRIPTION,
    tags=["organismes"],
    request=inline_serializer(
        name="UpsertOrganismesRequest",
        fields={
            "organismes": serializers.ListField(
                child=OrganismeUpsertInputSerializer(),
                min_length=1,
                max_length=100,
                help_text="Liste d'organismes à créer ou mettre à jour (min: 1, max: 100)",  # noqa: E501
            ),
        },
    ),
    responses={
        201: UpsertOrganismesResponseSerializer,
        400: ErreurApiSerializer,
        **api_v1_response_format,
    },
)
class OrganismesUpsertView(PublicApiKeyOnlyMixin, APIView):
    parser_classes = [JSONParser]
    serializer_class = UpsertOrganismesRequestSerializer

    def post(self, request):
        container = create_ingestion_container()
        logger = container.logger_service()

        serializer = UpsertOrganismesRequestSerializer(data=request.data)
        if not serializer.is_valid():
            logger.warning(
                "OrganismesUpsertView: validation errors %s", serializer.errors
            )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        valid_organismes = []
        errors = []
        organisme_mapper = OrganismeInputMapper()

        for organisme_data in request.data["organismes"]:
            item_serializer = OrganismeUpsertInputSerializer(data=organisme_data)
            if not item_serializer.is_valid():
                errors.append(
                    {
                        "organisme": {
                            "referentiel": organisme_data.get("referentiel"),
                            "external_id": organisme_data.get("external_id"),
                        },
                        "erreur": item_serializer.errors,
                    }
                )
                continue
            try:
                valid_organismes.append(
                    organisme_mapper.to_domain(item_serializer.validated_data)
                )
            except Exception as e:
                errors.append(
                    {
                        "organisme": {
                            "referentiel": organisme_data.get("referentiel"),
                            "external_id": organisme_data.get("external_id"),
                        },
                        "erreur": str(e),
                    }
                )

        try:
            usecase = container.upsert_organismes_usecase()
            result = usecase.execute(UpsertOrganismesInput(organismes=valid_organismes))
            return Response(
                {
                    "created": result["created"],
                    "updated": result["updated"],
                    "erreurs": [*result["errors"], *errors],
                },
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            logger.error("OrganismesUpsertView: unexpected error %s", str(e))
            return Response(
                {"erreur": "Unexpected error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


SUPPRIMER_ORGANISMES_DESCRIPTION = (
    "Supprimer (soft-delete), entre 1 et 100 organismes à la fois, via un payload "
    "JSON. La suppression se base sur le couple (référentiel, external_id)."
)


@extend_schema(
    summary="Supprimer des organismes",
    description=SUPPRIMER_ORGANISMES_DESCRIPTION,
    tags=["organismes"],
    request=SupprimerOrganismesRequestSerializer,
    responses={
        200: SupprimerOrganismesResponseSerializer,
        400: ErreurApiSerializer,
        **api_v1_response_format,
    },
)
class OrganismesSupprimerView(PublicApiKeyOnlyMixin, APIView):
    parser_classes = [JSONParser]
    serializer_class = SupprimerOrganismesRequestSerializer

    def put(self, request):
        serializer = SupprimerOrganismesRequestSerializer(data=request.data)
        if not serializer.is_valid():
            logger.warning(
                "OrganismesSupprimerView: validation errors %s", serializer.errors
            )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        organismes = [
            OrganismeDeleteData(
                referentiel=organisme["referentiel"],
                external_id=organisme["external_id"],
            )
            for organisme in serializer.validated_data["organismes"]
        ]

        try:
            usecase = SupprimerOrganismesUsecase(
                organisme_repository=PostgresOrganismeRepository(),
            )
            result = usecase.execute(SupprimerOrganismesInput(organismes=organismes))
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error("OrganismesSupprimerView: unexpected error %s", str(e))
            return Response(
                {"erreur": "Unexpected error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
