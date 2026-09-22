import logging

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from application.ingestion.services.upsert_talentsoft_organismes import (
    upsert_talentsoft_organismes,
)
from config.logger_names import LoggerName
from infrastructure.authentication.api_key_authentication import (
    ApiKeyAuthentication,
)
from presentation.api.serializers import GenericErrorSerializer
from presentation.ingestion.serializers import (
    TalentsoftOrganismeUpsertInputSerializer,
    UpsertTalentsoftOrganismesRequestSerializer,
    UpsertTalentsoftOrganismesResponseSerializer,
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
    request=UpsertTalentsoftOrganismesRequestSerializer,
    responses={
        201: UpsertTalentsoftOrganismesResponseSerializer,
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
            result = upsert_talentsoft_organismes(valid_items)
            result["errors"].extend(errors)
            return Response(result, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error("TalentsoftOrganismesUpsertView: unexpected error %s", str(e))
            return Response(
                {"error": "Unexpected error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
