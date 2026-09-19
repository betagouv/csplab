from uuid import UUID

from django.http import FileResponse, Http404
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema
from rest_framework import exceptions, status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from application.recruteur.services.list_documents import list_documents
from application.recruteur.services.read_document import read_document
from domain.commons.errors.organisme_errors import OrganismeNexistePas
from domain.identite.errors.organisme_permission_errors import (
    AccesOrganismeRefuse,
    AccesRecrutementRefuse,
    OperationOrganismeRefusee,
)
from domain.recruteur.errors.recrutement_errors import (
    RecrutementCandidatureInexistante,
    RecrutementDocumentInexistant,
    RecrutementInexistant,
)
from presentation.api.serializers import GenericErrorSerializer, generic_response_format
from presentation.commons.pagination import PageNumberLimitPagination
from presentation.recruteur.mappers import UtilisateurMapper
from presentation.recruteur.serializers import DocumentListeSerializer


@extend_schema(
    summary="Télécharger un document de candidature",
    tags=["recruteur"],
    responses={**generic_response_format, 200: OpenApiTypes.BINARY},
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
        document = read_document(
            organisme_id=organisme_uuid,
            recrutement_id=recrutement_uuid,
            candidature_id=candidature_uuid,
            document_id=document_uuid,
            utilisateur=UtilisateurMapper().to_domain(request),
        )
        return FileResponse(
            document.fichier.open("rb"),
            content_type=document.content_type,
            as_attachment=True,
            filename=document.nom_original,
        )

    def handle_exception(self, exc: Exception) -> Response:
        if isinstance(
            exc,
            (AccesOrganismeRefuse, AccesRecrutementRefuse, OperationOrganismeRefusee),
        ):
            return Response(
                GenericErrorSerializer({"error": str(exc)}).data,
                status=status.HTTP_403_FORBIDDEN,
            )
        if isinstance(
            exc,
            (OrganismeNexistePas, RecrutementInexistant, RecrutementDocumentInexistant),
        ):
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


@extend_schema(
    summary="Lister les documents d'une candidature",
    tags=["recruteur"],
    responses={**generic_response_format, 200: DocumentListeSerializer(many=True)},
)
class CandidatureDocumentsView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DocumentListeSerializer
    pagination_class = PageNumberLimitPagination

    def get_queryset(self):
        return list_documents(
            organisme_id=self.kwargs["organisme_uuid"],
            recrutement_id=self.kwargs["recrutement_uuid"],
            candidature_id=self.kwargs["candidature_uuid"],
            utilisateur=UtilisateurMapper().to_domain(self.request),
        )

    def handle_exception(self, exc: Exception) -> Response:
        if isinstance(
            exc,
            (AccesOrganismeRefuse, AccesRecrutementRefuse, OperationOrganismeRefusee),
        ):
            return Response(
                GenericErrorSerializer({"error": str(exc)}).data,
                status=status.HTTP_403_FORBIDDEN,
            )
        if isinstance(
            exc,
            (
                OrganismeNexistePas,
                RecrutementInexistant,
                RecrutementCandidatureInexistante,
            ),
        ):
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
