from uuid import UUID

from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from application.recruteur.dtos.etape_data import EtapeData
from application.recruteur.usecases.changer_etape_candidatures import (
    CandidatureAChanger,
    ChangerEtapeCandidaturesCommand,
)
from application.recruteur.usecases.get_recrutement_etapes import (
    GetRecrutementEtapesQuery,
)
from application.recruteur.usecases.init_recrutement_etapes import (
    InitRecrutementEtapesCommand,
)
from application.recruteur.usecases.update_recrutement_etapes import (
    UpdateRecrutementEtapesCommand,
)
from domain.identite.errors.organisme_errors import OrganismeNexistePas
from domain.recruteur.value_objects.categorie_etapes_recrutement import (
    CategorieEtapeRecrutement,
)
from infrastructure.di.recruteur.recruteur_factory import recruteur_container
from presentation.api.serializers import GenericErrorSerializer, TokenErrorSerializer
from presentation.recruteur.serializers import (
    ChangerEtapeCandidaturesSerializer,
    ChangerEtapeResultatSerializer,
    EtapeRecrutementSerializer,
    UpdateEtapeRecrutementSerializer,
)


# TODO: stub sans persistance, voir ChangerEtapeCandidaturesUsecase.
@extend_schema(
    summary="Changer l'étape d'une ou plusieurs candidatures (batch, statique)",
    tags=["recruteur"],
    request=ChangerEtapeCandidaturesSerializer,
    responses={
        200: ChangerEtapeResultatSerializer,
        400: GenericErrorSerializer,
        401: TokenErrorSerializer,
        404: GenericErrorSerializer,
        500: GenericErrorSerializer,
    },
)
class RecrutementCandidaturesEtapeView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.container = recruteur_container()

    def patch(
        self, request: Request, organisme_uuid: UUID, recrutement_uuid: UUID
    ) -> Response:
        serializer = ChangerEtapeCandidaturesSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        try:
            usecase = self.container.changer_etape_candidatures_usecase()
            resultat = usecase.execute(
                ChangerEtapeCandidaturesCommand(
                    organisme_id=organisme_uuid,
                    recrutement_id=recrutement_uuid,
                    etape_cible_id=data["etape_cible_uuid"],
                    candidatures=[
                        CandidatureAChanger(
                            candidature_id=c["candidature_uuid"],
                            etape_actuelle_id=c["etape_actuelle_uuid"],
                        )
                        for c in data["candidatures"]
                    ],
                )
            )
            return Response(
                ChangerEtapeResultatSerializer(
                    {
                        "reussites": resultat.reussites,
                        "echecs": [
                            {"candidature_uuid": cid, "raison": reason}
                            for cid, reason in resultat.echecs
                        ],
                    }
                ).data
            )
        except OrganismeNexistePas:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            error_serializer = GenericErrorSerializer({"error": "Unexpected error"})
            return Response(
                error_serializer.data, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


def _etapes_to_serializer_data(etapes: list) -> list[dict]:
    return [
        {"etape_uuid": e.etape_uuid, "nom": e.nom, "categorie": e.categorie.name}
        for e in etapes
    ]


@extend_schema_view(
    get=extend_schema(
        summary="Étapes d'un recrutement",
        tags=["recruteur"],
        responses={
            200: EtapeRecrutementSerializer(many=True),
            401: TokenErrorSerializer,
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

    def get(
        self, request: Request, organisme_uuid: UUID, recrutement_uuid: UUID
    ) -> Response:
        try:
            usecase = self.container.get_recrutement_etapes_usecase()
            resultat = usecase.execute(
                GetRecrutementEtapesQuery(
                    organisme_id=organisme_uuid,
                    recrutement_id=recrutement_uuid,
                    utilisateur_id=UUID(request.user.username),
                    est_staff=request.user.is_staff,
                )
            )
            serializer = EtapeRecrutementSerializer(
                _etapes_to_serializer_data(resultat), many=True
            )
            return Response(serializer.data)
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
                    utilisateur_id=UUID(request.user.username),
                    est_staff=request.user.is_staff,
                    etapes=etapes,
                )
            )
            out_serializer = EtapeRecrutementSerializer(
                _etapes_to_serializer_data(resultat), many=True
            )
            return Response(out_serializer.data)
        except OrganismeNexistePas:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
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
        404: GenericErrorSerializer,
        500: GenericErrorSerializer,
    },
)
class InitRecrutementEtapeView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.container = recruteur_container()

    def post(
        self, request: Request, organisme_uuid: UUID, recrutement_uuid: UUID
    ) -> Response:
        try:
            usecase = self.container.init_recrutement_etapes_usecase()
            resultat = usecase.execute(
                InitRecrutementEtapesCommand(
                    organisme_id=organisme_uuid,
                    recrutement_id=recrutement_uuid,
                    utilisateur_id=UUID(request.user.username),
                    est_staff=request.user.is_staff,
                )
            )
            serializer = EtapeRecrutementSerializer(
                _etapes_to_serializer_data(resultat), many=True
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except OrganismeNexistePas:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            error_serializer = GenericErrorSerializer({"error": "Unexpected error"})
            return Response(
                error_serializer.data, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
