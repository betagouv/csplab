from uuid import UUID

from django.http import Http404
from drf_spectacular.utils import extend_schema
from rest_framework import exceptions, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from application.recruteur.services.update_motif_refus import update_motif_refus
from domain.commons.errors.organisme_errors import OrganismeNexistePas
from domain.identite.errors.organisme_permission_errors import (
    AccesOrganismeRefuse,
    AccesRecrutementRefuse,
)
from domain.recruteur.errors.recrutement_errors import (
    CandidatureNonRefusee,
    RecrutementCandidatureInexistante,
    RecrutementInexistant,
)
from presentation.api.authentication import SessionApiMixin
from presentation.api.serializers import GenericErrorSerializer, generic_response_format
from presentation.recruteur.serializers import (
    MotifRefusSerializer,
    UpdateMotifRefusSerializer,
)


@extend_schema(
    summary="Modifier le motif de refus d'une candidature",
    tags=["recruteur"],
    request=UpdateMotifRefusSerializer,
    responses={
        **generic_response_format,
        200: MotifRefusSerializer,
        400: {
            "type": "object",
            "additionalProperties": {"type": "array", "items": {"type": "string"}},
        },
        409: GenericErrorSerializer,
    },
)
class CandidatureMotifRefusView(SessionApiMixin, APIView):
    def patch(
        self,
        request: Request,
        organisme_uuid: UUID,
        recrutement_uuid: UUID,
        candidature_uuid: UUID,
    ) -> Response:
        serializer = UpdateMotifRefusSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        candidature = update_motif_refus(
            organisme_id=organisme_uuid,
            recrutement_id=recrutement_uuid,
            candidature_id=candidature_uuid,
            motif_refus=serializer.validated_data["motif_refus"],
            utilisateur=request.user,
        )
        return Response(
            MotifRefusSerializer(
                {
                    "value": candidature.motif_refus,
                    "label": candidature.get_motif_refus_display(),
                }
            ).data
        )

    def handle_exception(self, exc: Exception) -> Response:
        if isinstance(
            exc,
            (
                AccesOrganismeRefuse,
                AccesRecrutementRefuse,
            ),
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
        if isinstance(exc, CandidatureNonRefusee):
            return Response(
                GenericErrorSerializer({"error": str(exc)}).data,
                status=status.HTTP_409_CONFLICT,
            )
        if isinstance(exc, (exceptions.APIException, Http404)):
            return super().handle_exception(exc)
        return Response(
            GenericErrorSerializer({"error": "Unexpected error"}).data,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
