from datetime import datetime, timezone

from drf_spectacular.utils import extend_schema, extend_schema_view
from pydantic import ValidationError
from referentiel.value_objects.siret import SIRET
from referentiel.value_objects.verse import Verse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from application.identite.usecases.create_organisme import CreateOrganismeCommand
from application.identite.usecases.list_organismes import ListOrganismesCommand
from domain.identite.errors.organisme_errors import OrganismeSiretExisteDeja
from domain.identite.errors.organisme_permission_errors import (
    OperationOrganismeRefusee,
)
from infrastructure.di.identite.identite_factory import create_identite_container
from infrastructure.factories.identite.organisme_factory import OrganismeFactory
from infrastructure.factories.seed_recruteur_datas import _ORGANISME_UUID
from presentation.api.serializers import (
    GenericErrorSerializer,
    generic_response_format,
)
from presentation.recruteur.mappers import UtilisateurMapper
from presentation.recruteur.serializers import (
    CreateOrganismeSerializer,
    OrganismeDetailSerializer,
    OrganismesListSerializer,
)

_FROZEN_TS = datetime.now(tz=timezone.utc)


@extend_schema_view(
    get=extend_schema(
        summary="Lister les organismes",
        tags=["recruteur"],
        responses={
            **generic_response_format,
            200: OrganismesListSerializer(many=True),
        },
    ),
    post=extend_schema(
        summary="Créer un organisme",
        tags=["recruteur"],
        request=CreateOrganismeSerializer,
        responses={
            **generic_response_format,
            200: OrganismeDetailSerializer,
            400: GenericErrorSerializer,
        },
    ),
)
class OrganismesView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrganismeDetailSerializer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.container = create_identite_container()
        self.user_mapper = UtilisateurMapper()

    def get(self, request: Request) -> Response:
        try:
            usecase = self.container.list_organismes_usecase()
            organismes = usecase.execute(
                ListOrganismesCommand(
                    utilisateur=self.user_mapper.to_domain(request),
                )
            ) or OrganismeFactory.create_entity_batch(
                3,
            )
            organismes_dto = [
                {
                    "organisme_uuid": organisme.entity_id,
                    "nom": organisme.nom,
                    "versant": organisme.versant.value,
                    "siret": organisme.siret.code,
                    "gestion_ats": organisme.gestion_ats,
                    "date_creation": organisme.date_creation,
                    "date_derniere_activite": organisme.date_derniere_activite,
                    "nombre_agents": 10,
                    "nombre_offres_publiees": 20,
                }
                for organisme in organismes
            ]
            return Response(OrganismesListSerializer(organismes_dto, many=True).data)
        except OperationOrganismeRefusee as e:
            serializer = GenericErrorSerializer({"error": str(e)})
            return Response(serializer.data, status=status.HTTP_403_FORBIDDEN)
        except Exception:
            serializer = GenericErrorSerializer({"error": "Unexpected error"})
            return Response(
                serializer.data, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request: Request) -> Response:
        serializer = CreateOrganismeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            usecase = self.container.create_organisme_usecase()
            command = CreateOrganismeCommand(
                nom=serializer.validated_data["nom"],
                versant=Verse(serializer.validated_data["versant"]),
                localisation=None,
                siret=SIRET(code=serializer.validated_data["siret"]),
                parent_id=None,
                utilisateur=self.user_mapper.to_domain(request),
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
        except (OrganismeSiretExisteDeja, ValidationError) as e:
            serializer = GenericErrorSerializer({"error": str(e)})
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
        except OperationOrganismeRefusee as e:
            serializer = GenericErrorSerializer({"error": str(e)})
            return Response(serializer.data, status=status.HTTP_403_FORBIDDEN)
        except Exception:
            serializer = GenericErrorSerializer({"error": "Unexpected error"})
            return Response(
                serializer.data, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
