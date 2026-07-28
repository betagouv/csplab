from uuid import UUID

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from application.recruteur.usecases.changer_etape_candidatures import (
    CandidatureAChanger,
    ChangerEtapeCandidaturesCommand,
)
from domain.identite.errors.organisme_errors import OrganismeNexistePas
from infrastructure.di.recruteur.recruteur_factory import recruteur_container
from presentation.api.serializers import GenericErrorSerializer, TokenErrorSerializer
from presentation.recruteur.serializers import (
    ChangerEtapeCandidaturesSerializer,
    ChangerEtapeResultatSerializer,
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
