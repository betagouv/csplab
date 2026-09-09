from uuid import UUID

from django.http import Http404
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import exceptions, status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from application.recruteur.services.list_recrutement_agents import (
    list_recrutement_agents,
)
from domain.commons.errors.organisme_errors import OrganismeNexistePas
from domain.identite.errors.organisme_permission_errors import (
    AccesOrganismeRefuse,
    OperationOrganismeRefusee,
)
from domain.recruteur.errors.recrutement_errors import RecrutementInexistant
from presentation.api.serializers import GenericErrorSerializer, generic_response_format
from presentation.recruteur.mappers import UtilisateurMapper
from presentation.recruteur.serializers import (
    RecrutementAgentRoleSerializer,
    RecrutementAgentSerializer,
)


@extend_schema_view(
    get=extend_schema(
        summary="Liste des agents ayant un rôle sur un recrutement",
        tags=["recruteur"],
        responses={
            **generic_response_format,
            200: RecrutementAgentSerializer(many=True),
        },
    ),
    post=extend_schema(
        summary="Ajouter un membre à l'équipe de recrutement",
        tags=["recruteur"],
        request=RecrutementAgentRoleSerializer,
        responses={
            **generic_response_format,
            201: RecrutementAgentSerializer,
            400: GenericErrorSerializer,
        },
    ),
    put=extend_schema(
        summary="Modifier le rôle d'un agent dans l'équipe de recrutement",
        tags=["recruteur"],
        request=RecrutementAgentRoleSerializer,
        responses={
            **generic_response_format,
            200: RecrutementAgentRoleSerializer,
            400: GenericErrorSerializer,
        },
    ),
)
class RecrutementAgentsView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RecrutementAgentSerializer

    def get_queryset(self):
        return list_recrutement_agents(
            organisme_id=self.kwargs["organisme_uuid"],
            recrutement_id=self.kwargs["recrutement_uuid"],
            utilisateur=UtilisateurMapper().to_domain(self.request),
        )

    def post(
        self, request: Request, organisme_uuid: UUID, recrutement_uuid: UUID
    ) -> Response:
        serializer = RecrutementAgentRoleSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                GenericErrorSerializer({"error": str(serializer.errors)}).data,
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {
                "agent_id": serializer.validated_data["agent_id"],
                "nom": "Nom",
                "prenom": "Prenom",
                "poste": "Poste",
                "email": "prenom.nom@test.com",
                "recrutement_role": serializer.validated_data["recrutement_role"],
            },
            status=status.HTTP_201_CREATED,
        )

    def put(
        self, request: Request, organisme_uuid: UUID, recrutement_uuid: UUID
    ) -> Response:
        serializer = RecrutementAgentRoleSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                GenericErrorSerializer({"error": str(serializer.errors)}).data,
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            RecrutementAgentRoleSerializer(serializer.validated_data).data,
            status=status.HTTP_200_OK,
        )

    def handle_exception(self, exc: Exception) -> Response:
        if isinstance(exc, (AccesOrganismeRefuse, OperationOrganismeRefusee)):
            return Response(
                GenericErrorSerializer({"error": str(exc)}).data,
                status=status.HTTP_403_FORBIDDEN,
            )
        if isinstance(exc, (OrganismeNexistePas, RecrutementInexistant)):
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
