from uuid import UUID

from django.conf import settings
from django.http import FileResponse, Http404
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema
from rest_framework import exceptions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from application.recruteur.services.read_document import read_document
from domain.commons.errors.organisme_errors import OrganismeNexistePas
from domain.identite.errors.organisme_permission_errors import (
    AccesOrganismeRefuse,
    AccesRecrutementInconnu,
    AccesRecrutementRefuse,
    OperationOrganismeRefusee,
)
from domain.recruteur.errors.recrutement_errors import (
    RecrutementDocumentInexistant,
    RecrutementDocumentTypeNonAutorise,
    RecrutementInexistant,
)
from presentation.api.serializers import GenericErrorSerializer, generic_response_format
from presentation.recruteur.mappers import UtilisateurMapper


@extend_schema(
    summary="Télécharger un document de candidature",
    tags=["recruteur"],
    responses={
        **generic_response_format,
        **{
            (200, content_type): OpenApiTypes.BINARY
            for content_type in settings.ALLOWED_DOCUMENT_CONTENT_TYPES
        },
        415: GenericErrorSerializer,
    },
)
class DocumentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(
        self,
        request: Request,
        organisme_uuid: UUID,
        recrutement_uuid: UUID,
        candidature_uuid: UUID,
        document_uuid: UUID,
    ) -> FileResponse:
        document, content_type = read_document(
            organisme_id=organisme_uuid,
            recrutement_id=recrutement_uuid,
            candidature_id=candidature_uuid,
            document_id=document_uuid,
            utilisateur=UtilisateurMapper().to_domain(request),
        )
        return FileResponse(
            document.fichier.open("rb"),
            content_type=content_type,
            as_attachment=False,
            filename=document.nom_original,
        )

    def handle_exception(self, exc: Exception) -> Response:
        if isinstance(
            exc,
            (
                AccesOrganismeRefuse,
                AccesRecrutementRefuse,
                OperationOrganismeRefusee,
                OrganismeNexistePas,
                AccesRecrutementInconnu,
                RecrutementInexistant,
                RecrutementDocumentInexistant,
            ),
        ):
            return Response(
                GenericErrorSerializer({"error": str(exc)}).data,
                status=status.HTTP_404_NOT_FOUND,
            )
        if isinstance(exc, RecrutementDocumentTypeNonAutorise):
            return Response(
                GenericErrorSerializer({"error": str(exc)}).data,
                status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            )
        if isinstance(exc, (exceptions.APIException, Http404)):
            return super().handle_exception(exc)
        return Response(
            GenericErrorSerializer({"error": "Unexpected error"}).data,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
