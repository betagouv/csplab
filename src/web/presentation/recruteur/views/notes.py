from uuid import UUID

from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from application.recruteur.services.creer_note import creer_note
from application.recruteur.services.editer_note import editer_note
from application.recruteur.services.lister_notes_candidature import (
    lister_notes_candidature,
)
from application.recruteur.services.supprimer_note import supprimer_note
from domain.identite.errors.agent_errors import ProfilAgentNexistePas
from domain.recruteur.errors.note_errors import NoteIntrouvable
from domain.recruteur.errors.recrutement_errors import CandidatureInexistante
from presentation.api.serializers import GenericErrorSerializer, TokenErrorSerializer
from presentation.recruteur.serializers import (
    CreerNoteSerializer,
    EditerNoteSerializer,
    NoteDetailSerializer,
    NoteSerializer,
)


@extend_schema_view(
    get=extend_schema(
        summary="Liste des notes d'une candidature",
        tags=["recruteur"],
        responses={
            200: NoteSerializer(many=True),
            401: TokenErrorSerializer,
            500: GenericErrorSerializer,
        },
    ),
    post=extend_schema(
        summary="Ajouter une note à une candidature",
        tags=["recruteur"],
        request=CreerNoteSerializer,
        responses={
            201: NoteDetailSerializer,
            400: GenericErrorSerializer,
            401: TokenErrorSerializer,
            404: GenericErrorSerializer,
            500: GenericErrorSerializer,
        },
    ),
)
class CandidatureNotesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, candidature_uuid: UUID) -> Response:
        # TODO RBAC : l'utilisateur a t il le droit de consulter la liste
        # des notes de cette candidature
        try:
            notes = lister_notes_candidature(candidature_id=candidature_uuid)
            serializer = NoteSerializer(notes, many=True)
            return Response(serializer.data)
        except Exception:
            serializer = GenericErrorSerializer({"error": "Unexpected error"})
            return Response(
                serializer.data, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request: Request, candidature_uuid: UUID) -> Response:
        serializer = CreerNoteSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            note = creer_note(
                candidature_id=candidature_uuid,
                publie_par_id=request.user.username,
                message=serializer.validated_data["message"],
            )
            return Response(
                NoteDetailSerializer(note).data,
                status=status.HTTP_201_CREATED,
            )
        except CandidatureInexistante:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        except ProfilAgentNexistePas:
            return Response(
                {"detail": "Invalid author."}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception:
            serializer = GenericErrorSerializer({"error": "Unexpected error"})
            return Response(
                serializer.data, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@extend_schema_view(
    patch=extend_schema(
        summary="Modifier une note d'une candidature",
        tags=["recruteur"],
        request=EditerNoteSerializer,
        responses={
            200: NoteDetailSerializer,
            400: GenericErrorSerializer,
            404: GenericErrorSerializer,
            500: GenericErrorSerializer,
        },
    ),
    delete=extend_schema(
        summary="Supprimer une note d'une candidature",
        tags=["recruteur"],
        responses={
            204: None,
            401: TokenErrorSerializer,
            404: GenericErrorSerializer,
            500: GenericErrorSerializer,
        },
    ),
)
class CandidatureNoteDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(
        self, request: Request, candidature_uuid: UUID, note_uuid: UUID
    ) -> Response:
        serializer = EditerNoteSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            note = editer_note(
                note_id=note_uuid,
                message=serializer.validated_data["message"],
                utilisateur_id=request.user.username,
            )
            return Response(NoteDetailSerializer(note).data)
        except NoteIntrouvable:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            serializer = GenericErrorSerializer({"error": "Unexpected error"})
            return Response(
                serializer.data, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(
        self, request: Request, candidature_uuid: UUID, note_uuid: UUID
    ) -> Response:
        try:
            supprimer_note(
                note_id=note_uuid,
                utilisateur_id=request.user.username,
            )
            return Response(status=status.HTTP_204_NO_CONTENT)
        except NoteIntrouvable:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            error_serializer = GenericErrorSerializer({"error": "Unexpected error"})
            return Response(
                error_serializer.data, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
