from uuid import UUID

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from application.recruteur.usecases.changer_etape_candidatures import (
    ChangerEtapeCandidaturesCommand,
)
from application.recruteur.usecases.get_recrutement_detail import (
    GetRecrutementDetailQuery,
)
from application.recruteur.usecases.get_recrutement_kanban import (
    GetRecrutementKanbanQuery,
)
from application.recruteur.usecases.get_recrutement_liste import (
    GetRecrutementListeQuery,
)
from domain.commons.errors.organisme_errors import OrganismeNexistePas
from domain.identite.errors.organisme_permission_errors import (
    OrganismePermissionError,
)
from domain.recruteur.errors.recrutement_errors import (
    CandidatureInexistante,
    RecrutementEtapeInexistante,
    RecrutementInexistant,
)
from infrastructure.di.recruteur.recruteur_factory import recruteur_container
from presentation.api.serializers import GenericErrorSerializer, TokenErrorSerializer
from presentation.commons.pagination import WebPagination
from presentation.recruteur.mappers import UtilisateurMapper
from presentation.recruteur.serializers import (
    CandidatureListeSerializer,
    ChangerEtapeCandidaturesSerializer,
    ChangerEtapeResultatSerializer,
    RecrutementDetailKanbanSerializer,
    RecrutementDetailSerializer,
)


@extend_schema(
    summary="Détail d'un recrutement",
    tags=["recruteur"],
    responses={
        200: RecrutementDetailSerializer,
        401: TokenErrorSerializer,
        403: GenericErrorSerializer,
        404: GenericErrorSerializer,
        500: GenericErrorSerializer,
    },
)
class RecrutementDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.container = recruteur_container()
        self.user_mapper = UtilisateurMapper()

    def get(
        self, request: Request, organisme_uuid: UUID, recrutement_uuid: UUID
    ) -> Response:
        try:
            usecase = self.container.get_recrutement_detail_usecase()
            result = usecase.execute(
                GetRecrutementDetailQuery(
                    organisme_id=organisme_uuid,
                    recrutement_id=recrutement_uuid,
                    utilisateur=self.user_mapper.to_domain(request),
                )
            )
            if result is None:
                return Response(
                    {"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND
                )

            serializer = RecrutementDetailSerializer(result)
            return Response(serializer.data)
        except OrganismePermissionError:
            return Response({"detail": "Forbidden."}, status=status.HTTP_403_FORBIDDEN)
        except OrganismeNexistePas:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            serializer = GenericErrorSerializer({"error": "Unexpected error"})
            return Response(
                serializer.data, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@extend_schema(
    summary="Détail d'un recrutement — vue kanban",
    tags=["recruteur"],
    responses={
        200: RecrutementDetailKanbanSerializer,
        401: TokenErrorSerializer,
        403: GenericErrorSerializer,
        404: GenericErrorSerializer,
        500: GenericErrorSerializer,
    },
)
class RecrutementKanbanView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.container = recruteur_container()
        self.user_mapper = UtilisateurMapper()

    def get(
        self, request: Request, organisme_uuid: UUID, recrutement_uuid: UUID
    ) -> Response:
        try:
            usecase = self.container.get_recrutement_kanban_usecase()
            result = usecase.execute(
                GetRecrutementKanbanQuery(
                    organisme_id=organisme_uuid,
                    recrutement_id=recrutement_uuid,
                    utilisateur=self.user_mapper.to_domain(request),
                )
            )
            if result is None:
                return Response(
                    {"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND
                )

            serializer = RecrutementDetailKanbanSerializer(result)
            return Response(serializer.data)
        except OrganismePermissionError:
            return Response({"detail": "Forbidden."}, status=status.HTTP_403_FORBIDDEN)
        except OrganismeNexistePas:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            serializer = GenericErrorSerializer({"error": "Unexpected error"})
            return Response(
                serializer.data, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@extend_schema(
    summary="Détail d'un recrutement — vue liste (paginée)",
    tags=["recruteur"],
    responses={
        200: CandidatureListeSerializer(many=True),
        400: GenericErrorSerializer,
        401: TokenErrorSerializer,
        403: GenericErrorSerializer,
        404: GenericErrorSerializer,
        500: GenericErrorSerializer,
    },
)
class RecrutementListeView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = WebPagination

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.container = recruteur_container()
        self.user_mapper = UtilisateurMapper()

    def get(
        self, request: Request, organisme_uuid: UUID, recrutement_uuid: UUID
    ) -> Response:
        try:
            usecase = self.container.get_recrutement_liste_usecase()
            result = usecase.execute(
                GetRecrutementListeQuery(
                    organisme_id=organisme_uuid,
                    recrutement_id=recrutement_uuid,
                    utilisateur=self.user_mapper.to_domain(request),
                )
            )
            if result is None:
                return Response(
                    {"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND
                )

            paginator = WebPagination()
            items = paginator.paginate(result, request)
            return paginator.get_paginated_response(
                CandidatureListeSerializer(items, many=True).data
            )
        except OrganismePermissionError:
            return Response({"detail": "Forbidden."}, status=status.HTTP_403_FORBIDDEN)
        except OrganismeNexistePas:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            serializer = GenericErrorSerializer({"error": "Unexpected error"})
            return Response(
                serializer.data, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


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
        self.user_mapper = UtilisateurMapper()

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
                    candidatures=[c["candidature_uuid"] for c in data["candidatures"]],
                    utilisateur=self.user_mapper.to_domain(request),
                )
            )
            return Response(
                ChangerEtapeResultatSerializer(
                    {
                        "reussites": [c.entity_id for c in resultat["successes"]],
                        "echecs": [
                            {"candidature_uuid": cid, "raison": reason}
                            for cid, reason in resultat["failures"]
                        ],
                    }
                ).data
            )
        except (
            OrganismeNexistePas,
            RecrutementInexistant,
            CandidatureInexistante,
        ) as e:
            serializer = GenericErrorSerializer({"error": str(e)})
            return Response(serializer.data, status=status.HTTP_404_NOT_FOUND)
        except RecrutementEtapeInexistante as e:
            serializer = GenericErrorSerializer({"error": str(e)})
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response(
                {"error": "Unexpected error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
