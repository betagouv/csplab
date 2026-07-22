from uuid import UUID

from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

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
from domain.identite.errors.organisme_errors import OrganismeNexistePas
from domain.recruteur.errors.erreur_recrutement import (
    ConfigurationEtapesInvalide,
    ErreurRecruteur,
)
from domain.recruteur.errors.organisme_permission_errors import AccesOrganismeRefuse
from domain.recruteur.value_objects.categorie_etapes_recrutement import (
    CategorieEtapeRecrutement,
)
from infrastructure.di.recruteur.recruteur_factory import recruteur_container
from presentation.api.serializers import GenericErrorSerializer, TokenErrorSerializer
from presentation.recruteur.mappers import (
    EtapesMapper,
)
from presentation.recruteur.serializers import (
    EtapeRecrutementSerializer,
    OrganismeSerializer,
    UpdateEtapeRecrutementSerializer,
)


@extend_schema(
    summary="Detail d'un organisme",
    tags=["recruteur"],
    responses={
        200: OrganismeSerializer,
        401: TokenErrorSerializer,
        403: GenericErrorSerializer,
        404: GenericErrorSerializer,
        500: GenericErrorSerializer,
    },
)
class OrganismeView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrganismeSerializer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.container = recruteur_container()

    def get(self, request: Request, organisme_uuid: UUID) -> Response:
        try:
            utilisateur_id = UUID(request.user.username)
            usecase = self.container.get_organisme_recruteur_usecase()
            organisme = usecase.execute(
                GetOrganismeRecruteurQuery(
                    organisme_id=organisme_uuid,
                    utilisateur_id=utilisateur_id,
                    est_staff=request.user.is_staff,
                )
            )
            serializer = OrganismeSerializer(organisme)
            return Response(serializer.data)
        except AccesOrganismeRefuse:
            return Response({"detail": "Forbidden."}, status=status.HTTP_403_FORBIDDEN)
        except (ErreurRecruteur, OrganismeNexistePas):
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
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
            200: EtapeRecrutementSerializer(many=True),
            401: TokenErrorSerializer,
            403: GenericErrorSerializer,
            404: GenericErrorSerializer,
            500: GenericErrorSerializer,
        },
    ),
    put=extend_schema(
        summary="Modifier les étapes de recrutement d'un organisme",
        tags=["recruteur"],
        request=UpdateEtapeRecrutementSerializer(many=True),
        responses={
            200: EtapeRecrutementSerializer(many=True),
            400: GenericErrorSerializer,
            401: TokenErrorSerializer,
            403: GenericErrorSerializer,
            404: GenericErrorSerializer,
            500: GenericErrorSerializer,
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
            utilisateur_id = UUID(request.user.username)
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
            utilisateur_id = UUID(request.user.username)
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
        201: EtapeRecrutementSerializer(many=True),
        401: TokenErrorSerializer,
        403: GenericErrorSerializer,
        404: GenericErrorSerializer,
        500: GenericErrorSerializer,
    },
)
class InitEtapesRecrutementOrganismeView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.container = recruteur_container()

    def post(self, request: Request, organisme_uuid: UUID) -> Response:
        try:
            utilisateur_id = UUID(request.user.username)
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
