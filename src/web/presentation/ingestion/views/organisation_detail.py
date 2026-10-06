from django.http import Http404
from drf_spectacular.utils import extend_schema
from rest_framework import exceptions, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from application.ingestion.errors.application_errors_ingestion import (
    TalentsoftOrganismeInexistant,
)
from application.ingestion.services.talentsoft_organisme_detail import (
    get_talentsoft_organisme,
)
from presentation.api.authentication import PublicJwtOnlyMixin
from presentation.api.serializers import GenericErrorSerializer, generic_response_format
from presentation.ingestion.serializers import FakeTsTalentsoftOrganismeSerializer


@extend_schema(
    summary="Détail d'une organisation (format Talentsoft)",
    description="Simule l'API Talentsoft `organisation/{id}`, à partir de "
    "l'`entityCode` de l'organisation.",
    tags=["fake-ts"],
    responses={
        **generic_response_format,
        200: FakeTsTalentsoftOrganismeSerializer,
    },
)
class OrganisationDetailView(PublicJwtOnlyMixin, APIView):
    serializer_class = FakeTsTalentsoftOrganismeSerializer

    def get(self, request: Request, entity_code: str) -> Response:
        organisme = get_talentsoft_organisme(entity_code)
        return Response(self.serializer_class(organisme).data)

    def handle_exception(self, exc: Exception) -> Response:
        if isinstance(exc, TalentsoftOrganismeInexistant):
            return Response(
                GenericErrorSerializer({"error": str(exc)}).data,
                status=status.HTTP_404_NOT_FOUND,
            )
        if isinstance(exc, (exceptions.APIException, Http404)):
            return super().handle_exception(exc)
        return Response(
            GenericErrorSerializer({"error": "Unexpected error"}).data,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
