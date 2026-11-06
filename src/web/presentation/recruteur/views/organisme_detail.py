from uuid import UUID

from drf_spectacular.utils import extend_schema, extend_schema_view
from referentiel.value_objects.verse import Verse
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from application.recruteur.services.get_organisme import get_organisme
from application.recruteur.services.get_organisme_etapes import get_organisme_etapes
from application.recruteur.services.initialize_organisme_etapes import (
    initialize_organisme_etapes,
)
from application.recruteur.services.list_motifs_refus import list_motifs_refus
from application.recruteur.services.update_organisme import update_organisme
from application.recruteur.services.update_organisme_etapes import (
    update_organisme_etapes,
)
from domain.commons.errors.organisme_errors import OrganismeNexistePas
from domain.identite.errors.organisme_permission_errors import (
    AccesOrganismeRefuse,
    OperationOrganismeRefusee,
)
from domain.recruteur.errors.organisme_recruteur_errors import (
    ConfigurationEtapesInvalide,
)
from domain.recruteur.value_objects.categorie_etapes_recrutement import (
    CategorieEtapeRecrutement,
)
from domain.recruteur.value_objects.etape_data import EtapeData
from presentation.api.authentication import SessionApiMixin
from presentation.api.serializers import (
    GenericErrorSerializer,
    generic_response_format,
)
from presentation.commons.conditional_get import ConditionalGetMixin
from presentation.recruteur.serializers import (
    EtapeOrganismeSerializer,
    EtapeRecrutementSerializer,
    MotifRefusSerializer,
    OrganismeDetailSerializer,
    OrganismeReadSerializer,
    UpdateEtapeRecrutementSerializer,
    UpdateOrganismeSerializer,
)


@extend_schema_view(
    get=extend_schema(
        summary="Récupérer un organisme",
        tags=["recruteur"],
        responses={
            **generic_response_format,
            200: OrganismeReadSerializer,
        },
    ),
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
class OrganismeDetailView(ConditionalGetMixin, SessionApiMixin, APIView):
    serializer_class = OrganismeDetailSerializer

    def get(self, request: Request, organisme_uuid: UUID) -> Response:
        try:
            organisme = get_organisme(
                organisme_id=organisme_uuid, utilisateur=request.user
            )
            return Response(OrganismeReadSerializer(organisme).data)
        except OrganismeNexistePas as e:
            serializer = GenericErrorSerializer({"error": str(e)})
            return Response(serializer.data, status=status.HTTP_404_NOT_FOUND)
        except (AccesOrganismeRefuse, OperationOrganismeRefusee) as e:
            serializer = GenericErrorSerializer({"error": str(e)})
            return Response(serializer.data, status=status.HTTP_403_FORBIDDEN)
        except Exception:
            serializer = GenericErrorSerializer({"error": "Unexpected error"})
            return Response(
                serializer.data, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def put(self, request: Request, organisme_uuid: UUID) -> Response:
        serializer = UpdateOrganismeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            data = serializer.validated_data
            organisme = update_organisme(
                organisme_id=organisme_uuid,
                utilisateur=request.user,
                nom=data["nom"],
                versant=Verse(data["versant"]),
                gestion_ats=data["gestion_ats"],
            )
            return Response(
                OrganismeDetailSerializer(organisme).data,
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
class EtapesRecrutementOrganismeView(ConditionalGetMixin, SessionApiMixin, APIView):
    def get(self, request: Request, organisme_uuid: UUID) -> Response:
        try:
            organisme = get_organisme_etapes(
                organisme_id=organisme_uuid,
                utilisateur=request.user,
            )
            serializer = EtapeOrganismeSerializer(organisme.etapes, many=True)
            return Response(serializer.data)
        except AccesOrganismeRefuse:
            return Response(
                GenericErrorSerializer({"error": "Forbidden."}).data,
                status=status.HTTP_403_FORBIDDEN,
            )
        except OrganismeNexistePas:
            return Response(
                GenericErrorSerializer({"error": "organisme_uuid: Not found."}).data,
                status=status.HTTP_404_NOT_FOUND,
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
        etapes_data = [
            EtapeData(
                etape_uuid=etape.get("etape_uuid"),
                nom=etape["nom"],
                categorie=CategorieEtapeRecrutement[etape["categorie"]],
            )
            for etape in validated_etapes
        ]
        try:
            organisme = update_organisme_etapes(
                organisme_id=organisme_uuid,
                utilisateur=request.user,
                etapes=etapes_data,
            )
            return Response(EtapeOrganismeSerializer(organisme.etapes, many=True).data)
        except ConfigurationEtapesInvalide as e:
            return Response({"error": e.raison}, status=status.HTTP_400_BAD_REQUEST)
        except AccesOrganismeRefuse:
            return Response(
                GenericErrorSerializer({"error": "Forbidden."}).data,
                status=status.HTTP_403_FORBIDDEN,
            )
        except OrganismeNexistePas:
            return Response(
                GenericErrorSerializer({"error": "organisme_uuid: Not found."}).data,
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception:
            serializer = GenericErrorSerializer({"error": "Unexpected error"})
            return Response(
                serializer.data, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@extend_schema_view(
    get=extend_schema(
        summary="Liste des motifs de refus d'une candidature",
        tags=["recruteur"],
        responses={
            **generic_response_format,
            200: MotifRefusSerializer(many=True),
        },
    ),
)
class MotifsRefusOrganismeView(ConditionalGetMixin, SessionApiMixin, APIView):
    def get(self, request: Request, organisme_uuid: UUID) -> Response:
        try:
            motifs = list_motifs_refus(
                organisme_id=organisme_uuid,
                utilisateur=request.user,
            )
            data = [{"value": m.value, "label": m.label} for m in motifs]
            return Response(MotifRefusSerializer(data, many=True).data)
        except AccesOrganismeRefuse as e:
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


@extend_schema(
    summary="Initialiser les étapes de recrutement par défaut d'un organisme",
    tags=["recruteur"],
    request=None,
    responses={
        **generic_response_format,
        201: EtapeRecrutementSerializer(many=True),
    },
)
class InitEtapesRecrutementOrganismeView(ConditionalGetMixin, SessionApiMixin, APIView):
    def post(self, request: Request, organisme_uuid: UUID) -> Response:
        try:
            organisme = initialize_organisme_etapes(
                organisme_id=organisme_uuid,
                utilisateur=request.user,
            )
            serializer = EtapeOrganismeSerializer(organisme.etapes, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except AccesOrganismeRefuse:
            return Response(
                GenericErrorSerializer({"error": "Forbidden."}).data,
                status=status.HTTP_403_FORBIDDEN,
            )
        except OrganismeNexistePas:
            return Response(
                GenericErrorSerializer({"error": "organisme_uuid: Not found."}).data,
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception:
            serializer = GenericErrorSerializer({"error": "Unexpected error"})
            return Response(
                serializer.data, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
