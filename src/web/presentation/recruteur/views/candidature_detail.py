from uuid import UUID

from django.http import Http404
from drf_spectacular.utils import extend_schema
from rest_framework import exceptions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from application.recruteur.services.candidature_detail import get_candidature_detail
from domain.commons.errors.organisme_errors import OrganismeNexistePas
from domain.identite.errors.organisme_permission_errors import (
    AccesOrganismeRefuse,
    AccesRecrutementInconnu,
    AccesRecrutementRefuse,
    OperationOrganismeRefusee,
)
from domain.recruteur.errors.recrutement_errors import (
    RecrutementCandidatureInexistante,
    RecrutementInexistant,
)
from presentation.api.serializers import GenericErrorSerializer, generic_response_format
from presentation.recruteur.mappers import UtilisateurMapper
from presentation.recruteur.serializers import CandidatureDetailSerializer


@extend_schema(
    summary="Détail d'une candidature",
    tags=["recruteur"],
    responses={
        **generic_response_format,
        200: CandidatureDetailSerializer,
    },
)
class CandidatureDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(
        self,
        request: Request,
        organisme_uuid: UUID,
        recrutement_uuid: UUID,
        candidature_uuid: UUID,
    ) -> Response:
        result = get_candidature_detail(
            organisme_id=organisme_uuid,
            recrutement_id=recrutement_uuid,
            candidature_id=candidature_uuid,
            utilisateur=UtilisateurMapper().to_domain(request),
        )
        return Response(CandidatureDetailSerializer(result).data)

    def handle_exception(self, exc: Exception) -> Response:
        if isinstance(
            exc,
            (
                AccesOrganismeRefuse,
                OperationOrganismeRefusee,
                AccesRecrutementRefuse,
                AccesRecrutementInconnu,
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
