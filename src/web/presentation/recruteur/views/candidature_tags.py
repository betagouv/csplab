from uuid import UUID

from django.http import Http404
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import exceptions, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from application.recruteur.services.add_candidature_tag import add_candidature_tag
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
from domain.recruteur.errors.tag_errors import (
    TagAlreadyOnCandidature,
    TagCategoryMismatch,
    TagNotFound,
)
from presentation.api.authentication import SessionApiMixin
from presentation.api.serializers import GenericErrorSerializer, generic_response_format
from presentation.recruteur.serializers import AddNoteTagSerializer


class CandidatureTagBaseView(SessionApiMixin, APIView):
    def handle_exception(self, exc: Exception) -> Response:
        if isinstance(
            exc,
            (
                AccesOrganismeRefuse,
                OperationOrganismeRefusee,
                AccesRecrutementRefuse,
                AccesRecrutementInconnu,
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
                TagNotFound,
            ),
        ):
            return Response(
                GenericErrorSerializer({"error": str(exc)}).data,
                status=status.HTTP_404_NOT_FOUND,
            )
        if isinstance(exc, TagCategoryMismatch):
            return Response(
                {"tag_uuid": [str(exc)]}, status=status.HTTP_400_BAD_REQUEST
            )
        if isinstance(exc, TagAlreadyOnCandidature):
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


@extend_schema_view(
    post=extend_schema(
        summary="Poser une étiquette sur une candidature",
        tags=["recruteur"],
        request=AddNoteTagSerializer,
        responses={
            **generic_response_format,
            201: None,
            400: {
                "type": "object",
                "additionalProperties": {"type": "array", "items": {"type": "string"}},
            },
            409: GenericErrorSerializer,
        },
    ),
)
class CandidatureTagsView(CandidatureTagBaseView):
    def post(
        self,
        request: Request,
        organisme_uuid: UUID,
        recrutement_uuid: UUID,
        candidature_uuid: UUID,
    ) -> Response:
        serializer = AddNoteTagSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        add_candidature_tag(
            organisme_id=organisme_uuid,
            recrutement_id=recrutement_uuid,
            candidature_id=candidature_uuid,
            tag_id=serializer.validated_data["tag_uuid"],
            utilisateur=request.user,
        )
        return Response(status=status.HTTP_201_CREATED)
