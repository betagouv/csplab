from uuid import UUID

from drf_spectacular.utils import extend_schema, extend_schema_view
from referentiel.value_objects.verse import Verse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from application.identite.usecases.update_organisme import (
    UpdateOrganismeCommand,
)
from application.recruteur.usecases.get_organisme_recruteur import (
    GetOrganismeRecruteurQuery,
)
from application.recruteur.usecases.initialize_organisme_steps import (
    InitializeOrganismeStepsCommand,
)
from application.recruteur.usecases.update_organisme_steps import (
    EtapeData,
    UpdateOrganismeStepsCommand,
)
from domain.commons.errors.organisme_errors import OrganismeNexistePas
from domain.identite.errors.organisme_permission_errors import OperationOrganismeRefusee
from domain.recruteur.errors.erreur_recrutement import (
    ConfigurationEtapesInvalide,
    ErreurRecruteur,
)
from domain.recruteur.errors.organisme_permission_errors import AccesOrganismeRefuse
from domain.recruteur.value_objects.categorie_etapes_recrutement import (
    CategorieEtapeRecrutement,
)
from infrastructure.di.identite.identite_factory import create_identite_container
from infrastructure.di.recruteur.recruteur_factory import recruteur_container
from presentation.api.serializers import (
    GenericErrorSerializer,
    generic_response_format,
)
from presentation.recruteur.mappers import (
    EtapesMapper,
)
from presentation.recruteur.serializers import (
    EtapeRecrutementSerializer,
    OrganismeDetailSerializer,
    UpdateEtapeRecrutementSerializer,
    UpdateOrganismeSerializer,
)


@extend_schema_view(
    put=extend_schema(
        summary="Modifier un organisme",
        tags=["recruteur"],
        request=UpdateOrganismeSerializer,
        responses={
            **generic_response_format,
            200: OrganismeDetailSerializer,
            400: GenericErrorSerializer,
        },
    ),
)
class OrganismeDetailView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrganismeDetailSerializer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.container = create_identite_container()

    def put(self, request: Request, organisme_uuid: UUID) -> Response:
        serializer = UpdateOrganismeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            usecase = self.container.update_organisme_usecase()
            data = serializer.validated_data
            command = UpdateOrganismeCommand(
                organisme_id=organisme_uuid,
                name=data.get("nom"),
                verse=Verse(data["versant"]) if data.get("versant") else None,
                managed_ats=data.get("gestion_ats"),
                is_staff=request.user.is_staff,
            )
            organisme = usecase.execute(command)
            organisme_dto = {
                **data,
                "organisme_uuid": str(organisme.entity_id),
                "nom": data["nom"] if data.get("nom") is not None else organisme.nom,
                "siret": organisme.siret.code,
                "versant": data["versant"]
                if data.get("versant") is not None
                else organisme.versant,
                "gestionnaire": None,
                "gestion_ats": data["gestion_ats"]
                if data.get("gestion_ats") is not None
                else True,
                "date_derniere_activite": "2026-01-15T10:00:00Z",
                "date_creation": "2026-01-01T09:00:00Z",
            }
            return Response(
                OrganismeDetailSerializer(organisme_dto).data,
                status=status.HTTP_200_OK,
            )
        except OperationOrganismeRefusee as e:
            serializer = GenericErrorSerializer({"error": str(e)})
            return Response(serializer.data, status=status.HTTP_403_FORBIDDEN)
        except OrganismeNexistePas as e:
            serializer = GenericErrorSerializer({"error": str(e)})
            return Response(serializer.data, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            serializer = GenericErrorSerializer({"error": "Unexpected error"})
            return Response(
                serializer.data, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@extend_schema_view(
    get=extend_schema(
        summary="Liste des étapes de recrutement d'un organisme",
        tags=["recruteur"],
        responses={
            **generic_response_format,
            200: EtapeRecrutementSerializer(many=True),
        },
    ),
    put=extend_schema(
        summary="Modifier les étapes de recrutement d'un organisme",
        tags=["recruteur"],
        request=UpdateEtapeRecrutementSerializer(many=True),
        responses={
            **generic_response_format,
            200: EtapeRecrutementSerializer(many=True),
            400: GenericErrorSerializer,
        },
    ),
)
class EtapesRecrutementOrganismeView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.container = recruteur_container()

    def get(self, request: Request, organisme_uuid: UUID) -> Response:
        try:
            utilisateur_id = request.user.username
            usecase = self.container.get_organisme_recruteur_usecase()
            organisme = usecase.execute(
                GetOrganismeRecruteurQuery(
                    organisme_id=organisme_uuid,
                    utilisateur_id=utilisateur_id,
                    est_staff=request.user.is_staff,
                )
            )
            data = EtapesMapper().from_domain(organisme)
            serializer = EtapeRecrutementSerializer(data, many=True)
            return Response(serializer.data)
        except AccesOrganismeRefuse:
            return Response({"detail": "Forbidden."}, status=status.HTTP_403_FORBIDDEN)
        except OrganismeNexistePas:
            return Response(
                {"organisme_uuid": "Not found."}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception:
            serializer = GenericErrorSerializer({"error": "Unexpected error"})
            return Response(
                serializer.data, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def put(self, request: Request, organisme_uuid: UUID) -> Response:
        serializer = UpdateEtapeRecrutementSerializer(data=request.data, many=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_etapes: list = serializer.validated_data  # type: ignore[assignment]
        etapes = [
            EtapeData(
                etape_uuid=etape.get("etape_uuid"),
                nom=etape["nom"],
                categorie=CategorieEtapeRecrutement[etape["categorie"]],
            )
            for etape in validated_etapes
        ]
        try:
            utilisateur_id = request.user.username
            usecase = self.container.update_organisme_steps_usecase()
            organisme = usecase.execute(
                UpdateOrganismeStepsCommand(
                    organisme_id=organisme_uuid,
                    utilisateur_id=utilisateur_id,
                    etapes=etapes,
                    est_staff=request.user.is_staff,
                )
            )
            data = EtapesMapper().from_domain(organisme)
            out_serializer = EtapeRecrutementSerializer(data, many=True)
            return Response(out_serializer.data)
        except ConfigurationEtapesInvalide as e:
            return Response({"error": e.raison}, status=status.HTTP_400_BAD_REQUEST)
        except AccesOrganismeRefuse:
            return Response({"detail": "Forbidden."}, status=status.HTTP_403_FORBIDDEN)
        except OrganismeNexistePas:
            return Response(
                {"organisme_uuid": "Not found."}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception:
            serializer = GenericErrorSerializer({"error": "Unexpected error"})
            return Response(
                serializer.data, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@extend_schema(
    summary="Initialiser les étapes de recrutement par défaut d'un organisme",
    tags=["recruteur"],
    request=None,
    responses={
        **generic_response_format,
        201: EtapeRecrutementSerializer(many=True),
    },
)
class InitEtapesRecrutementOrganismeView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.container = recruteur_container()

    def post(self, request: Request, organisme_uuid: UUID) -> Response:
        try:
            utilisateur_id = request.user.username
            usecase = self.container.initialize_organisme_steps_usecase()
            organisme = usecase.execute(
                InitializeOrganismeStepsCommand(
                    organisme_id=organisme_uuid,
                    utilisateur_id=utilisateur_id,
                    est_staff=request.user.is_staff,
                )
            )
            data = EtapesMapper().from_domain(organisme)
            serializer = EtapeRecrutementSerializer(data, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except AccesOrganismeRefuse:
            return Response({"detail": "Forbidden."}, status=status.HTTP_403_FORBIDDEN)
        except (ErreurRecruteur, OrganismeNexistePas):
            return Response(
                {"organisme_uuid": "Not found."}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception:
            serializer = GenericErrorSerializer({"error": "Unexpected error"})
            return Response(
                serializer.data, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
