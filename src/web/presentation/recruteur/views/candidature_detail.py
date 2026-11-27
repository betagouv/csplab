from uuid import UUID

from django.http import Http404
from drf_spectacular.utils import extend_schema
from rest_framework import exceptions, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from application.recruteur.errors.application_errors_recruteur import (
    CandidatureInaccessible,
)
from application.recruteur.services.get_candidature import get_candidature
from presentation.api.authentication import SessionApiMixin
from presentation.api.serializers import GenericErrorSerializer, generic_response_format
from presentation.commons.conditional_get import ConditionalGetMixin
from presentation.recruteur.serializers import CandidatureDetailSerializer
from presentation.recruteur.views.candidature_inaccessible import (
    candidature_inaccessible_response,
)


@extend_schema(
    summary="Détail d'une candidature",
    tags=["recruteur"],
    responses={
        **generic_response_format,
        200: CandidatureDetailSerializer,
    },
)
class CandidatureDetailView(ConditionalGetMixin, SessionApiMixin, APIView):
    def get(
        self,
        request: Request,
        organisme_uuid: UUID,
        recrutement_uuid: UUID,
        candidature_uuid: UUID,
    ) -> Response:
        result = get_candidature(
            organisme_id=organisme_uuid,
            recrutement_id=recrutement_uuid,
            candidature_id=candidature_uuid,
            utilisateur=request.user,
        )
        return Response(CandidatureDetailSerializer(result).data)

    def handle_exception(self, exc: Exception) -> Response:
        if isinstance(exc, CandidatureInaccessible):
            return candidature_inaccessible_response()
        if isinstance(exc, (exceptions.APIException, Http404)):
            return super().handle_exception(exc)
        return Response(
            GenericErrorSerializer({"error": "Unexpected error"}).data,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
