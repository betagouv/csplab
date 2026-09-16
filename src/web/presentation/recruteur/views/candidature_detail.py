from uuid import UUID

from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from application.recruteur.services.candidature_detail import (
    get_candidature_detail_stub,
)
from presentation.api.serializers import generic_response_format
from presentation.recruteur.serializers import CandidatureDetailSerializer


@extend_schema(
    summary="Détail d'une candidature (stub)",
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
        result = get_candidature_detail_stub(
            organisme_id=organisme_uuid,
            recrutement_id=recrutement_uuid,
            candidature_id=candidature_uuid,
        )
        return Response(CandidatureDetailSerializer(result).data)
