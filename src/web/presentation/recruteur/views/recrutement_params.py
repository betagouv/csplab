from uuid import UUID

from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from application.recruteur.dtos.etape_data import EtapeData
from application.recruteur.dtos.recrutement_request import (
    RecrutementRequest,
)
from application.recruteur.errors.application_errors_recruteur import (
    OrganismeRecrutementIncoherents,
    OrganismeRecruteurSansEtapes,
)
from application.recruteur.usecases.get_recrutement_etapes import (
    GetRecrutementEtapesQuery,
)
from application.recruteur.usecases.update_recrutement_etapes import (
    UpdateRecrutementEtapesCommand,
)
from domain.commons.errors.organisme_errors import OrganismeNexistePas
from domain.identite.errors.organisme_permission_errors import (
    OrganismePermissionError,
)
from domain.recruteur.entities.etape_recrutement import EtapeRecrutement
from domain.recruteur.errors.recrutement_errors import (
    RecrutementInexistant,
    SupressionEtapeImpossible,
)
from domain.recruteur.value_objects.categorie_etapes_recrutement import (
    CategorieEtapeRecrutement,
)
from infrastructure.di.recruteur.recruteur_factory import recruteur_container
from presentation.api.serializers import GenericErrorSerializer, TokenErrorSerializer
from presentation.recruteur.mappers import UtilisateurMapper
from presentation.recruteur.serializers import (
    EtapeRecrutementSerializer,
    UpdateEtapeRecrutementSerializer,
)


def _fake_etapes_to_serializer_data(etapes: list) -> list[dict]:
    return [
        {"etape_uuid": e.etape_uuid, "nom": e.nom, "categorie": e.categorie.name}
        for e in etapes
    ]


def _etapes_to_serializer_data(etapes: tuple[EtapeRecrutement, ...]) -> list[dict]:
    return [
        {"etape_uuid": e.entity_id, "nom": e.nom, "categorie": e.categorie.name}
        for e in etapes
    ]


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
class RecrutementEtapeView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.container = recruteur_container()
        self.user_mapper = UtilisateurMapper()

    def get(
        self, request: Request, organisme_uuid: UUID, recrutement_uuid: UUID
    ) -> Response:
        try:
            usecase = self.container.get_recrutement_etapes_usecase()
            resultat = usecase.execute(
                GetRecrutementEtapesQuery(
                    organisme_id=organisme_uuid,
                    recrutement_id=recrutement_uuid,
                    utilisateur=self.user_mapper.to_domain(request),
                )
            )
            serializer = EtapeRecrutementSerializer(
                _fake_etapes_to_serializer_data(resultat), many=True
            )
            return Response(serializer.data)
        except OrganismePermissionError:
            return Response({"detail": "Forbidden."}, status=status.HTTP_403_FORBIDDEN)
        except OrganismeNexistePas:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
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
        etapes = [
            EtapeData(
                etape_uuid=etape.get("etape_uuid"),
                nom=etape["nom"],
                categorie=CategorieEtapeRecrutement[etape["categorie"]],
            )
            for etape in validated_etapes
        ]
        try:
            usecase = self.container.update_recrutement_etapes_usecase()
            resultat = usecase.execute(
                UpdateRecrutementEtapesCommand(
                    organisme_id=organisme_uuid,
                    recrutement_id=recrutement_uuid,
                    utilisateur=self.user_mapper.to_domain(request),
                    etapes=etapes,
                )
            )
            out_serializer = EtapeRecrutementSerializer(
                _fake_etapes_to_serializer_data(resultat), many=True
            )
            return Response(out_serializer.data)
        except (OrganismeRecruteurSansEtapes, OrganismeRecrutementIncoherents) as e:
            error_serializer = GenericErrorSerializer({"error": str(e)})
            return Response(error_serializer.data, status=status.HTTP_400_BAD_REQUEST)
        except OrganismePermissionError:
            return Response({"detail": "Forbidden."}, status=status.HTTP_403_FORBIDDEN)
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
class InitRecrutementEtapeView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.container = recruteur_container()
        self.user_mapper = UtilisateurMapper()

    def post(
        self, request: Request, organisme_uuid: UUID, recrutement_uuid: UUID
    ) -> Response:
        try:
            usecase = self.container.init_recrutement_etapes_usecase()
            resultat = usecase.execute(
                RecrutementRequest(
                    organisme_id=organisme_uuid,
                    recrutement_id=recrutement_uuid,
                    utilisateur=self.user_mapper.to_domain(request),
                )
            )
            serializer = EtapeRecrutementSerializer(
                _etapes_to_serializer_data(resultat), many=True
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except (
            OrganismeRecruteurSansEtapes,
            OrganismeRecrutementIncoherents,
            SupressionEtapeImpossible,
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
