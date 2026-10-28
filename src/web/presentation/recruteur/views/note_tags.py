from uuid import UUID

from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from application.recruteur.services.add_note_tag import add_note_tag
from application.recruteur.services.remove_note_tag import remove_note_tag
from domain.recruteur.errors.tag_errors import (
    TagAlreadyOnNote,
    TagCategoryMismatch,
    TagNotFound,
)
from presentation.api.serializers import GenericErrorSerializer, generic_response_format
from presentation.recruteur.serializers import AddNoteTagSerializer
from presentation.recruteur.views.notes import NoteBaseView


class NoteTagBaseView(NoteBaseView):
    def handle_exception(self, exc: Exception) -> Response:
        if isinstance(exc, TagCategoryMismatch):
            return Response(
                {"tag_uuid": [str(exc)]}, status=status.HTTP_400_BAD_REQUEST
            )
        if isinstance(exc, TagNotFound):
            return Response(
                GenericErrorSerializer({"error": str(exc)}).data,
                status=status.HTTP_404_NOT_FOUND,
            )
        if isinstance(exc, TagAlreadyOnNote):
            return Response(
                GenericErrorSerializer({"error": str(exc)}).data,
                status=status.HTTP_409_CONFLICT,
            )
        return super().handle_exception(exc)


@extend_schema_view(
    post=extend_schema(
        summary="Poser une étiquette sur une note d'une candidature",
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
class CandidatureNoteTagsView(NoteTagBaseView):
    def post(
        self,
        request: Request,
        organisme_uuid: UUID,
        recrutement_uuid: UUID,
        candidature_uuid: UUID,
        note_uuid: UUID,
    ) -> Response:
        serializer = AddNoteTagSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        add_note_tag(
            organisme_id=organisme_uuid,
            recrutement_id=recrutement_uuid,
            candidature_id=candidature_uuid,
            note_id=note_uuid,
            tag_id=serializer.validated_data["tag_uuid"],
            utilisateur=request.user,
        )
        return Response(status=status.HTTP_201_CREATED)


@extend_schema_view(
    delete=extend_schema(
        summary="Retirer une étiquette d'une note d'une candidature",
        tags=["recruteur"],
        responses={
            **generic_response_format,
            204: None,
        },
    ),
)
class CandidatureNoteTagDetailView(NoteTagBaseView):
    def delete(
        self,
        request: Request,
        organisme_uuid: UUID,
        recrutement_uuid: UUID,
        candidature_uuid: UUID,
        note_uuid: UUID,
        tag_uuid: UUID,
    ) -> Response:
        remove_note_tag(
            organisme_id=organisme_uuid,
            recrutement_id=recrutement_uuid,
            candidature_id=candidature_uuid,
            note_id=note_uuid,
            tag_id=tag_uuid,
            utilisateur=request.user,
        )
        return Response(status=status.HTTP_204_NO_CONTENT)
