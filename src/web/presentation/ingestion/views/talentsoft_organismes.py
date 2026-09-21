import logging

from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers, status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from application.ingestion.usecases.upsert_talentsoft_organismes import (
    UpsertTalentsoftOrganismesUsecase,
)
from config.logger_names import LoggerName
from infrastructure.authentication.api_key_authentication import (
    ApiKeyAuthentication,
)
from presentation.api.serializers import GenericErrorSerializer
from presentation.ingestion.serializers import (
    TalentsoftOrganismeUpsertInputSerializer,
    UpsertTalentsoftOrganismesRequestSerializer,
)

logger = logging.getLogger(LoggerName.INGESTION.value)

UPSERT_TALENTSOFT_ORGANISMES_DESCRIPTION = (
    "Créer ou mettre à jour, entre 1 et 100 organismes Talentsoft à la fois, via un "
    "payload JSON. L'upsert se base sur le code de l'entité Talentsoft "
    "(`entity_code`)."
)


@extend_schema(
    summary="Ajouter/mettre à jour des organismes Talentsoft",
    description=UPSERT_TALENTSOFT_ORGANISMES_DESCRIPTION,
    tags=["talentsoft_organisme"],
    request=inline_serializer(
        name="UpsertTalentsoftOrganismesRequest",
        fields={
            "talentsoft_organismes": serializers.ListField(
                child=TalentsoftOrganismeUpsertInputSerializer(),
                min_length=1,
                max_length=100,
                help_text=(
                    "Liste d'organismes Talentsoft à créer ou mettre à jour "
                    "(min: 1, max: 100)"
                ),
            ),
        },
    ),
    responses={
        201: inline_serializer(
            name="UpsertTalentsoftOrganismesResponse",
            fields={
                "created": serializers.IntegerField(
                    help_text="Nombre d'organismes Talentsoft créés"
                ),
                "updated": serializers.IntegerField(
                    help_text="Nombre d'organismes Talentsoft mis à jour"
                ),
                "errors": serializers.ListField(
                    help_text=(
                        "Organismes Talentsoft rejetés avec le détail de l'erreur"
                    ),
                    child=serializers.DictField(),
                ),
            },
        ),
        400: GenericErrorSerializer,
        401: GenericErrorSerializer,
        500: GenericErrorSerializer,
    },
)
class TalentsoftOrganismesUpsertView(APIView):
    authentication_classes = [ApiKeyAuthentication]
    parser_classes = [JSONParser]
    serializer_class = UpsertTalentsoftOrganismesRequestSerializer

    def post(self, request):
        serializer = UpsertTalentsoftOrganismesRequestSerializer(data=request.data)
        if not serializer.is_valid():
            logger.warning(
                "TalentsoftOrganismesUpsertView: validation errors %s",
                serializer.errors,
            )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        valid_items = []
        errors = []

        for item_data in request.data["talentsoft_organismes"]:
            item_serializer = TalentsoftOrganismeUpsertInputSerializer(data=item_data)
            if not item_serializer.is_valid():
                errors.append(
                    {
                        "talentsoft_organisme": {
                            "entity_code": item_data.get("entity_code"),
                            "organisme_id": item_data.get("organisme_id"),
                        },
                        "error": item_serializer.errors,
                    }
                )
                continue
            valid_items.append(item_serializer.validated_data)

        try:
            usecase = UpsertTalentsoftOrganismesUsecase()
            result = usecase.execute(valid_items)
            result["errors"].extend(errors)
            return Response(result, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error("TalentsoftOrganismesUpsertView: unexpected error %s", str(e))
            return Response(
                {"error": "Unexpected error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
