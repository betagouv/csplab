from uuid import UUID

from django.http import Http404
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import exceptions, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from application.recruteur.services.add_recrutement_agent_tag import (
    add_recrutement_agent_tag,
)
from application.recruteur.services.remove_recrutement_agent_tag import (
    remove_recrutement_agent_tag,
)
from domain.commons.errors.organisme_errors import OrganismeNexistePas
from domain.identite.errors.organisme_permission_errors import (
    AccesOrganismeRefuse,
    AccesRecrutementInconnu,
    AccesRecrutementRefuse,
    OperationOrganismeRefusee,
)
from domain.recruteur.errors.recrutement_agent_errors import AgentNonMembreRecrutement
from domain.recruteur.errors.recrutement_errors import RecrutementInexistant
from domain.recruteur.errors.tag_errors import (
    TagAlreadyOnMember,
    TagCategoryMismatch,
    TagNotFound,
    TagNotOnMember,
    TagOrganismeMismatch,
)
from presentation.api.authentication import SessionApiMixin
from presentation.api.serializers import GenericErrorSerializer, generic_response_format
from presentation.recruteur.serializers import AddTagSerializer


class RecrutementAgentTagBaseView(SessionApiMixin, APIView):
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
                AgentNonMembreRecrutement,
                TagNotFound,
                TagNotOnMember,
                TagOrganismeMismatch,
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
        if isinstance(exc, TagAlreadyOnMember):
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
        summary="Poser une étiquette sur un membre de l'équipe de recrutement",
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
class RecrutementAgentTagsView(RecrutementAgentTagBaseView):
    def post(
        self,
        request: Request,
        organisme_uuid: UUID,
        recrutement_uuid: UUID,
        agent_uuid: UUID,
    ) -> Response:
        serializer = AddTagSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        add_recrutement_agent_tag(
            organisme_id=organisme_uuid,
            recrutement_id=recrutement_uuid,
            agent_id=agent_uuid,
            tag_id=serializer.validated_data["tag_uuid"],
            utilisateur=request.user,
        )
        return Response(status=status.HTTP_201_CREATED)


@extend_schema_view(
    delete=extend_schema(
        summary="Retirer l'étiquette d'un membre de l'équipe de recrutement",
        tags=["recruteur"],
        responses={
            **generic_response_format,
            204: None,
        },
    ),
)
class RecrutementAgentTagDetailView(RecrutementAgentTagBaseView):
    def delete(
        self,
        request: Request,
        organisme_uuid: UUID,
        recrutement_uuid: UUID,
        agent_uuid: UUID,
        tag_uuid: UUID,
    ) -> Response:
        remove_recrutement_agent_tag(
            organisme_id=organisme_uuid,
            recrutement_id=recrutement_uuid,
            agent_id=agent_uuid,
            tag_id=tag_uuid,
            utilisateur=request.user,
        )
        return Response(status=status.HTTP_204_NO_CONTENT)
