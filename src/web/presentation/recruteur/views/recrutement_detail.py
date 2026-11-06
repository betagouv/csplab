from uuid import UUID

from django.db.models import QuerySet
from django.http import Http404
from drf_spectacular.utils import extend_schema
from rest_framework import exceptions, status
from rest_framework.generics import ListAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from application.recruteur.services.get_recrutement import (
    get_recrutement,
)
from application.recruteur.services.list_candidatures import (
    list_candidatures_et_etapes,
)
from application.recruteur.usecases.change_etape_candidatures import (
    ChangeEtapeCandidaturesCommand,
)
from domain.commons.errors.organisme_errors import OrganismeNexistePas
from domain.identite.errors.organisme_permission_errors import (
    OrganismePermissionError,
)
from domain.recruteur.errors.recrutement_errors import (
    CandidatureInexistante,
    MotifRefusRequis,
    RecrutementEtapeInexistante,
    RecrutementInexistant,
)
from infrastructure.di.recruteur.recruteur_factory import recruteur_container
from infrastructure.django_apps.candidate.models.candidature import CandidatureModel
from infrastructure.django_apps.recruteur.models.etape import EtapeModel
from presentation.api.authentication import SessionApiMixin
from presentation.api.serializers import GenericErrorSerializer, TokenErrorSerializer
from presentation.commons.conditional_get import ConditionalGetMixin
from presentation.commons.pagination import PaginationSchemaDuSerializer
from presentation.recruteur.mappers import UtilisateurMapper
from presentation.recruteur.serializers import (
    CandidatureListeSerializer,
    ChangerEtapeCandidaturesSerializer,
    ChangerEtapeResultatSerializer,
    EtapeRecrutementModelSerializer,
    RecrutementDetailSerializer,
    RecrutementListeSerializer,
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
class RecrutementDetailView(ConditionalGetMixin, SessionApiMixin, APIView):
    def get(
        self, request: Request, organisme_uuid: UUID, recrutement_uuid: UUID
    ) -> Response:
        try:
            recrutement = get_recrutement(
                organisme_id=organisme_uuid,
                recrutement_id=recrutement_uuid,
                utilisateur=request.user,
            )
            return Response(RecrutementDetailSerializer(recrutement).data)
        except OrganismePermissionError:
            return Response(
                GenericErrorSerializer({"error": "Forbidden."}).data,
                status=status.HTTP_403_FORBIDDEN,
            )
        except (OrganismeNexistePas, RecrutementInexistant):
            return Response(
                GenericErrorSerializer({"error": "Not found."}).data,
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception:
            serializer = GenericErrorSerializer({"error": "Unexpected error"})
            return Response(
                serializer.data, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@extend_schema(
    summary="Détail d'un recrutement — vue liste (paginée)",
    tags=["recruteur"],
    responses={
        200: RecrutementListeSerializer,
        400: GenericErrorSerializer,
        401: TokenErrorSerializer,
        403: GenericErrorSerializer,
        404: GenericErrorSerializer,
        500: GenericErrorSerializer,
    },
)
class RecrutementListeView(ConditionalGetMixin, SessionApiMixin, ListAPIView):
    serializer_class = CandidatureListeSerializer
    pagination_class = PaginationSchemaDuSerializer
    etapes: list[EtapeModel]

    def get_queryset(self) -> QuerySet[CandidatureModel]:
        candidatures, self.etapes = list_candidatures_et_etapes(
            organisme_id=self.kwargs["organisme_uuid"],
            recrutement_id=self.kwargs["recrutement_uuid"],
            utilisateur=self.request.user,
        )
        return candidatures

    def get_paginated_response(self, data: list) -> Response:
        response = super().get_paginated_response(data)
        response.data["etapes"] = EtapeRecrutementModelSerializer(
            self.etapes, many=True
        ).data
        return response

    def handle_exception(self, exc: Exception) -> Response:
        if isinstance(exc, OrganismePermissionError):
            return Response(
                GenericErrorSerializer({"error": "Forbidden."}).data,
                status=status.HTTP_403_FORBIDDEN,
            )
        if isinstance(exc, (OrganismeNexistePas, RecrutementInexistant)):
            return Response(
                GenericErrorSerializer({"error": "Not found."}).data,
                status=status.HTTP_404_NOT_FOUND,
            )
        if isinstance(exc, (exceptions.APIException, Http404)):
            return super().handle_exception(exc)
        return Response(
            GenericErrorSerializer({"error": "Unexpected error"}).data,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
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
class RecrutementCandidaturesEtapeView(ConditionalGetMixin, SessionApiMixin, APIView):
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
            usecase = self.container.change_etape_candidatures_usecase()
            resultat = usecase.execute(
                ChangeEtapeCandidaturesCommand(
                    organisme_id=organisme_uuid,
                    recrutement_id=recrutement_uuid,
                    etape_cible_id=data["etape_cible_uuid"],
                    candidatures=[c["candidature_uuid"] for c in data["candidatures"]],
                    motif_refus=data.get("motif_refus"),
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
        except (RecrutementEtapeInexistante, MotifRefusRequis) as e:
            serializer = GenericErrorSerializer({"error": str(e)})
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response(
                {"error": "Unexpected error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
