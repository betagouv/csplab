from uuid import UUID

from django.http import Http404
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import exceptions, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from application.recruteur.errors.application_errors_recruteur import (
    CandidatureInaccessible,
)
from application.recruteur.services.add_candidature_tag import add_candidature_tag
from application.recruteur.services.remove_candidature_tag import (
    remove_candidature_tag,
)
from domain.recruteur.errors.tag_errors import (
    TagAlreadyOnCandidature,
    TagCategoryMismatch,
    TagNotFound,
    TagNotOnCandidature,
    TagOrganismeMismatch,
)
from presentation.api.authentication import SessionApiMixin
from presentation.api.serializers import GenericErrorSerializer, generic_response_format
from presentation.recruteur.serializers import AddTagSerializer
from presentation.recruteur.views.candidature_inaccessible import (
    candidature_inaccessible_response,
)


class CandidatureTagBaseView(SessionApiMixin, APIView):
    def handle_exception(self, exc: Exception) -> Response:
        if isinstance(exc, CandidatureInaccessible):
            return candidature_inaccessible_response()
        if isinstance(
            exc,
            (TagNotFound, TagNotOnCandidature, TagOrganismeMismatch),
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
        request=AddTagSerializer,
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
        serializer = AddTagSerializer(data=request.data)
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


@extend_schema_view(
    delete=extend_schema(
        summary="Retirer une étiquette d'une candidature",
        tags=["recruteur"],
        responses={
            **generic_response_format,
            204: None,
        },
    ),
)
class CandidatureTagDetailView(CandidatureTagBaseView):
    def delete(
        self,
        request: Request,
        organisme_uuid: UUID,
        recrutement_uuid: UUID,
        candidature_uuid: UUID,
        tag_uuid: UUID,
    ) -> Response:
        remove_candidature_tag(
            organisme_id=organisme_uuid,
            recrutement_id=recrutement_uuid,
            candidature_id=candidature_uuid,
            tag_id=tag_uuid,
            utilisateur=request.user,
        )
        return Response(status=status.HTTP_204_NO_CONTENT)
