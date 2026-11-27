from datetime import datetime, timedelta, timezone

from django.http import Http404
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import exceptions, status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from application.recruteur.context_services.candidature_agent_service import (
    CandidatureAgentService,
)
from application.recruteur.errors.application_errors_recruteur import (
    CandidatureInaccessible,
)
from infrastructure.django_apps.commons.models import AuditLogModel
from infrastructure.factories.commons.audit_log_django_factory import (
    AuditLogDjangoFactory,
)
from presentation.api.authentication import SessionApiMixin
from presentation.api.serializers import GenericErrorSerializer, generic_response_format
from presentation.commons.conditional_get import ConditionalGetMixin
from presentation.commons.pagination import PageNumberLimitPagination
from presentation.recruteur.serializers import AuditLogSerializer
from presentation.recruteur.views.candidature_inaccessible import (
    candidature_inaccessible_response,
)

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
class CandidatureLogsView(ConditionalGetMixin, SessionApiMixin, ListAPIView):
    serializer_class = AuditLogSerializer
    pagination_class = PageNumberLimitPagination

    def get_queryset(self) -> list[AuditLogModel]:
        organisme_uuid = self.kwargs["organisme_uuid"]
        recrutement_uuid = self.kwargs["recrutement_uuid"]
        candidature_uuid = self.kwargs["candidature_uuid"]

        CandidatureAgentService(
            organisme_id=organisme_uuid,
            recrutement_id=recrutement_uuid,
            candidature_id=candidature_uuid,
            utilisateur=self.request.user,
        ).check_exists()

        return _build_seed_logs()

    def handle_exception(self, exc: Exception) -> Response:
        if isinstance(exc, CandidatureInaccessible):
            return candidature_inaccessible_response()
        if isinstance(exc, (exceptions.APIException, Http404)):
            return super().handle_exception(exc)
        return Response(
            GenericErrorSerializer({"error": "Unexpected error"}).data,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
