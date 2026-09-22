from datetime import datetime, timedelta, timezone

from django.http import Http404
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import exceptions, status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from domain.commons.errors.organisme_errors import OrganismeNexistePas
from domain.recruteur.errors.recrutement_errors import (
    RecrutementCandidatureInexistante,
    RecrutementInexistant,
)
from infrastructure.django_apps.candidate.models.candidature import CandidatureModel
from infrastructure.django_apps.commons.models import AuditLogModel
from infrastructure.django_apps.recruteur.models.organisme import OrganismeModel
from infrastructure.django_apps.recruteur.models.recrutement import RecrutementModel
from infrastructure.factories.commons.audit_log_django_factory import (
    AuditLogDjangoFactory,
)
from presentation.api.serializers import GenericErrorSerializer, generic_response_format
from presentation.commons.pagination import PageNumberLimitPagination
from presentation.recruteur.serializers import AuditLogSerializer

_EVENEMENTS = [
    ("NoteAjoutee", "Camille", "Durand"),
    ("CandidatureEtapeModifiee", "Sami", "Benali"),
    ("NoteEditee", "Camille", "Durand"),
    ("NoteSupprimee", "Julie", "Petit"),
]


def _seed_log(
    *, occurred_at: datetime, event_name: str, prenom: str, nom: str
) -> AuditLogModel:
    log = AuditLogDjangoFactory.build(
        occurred_at=occurred_at,
        event_name=event_name,
        ressource_kind="CandidatureRecruteur",
    )
    log.utilisateur_prenom = prenom
    log.utilisateur_nom = nom
    return log


def _build_seed_logs() -> list[AuditLogModel]:
    now = datetime.now(tz=timezone.utc)
    logs = [
        _seed_log(
            occurred_at=now - timedelta(days=5),
            event_name="CandidatureRecue",
            prenom="Nadia",
            nom="Haddad",
        )
    ]
    for index, (event_name, prenom, nom) in enumerate(_EVENEMENTS, start=1):
        logs.append(
            _seed_log(
                occurred_at=now - timedelta(days=5 - index),
                event_name=event_name,
                prenom=prenom,
                nom=nom,
            )
        )
    return logs


@extend_schema_view(
    get=extend_schema(
        summary="Journal d'activité d'une candidature",
        tags=["recruteur"],
        responses={
            **generic_response_format,
            200: AuditLogSerializer(many=True),
            400: GenericErrorSerializer,
        },
    ),
)
class CandidatureLogsView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AuditLogSerializer
    pagination_class = PageNumberLimitPagination

    def get_queryset(self) -> list[AuditLogModel]:
        organisme_uuid = self.kwargs["organisme_uuid"]
        recrutement_uuid = self.kwargs["recrutement_uuid"]
        candidature_uuid = self.kwargs["candidature_uuid"]

        # TODO: guards to move in upcoming service
        if not OrganismeModel.objects.filter(id=organisme_uuid).exists():
            raise OrganismeNexistePas(str(organisme_uuid))
        if not RecrutementModel.objects.by_organisme_and_recrutement(
            organisme_uuid, recrutement_uuid
        ).exists():
            raise RecrutementInexistant(recrutement_uuid)
        if not CandidatureModel.objects.filter(
            id=candidature_uuid, etape__recrutement_id=recrutement_uuid
        ).exists():
            raise RecrutementCandidatureInexistante(candidature_uuid)

        return _build_seed_logs()

    def handle_exception(self, exc: Exception) -> Response:
        if isinstance(
            exc,
            (
                OrganismeNexistePas,
                RecrutementInexistant,
                RecrutementCandidatureInexistante,
            ),
        ):
            return Response(
                GenericErrorSerializer({"error": str(exc)}).data,
                status=status.HTTP_404_NOT_FOUND,
            )
        if isinstance(exc, (exceptions.APIException, Http404)):
            return super().handle_exception(exc)
        return Response(
            GenericErrorSerializer({"error": "Unexpected error"}).data,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
