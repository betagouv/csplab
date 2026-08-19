from datetime import datetime, timezone

from drf_spectacular.utils import extend_schema, extend_schema_view
from referentiel.value_objects.verse import Verse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from application.identite.usecases.create_organisme import CreateOrganismeCommand
from domain.identite.errors.organisme_errors import (
    OrganismeSiretExisteDeja,
    SiretInvalide,
)
from domain.identite.errors.organisme_permission_errors import (
    ConsultationOrganismesRefusee,
    CreationOrganismeRefusee,
)
from domain.identite.value_objects.siret import SIRET
from infrastructure.di.identite.identite_factory import create_identite_container
from infrastructure.factories.identite.organisme_factory import OrganismeFactory
from infrastructure.factories.seed_recruteur_datas import _ORGANISME_UUID
from presentation.api.serializers import GenericErrorSerializer, TokenErrorSerializer
from presentation.recruteur.serializers import (
    CreerOrganismeSerializer,
    OrganismeDetailSerializer,
)

_FROZEN_TS = datetime.now(tz=timezone.utc)


def fake_organismes() -> list[dict]:
    return [
        {
            "nom": org.nom,
            "siret": org.siret.value,
            "gestion_ats": True,
            "gestionnaire": None,
            "date_derniere_activite": "2026-01-15T10:00:00Z",
            "date_creation": "2026-01-01T09:00:00Z",
        }
        for org in OrganismeFactory.create_entity_batch()
    ]


@extend_schema_view(
    get=extend_schema(
        summary="Lister oganismes",
        tags=["recruteur"],
        responses={
            200: OrganismeDetailSerializer(many=True),
            401: TokenErrorSerializer,
            403: GenericErrorSerializer,
            404: GenericErrorSerializer,
            500: GenericErrorSerializer,
        },
    ),
    post=extend_schema(
        summary="Créer un organisme",
        tags=["recruteur"],
        request=CreerOrganismeSerializer,
        responses={
            200: OrganismeDetailSerializer,
            400: GenericErrorSerializer,
            401: TokenErrorSerializer,
            403: GenericErrorSerializer,
            404: GenericErrorSerializer,
            500: GenericErrorSerializer,
        },
    ),
)
class OrganismesView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrganismeDetailSerializer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.container = create_identite_container()

    def get(self, request: Request) -> Response:
        try:
            usecase = self.container.list_organismes_usecase()
            organismes = usecase.execute(
                request.user.username
            ) or OrganismeFactory.create_entity_batch(
                3,
            )
            organismes_dto = [
                {
                    "organisme_uuid": organisme.entity_id,
                    "nom": organisme.nom,
                    "siret": organisme.siret.value,
                    "gestion_ats": organisme.gestion_ats,
                    "date_creation": organisme.date_creation,
                    "date_derniere_activite": organisme.date_derniere_activite,
                }
                for organisme in organismes
            ]
            return Response(OrganismeDetailSerializer(organismes_dto, many=True).data)
        except ConsultationOrganismesRefusee as e:
            serializer = GenericErrorSerializer({"error": str(e)})
            return Response(serializer.data, status=status.HTTP_403_FORBIDDEN)
        except Exception:
            serializer = GenericErrorSerializer({"error": "Unexpected error"})
            return Response(
                serializer.data, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request: Request) -> Response:
        serializer = CreerOrganismeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            usecase = self.container.create_organisme_usecase()
            command = CreateOrganismeCommand(
                nom=serializer.validated_data["nom"],
                versant=Verse(serializer.validated_data["versant"]),
                localisation=None,
                siret=SIRET(serializer.validated_data["siret"]),
                parent_id=None,
                est_staff=request.user.is_staff,
            )
            usecase.execute(command)
            organisme = OrganismeFactory.create_entity(
                entity_id=_ORGANISME_UUID,
                date_creation=_FROZEN_TS,
                date_derniere_activite=_FROZEN_TS,
            )
            organisme_dto = {
                **serializer.validated_data,
                "organisme_uuid": organisme.entity_id,
                "date_creation": organisme.date_creation,
                "date_derniere_activite": organisme.date_derniere_activite,
            }
            return Response(
                OrganismeDetailSerializer(organisme_dto).data,
                status=status.HTTP_201_CREATED,
            )
        except (OrganismeSiretExisteDeja, SiretInvalide) as e:
            serializer = GenericErrorSerializer({"error": str(e)})
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
        except CreationOrganismeRefusee as e:
            serializer = GenericErrorSerializer({"error": str(e)})
            return Response(serializer.data, status=status.HTTP_403_FORBIDDEN)
        except Exception:
            serializer = GenericErrorSerializer({"error": "Unexpected error"})
            return Response(
                serializer.data, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
