from django.http import Http404
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import exceptions, status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from application.recruteur.services.read_conversation import (
    MessageStub,
    read_conversation,
)
from domain.commons.errors.organisme_errors import OrganismeNexistePas
from domain.identite.errors.organisme_permission_errors import (
    AccesOrganismeRefuse,
    AccesRecrutementInconnu,
    AccesRecrutementRefuse,
    OperationOrganismeRefusee,
)
from domain.recruteur.errors.recrutement_errors import (
    ConversationInexistante,
    RecrutementCandidatureInexistante,
    RecrutementInexistant,
)
from presentation.api.serializers import GenericErrorSerializer, generic_response_format
from presentation.commons.pagination import PageNumberLimitPagination
from presentation.recruteur.mappers import UtilisateurMapper
from presentation.recruteur.serializers import ConversationMessageSerializer


class MessagePagination(PageNumberLimitPagination):
    page_size = 20


@extend_schema_view(
    get=extend_schema(
        operation_id="recruteur_organismes_recrutements_candidatures_conversations_messages_list",
        summary="Messages d'une conversation d'une candidature (stub)",
        tags=["recruteur"],
        responses={
            **generic_response_format,
            200: ConversationMessageSerializer(many=True),
        },
    ),
)
class CandidatureConversationDetailView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ConversationMessageSerializer
    pagination_class = MessagePagination

    def get_queryset(self) -> list[MessageStub]:
        return read_conversation(
            organisme_id=self.kwargs["organisme_uuid"],
            recrutement_id=self.kwargs["recrutement_uuid"],
            candidature_id=self.kwargs["candidature_uuid"],
            conversation_id=self.kwargs["conversation_uuid"],
            utilisateur=UtilisateurMapper().to_domain(self.request),
        )

    def handle_exception(self, exc: Exception) -> Response:
        if isinstance(
            exc,
            (
                AccesOrganismeRefuse,
                AccesRecrutementRefuse,
                OperationOrganismeRefusee,
                OrganismeNexistePas,
                AccesRecrutementInconnu,
                RecrutementInexistant,
                RecrutementCandidatureInexistante,
                ConversationInexistante,
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
