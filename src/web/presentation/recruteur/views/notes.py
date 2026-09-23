from uuid import UUID

from django.http import Http404
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import exceptions, status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from application.recruteur.services.create_note import create_note
from application.recruteur.services.delete_note import delete_note
from application.recruteur.services.list_notes import list_notes
from application.recruteur.services.update_note import update_note
from domain.commons.errors.organisme_errors import OrganismeNexistePas
from domain.identite.errors.organisme_permission_errors import (
    AccesOrganismeRefuse,
    AccesRecrutementInconnu,
    AccesRecrutementRefuse,
    OperationOrganismeRefusee,
)
from domain.recruteur.errors.note_errors import NoteIntrouvable
from domain.recruteur.errors.recrutement_errors import (
    RecrutementCandidatureInexistante,
    RecrutementInexistant,
)
from presentation.api.serializers import GenericErrorSerializer, TokenErrorSerializer
from presentation.recruteur.mappers import UtilisateurMapper
from presentation.recruteur.serializers import (
    CreateNoteSerializer,
    NoteDetailSerializer,
    NoteSerializer,
    UpdateNoteSerializer,
)


class NoteBaseView(APIView):
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
                NoteIntrouvable,
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


@extend_schema_view(
    get=extend_schema(
        summary="Liste des notes d'une candidature",
        tags=["recruteur"],
        responses={
            200: NoteSerializer(many=True),
            401: TokenErrorSerializer,
            403: GenericErrorSerializer,
            404: GenericErrorSerializer,
            500: GenericErrorSerializer,
        },
    ),
    post=extend_schema(
        summary="Ajouter une note à une candidature",
        tags=["recruteur"],
        request=CreateNoteSerializer,
        responses={
            201: NoteDetailSerializer,
            400: GenericErrorSerializer,
            401: TokenErrorSerializer,
            403: GenericErrorSerializer,
            404: GenericErrorSerializer,
            500: GenericErrorSerializer,
        },
    ),
)
class CandidatureNotesView(NoteBaseView, ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NoteSerializer

    def get_queryset(self):
        return list_notes(
            organisme_id=self.kwargs["organisme_uuid"],
            recrutement_id=self.kwargs["recrutement_uuid"],
            candidature_id=self.kwargs["candidature_uuid"],
            utilisateur=UtilisateurMapper().to_domain(self.request),
        )

    def post(
        self,
        request: Request,
        organisme_uuid: UUID,
        recrutement_uuid: UUID,
        candidature_uuid: UUID,
    ) -> Response:
        serializer = CreateNoteSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        note = create_note(
            organisme_id=organisme_uuid,
            recrutement_id=recrutement_uuid,
            candidature_id=candidature_uuid,
            message=serializer.validated_data["message"],
            utilisateur=UtilisateurMapper().to_domain(request),
        )
        return Response(
            NoteDetailSerializer(note).data,
            status=status.HTTP_201_CREATED,
        )


@extend_schema_view(
    patch=extend_schema(
        summary="Modifier une note d'une candidature",
        tags=["recruteur"],
        request=UpdateNoteSerializer,
        responses={
            200: NoteDetailSerializer,
            400: GenericErrorSerializer,
            403: GenericErrorSerializer,
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
            403: GenericErrorSerializer,
            404: GenericErrorSerializer,
            500: GenericErrorSerializer,
        },
    ),
)
class CandidatureNoteDetailView(NoteBaseView):
    permission_classes = [IsAuthenticated]

    def patch(
        self,
        request: Request,
        organisme_uuid: UUID,
        recrutement_uuid: UUID,
        candidature_uuid: UUID,
        note_uuid: UUID,
    ) -> Response:
        serializer = UpdateNoteSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        note = update_note(
            organisme_id=organisme_uuid,
            recrutement_id=recrutement_uuid,
            candidature_id=candidature_uuid,
            note_id=note_uuid,
            message=serializer.validated_data["message"],
            utilisateur=UtilisateurMapper().to_domain(request),
        )
        return Response(NoteDetailSerializer(note).data)

    def delete(
        self,
        request: Request,
        organisme_uuid: UUID,
        recrutement_uuid: UUID,
        candidature_uuid: UUID,
        note_uuid: UUID,
    ) -> Response:
        delete_note(
            organisme_id=organisme_uuid,
            recrutement_id=recrutement_uuid,
            candidature_id=candidature_uuid,
            note_id=note_uuid,
            utilisateur=UtilisateurMapper().to_domain(request),
        )
        return Response(status=status.HTTP_204_NO_CONTENT)
