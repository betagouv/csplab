from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers, status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from application.ingestion.interfaces.upsert_organismes_input import (
    UpsertOrganismesInput,
)
from infrastructure.authentication.api_key_authentication import (
    ApiKeyAuthentication,
)
from infrastructure.di.ingestion.ingestion_factory import create_ingestion_container
from presentation.api.serializers import GenericErrorSerializer
from presentation.ingestion.mappers import OrganismeInputMapper
from presentation.ingestion.serializers import (
    OrganismeUpsertInputSerializer,
    UpsertOrganismesRequestSerializer,
)

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
        201: inline_serializer(
            name="UpsertOrganismesResponse",
            fields={
                "created": serializers.IntegerField(
                    help_text="Nombre d'organismes créés"
                ),
                "updated": serializers.IntegerField(
                    help_text="Nombre d'organismes mis à jour"
                ),
                "errors": serializers.ListField(
                    help_text="Organismes rejetés avec le détail de l'erreur",
                    child=serializers.DictField(),
                ),
            },
        ),
        400: GenericErrorSerializer,
        401: GenericErrorSerializer,
        500: GenericErrorSerializer,
    },
)
class OrganismesUpsertView(APIView):
    authentication_classes = [ApiKeyAuthentication]
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
                        "error": item_serializer.errors,
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
                        "error": str(e),
                    }
                )

        try:
            usecase = container.upsert_organismes_usecase()
            result = usecase.execute(UpsertOrganismesInput(organismes=valid_organismes))
            result["errors"].extend(errors)
            return Response(result, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error("OrganismesUpsertView: unexpected error %s", str(e))
            return Response(
                {"error": "Unexpected error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
