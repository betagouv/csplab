from uuid import UUID

from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from application.recruteur.errors.application_errors_recruteur import (
    RecrutementEtapeIncoherents,
)
from application.recruteur.services.get_recrutement_etapes import (
    get_recrutement_etapes,
)
from application.recruteur.services.initialize_recrutement_etapes import (
    initialize_recrutement_etapes,
)
from application.recruteur.services.update_recrutement_etapes import (
    update_recrutement_etapes,
)
from domain.commons.errors.organisme_errors import OrganismeNexistePas
from domain.identite.errors.organisme_permission_errors import (
    OrganismePermissionError,
)
from domain.recruteur.errors.organisme_recruteur_errors import (
    ConfigurationEtapesInvalide,
)
from domain.recruteur.errors.recrutement_errors import (
    RecrutementInexistant,
    SupressionEtapeImpossible,
)
from domain.recruteur.value_objects.categorie_etapes_recrutement import (
    CategorieEtapeRecrutement,
)
from domain.recruteur.value_objects.etape_data import EtapeData
from presentation.api.authentication import SessionApiMixin
from presentation.api.serializers import GenericErrorSerializer, TokenErrorSerializer
from presentation.recruteur.serializers import (
    EtapeRecrutementModelSerializer,
    EtapeRecrutementSerializer,
    UpdateEtapeRecrutementSerializer,
)


@extend_schema_view(
    get=extend_schema(
        summary="Étapes d'un recrutement",
        tags=["recruteur"],
        responses={
            200: EtapeRecrutementSerializer(many=True),
            401: TokenErrorSerializer,
            403: GenericErrorSerializer,
            404: GenericErrorSerializer,
            500: GenericErrorSerializer,
        },
    ),
    patch=extend_schema(
        summary="Modifier les étapes d'un recrutement",
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
class RecrutementEtapeView(SessionApiMixin, APIView):
    def get(
        self, request: Request, organisme_uuid: UUID, recrutement_uuid: UUID
    ) -> Response:
        try:
            etapes = get_recrutement_etapes(
                organisme_id=organisme_uuid,
                recrutement_id=recrutement_uuid,
                utilisateur=request.user,
            )
            serializer = EtapeRecrutementModelSerializer(etapes, many=True)
            return Response(serializer.data)
        except OrganismePermissionError as e:
            error_serializer = GenericErrorSerializer({"error": str(e)})
            return Response(error_serializer.data, status=status.HTTP_403_FORBIDDEN)
        except (OrganismeNexistePas, RecrutementInexistant) as e:
            error_serializer = GenericErrorSerializer({"error": str(e)})
            return Response(error_serializer.data, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            error_serializer = GenericErrorSerializer({"error": "Unexpected error"})
            return Response(
                error_serializer.data, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def patch(
        self, request: Request, organisme_uuid: UUID, recrutement_uuid: UUID
    ) -> Response:
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
            etapes = update_recrutement_etapes(
                organisme_id=organisme_uuid,
                recrutement_id=recrutement_uuid,
                utilisateur=request.user,
                etapes=etapes_data,
            )
            out_serializer = EtapeRecrutementModelSerializer(etapes, many=True)
            return Response(out_serializer.data)
        except (
            RecrutementEtapeIncoherents,
            SupressionEtapeImpossible,
            ConfigurationEtapesInvalide,
        ) as e:
            error_serializer = GenericErrorSerializer({"error": str(e)})
            return Response(error_serializer.data, status=status.HTTP_400_BAD_REQUEST)
        except OrganismePermissionError as e:
            error_serializer = GenericErrorSerializer({"error": str(e)})
            return Response(error_serializer.data, status=status.HTTP_403_FORBIDDEN)
        except (OrganismeNexistePas, RecrutementInexistant) as e:
            error_serializer = GenericErrorSerializer({"error": str(e)})
            return Response(error_serializer.data, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            error_serializer = GenericErrorSerializer({"error": "Unexpected error"})
            return Response(
                error_serializer.data, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@extend_schema(
    summary="Réinitialiser les étapes par défaut d'un recrutement",
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
class InitRecrutementEtapeView(SessionApiMixin, APIView):
    def post(
        self, request: Request, organisme_uuid: UUID, recrutement_uuid: UUID
    ) -> Response:
        try:
            etapes = initialize_recrutement_etapes(
                organisme_id=organisme_uuid,
                recrutement_id=recrutement_uuid,
                utilisateur=request.user,
            )
            serializer = EtapeRecrutementModelSerializer(etapes, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except SupressionEtapeImpossible as e:
            error_serializer = GenericErrorSerializer({"error": str(e)})
            return Response(error_serializer.data, status=status.HTTP_400_BAD_REQUEST)
        except OrganismePermissionError as e:
            error_serializer = GenericErrorSerializer({"error": str(e)})
            return Response(error_serializer.data, status=status.HTTP_403_FORBIDDEN)
        except (OrganismeNexistePas, RecrutementInexistant) as e:
            error_serializer = GenericErrorSerializer({"error": str(e)})
            return Response(error_serializer.data, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            error_serializer = GenericErrorSerializer({"error": "Unexpected error"})
            return Response(
                error_serializer.data, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
