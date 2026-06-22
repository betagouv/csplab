from uuid import UUID

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from application.recruteur.usecases.initialize_organisme_steps import (
    InitializeOrganismeStepsCommand,
)
from domain.recruteur.entities.organisme_recruteur import OrganismeRecruteur
from domain.recruteur.errors.erreur_recrutement import ErreurRecruteur
from infrastructure.di.recruteur.recruteur_factory import recruteur_container
from presentation.api.serializers import GenericErrorSerializer, TokenErrorSerializer
from presentation.recruteur.serializers import (
    EtapeRecrutementSerializer,
    OrganismeSerializer,
)


@extend_schema(
    summary="Detail d'un organisme",
    tags=["recruteur"],
    responses={
        200: OrganismeSerializer,
        401: TokenErrorSerializer,
        404: GenericErrorSerializer,
        500: GenericErrorSerializer,
    },
)
class OrganismeView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrganismeSerializer

    def get(self, request: Request, organisme_uuid: UUID) -> Response:
        try:
            # TODO: wire the recruteur DI container + use case + repository
            # (infrastructure/di/recruteur/ does not exist yet) to fetch the
            # organisme by organisme_uuid, e.g.:
            #   organisme = usecase.execute(organisme_uuid)
            #   return Response(OrganismeSerializer(organisme).data)
            # Static response for dev purposes until persistence is wired.
            serializer = OrganismeSerializer(
                {"nom": "COMMUNE DE BRIANCON", "siret": "21050023700354"}
            )
            return Response(serializer.data)
        except ErreurRecruteur:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            serializer = GenericErrorSerializer({"error": "Unexpected error"})
            return Response(
                serializer.data, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@extend_schema(
    summary="Liste des étapes de recrutement d'un organisme",
    tags=["recruteur"],
    responses={
        200: EtapeRecrutementSerializer(many=True),
        401: TokenErrorSerializer,
        404: GenericErrorSerializer,
        500: GenericErrorSerializer,
    },
)
class EtapesRecrutementOrganismeView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EtapeRecrutementSerializer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.container = recruteur_container()

    def get(self, request: Request, organisme_uuid: UUID) -> Response:
        try:
            usecase = self.container.initialize_organisme_steps_usecase()
            organisme: OrganismeRecruteur = usecase.execute(
                InitializeOrganismeStepsCommand(organisme_uuid)
            )
            etapes = organisme.etapes or ()
            data = [
                {
                    "etape_uuid": str(e.entity_id),
                    "nom": e.nom,
                    "categorie": e.categorie.name,
                }
                for e in etapes
            ]
            serializer = EtapeRecrutementSerializer(data, many=True)
            return Response(serializer.data)
        except ErreurRecruteur:
            return Response(
                {"organisme_uuid": "Not found."}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception:
            serializer = GenericErrorSerializer({"error": "Unexpected error"})
            return Response(
                serializer.data, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
