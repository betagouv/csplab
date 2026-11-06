from datetime import date

from django.db import transaction
from django.db.models import Count, QuerySet

from domain.recruteur.value_objects.roles import (
    AgentOrganismeRole,
    AgentRecrutementRole,
)
from infrastructure.django_apps.candidate.models.candidature import CandidatureModel
from infrastructure.django_apps.candidate.models.document import DocumentModel
from infrastructure.django_apps.commons.enums import Metric
from infrastructure.django_apps.commons.models import StatSnapshotModel
from infrastructure.django_apps.messagerie.models import (
    ConversationModel,
    MessageModel,
)
from infrastructure.django_apps.recruteur.models.note import NoteModel
from infrastructure.django_apps.recruteur.models.organisme import (
    OrganismeAgentModel,
    OrganismeModel,
)
from infrastructure.django_apps.recruteur.models.recrutement import (
    RecrutementAgentModel,
    RecrutementModel,
)
from infrastructure.django_apps.referentiel.models.offer import OfferModel
from infrastructure.django_apps.users.models import ProfilCandidatModel


def _offer_metrics() -> dict[Metric, int]:
    return {
        Metric.PUBLISHED_OFFERS: OfferModel.objects.actives().count(),
        Metric.ARCHIVED_OFFERS: OfferModel.objects.archived().count(),
    }


def _volume_metrics() -> dict[Metric, int]:
    candidatures = CandidatureModel.objects
    organisme_agents = OrganismeAgentModel.objects.active()
    recrutement_agents = RecrutementAgentModel.objects.active()
    return {
        Metric.RECEIVED_APPLICATIONS: candidatures.received().count(),
        Metric.WITHDRAWN_APPLICATIONS: candidatures.withdrawn().count(),
        Metric.APPLICATIONS_TO_PROCESS: candidatures.to_process().count(),
        Metric.PROCESSED_APPLICATIONS: candidatures.processed().count(),
        Metric.APPLICATIONS_PAST_FIRST_SCREENING: (
            candidatures.past_first_screening().count()
        ),
        Metric.REFUSED_APPLICATIONS: candidatures.refused().count(),
        Metric.SELECTED_APPLICATIONS: candidatures.selected().count(),
        Metric.RECRUTEMENTS: RecrutementModel.objects.count(),
        Metric.OPEN_ORGANISMES: OrganismeModel.objects.open().count(),
        Metric.ORGANISME_SUPERVISEURS: organisme_agents.filter(
            role=AgentOrganismeRole.SUPERVISEUR.value
        ).count(),
        Metric.ORGANISME_AGENTS: organisme_agents.filter(
            role=AgentOrganismeRole.AGENT.value
        ).count(),
        Metric.RECRUTEMENT_RESPONSABLES: recrutement_agents.filter(
            role=AgentRecrutementRole.RESPONSABLE.value
        ).count(),
        Metric.RECRUTEMENT_RECRUTEURS: recrutement_agents.filter(
            role=AgentRecrutementRole.RECRUTEUR.value
        ).count(),
        Metric.RECRUTEMENT_CONTRIBUTEURS: recrutement_agents.filter(
            role=AgentRecrutementRole.CONTRIBUTEUR.value
        ).count(),
        Metric.CANDIDAT_ACCOUNTS: ProfilCandidatModel.objects.count(),
    }


def _count_candidatures(
    queryset: QuerySet, candidature_field: str = "candidature_id"
) -> int:
    return queryset.values(candidature_field).distinct().count()


def _collaboration_metrics() -> dict[Metric, int]:
    screened = CandidatureModel.objects.past_first_screening()
    team_notes = NoteModel.objects.for_team()
    team_messages = MessageModel.objects.by_team()
    conversations_per_candidature = (
        ConversationModel.objects.order_by()
        .values("candidature_id")
        .annotate(total=Count("pk"))
    )
    return {
        Metric.TEAM_NOTES: team_notes.count(),
        Metric.PERSONAL_NOTES: NoteModel.objects.personal().count(),
        Metric.SCREENED_APPLICATIONS_WITH_TEAM_NOTE: _count_candidatures(
            team_notes.filter(candidature__in=screened)
        ),
        Metric.TEAM_MESSAGES: team_messages.count(),
        Metric.CANDIDAT_MESSAGES: MessageModel.objects.by_candidat().count(),
        Metric.SCREENED_APPLICATIONS_WITH_TEAM_MESSAGE: _count_candidatures(
            team_messages.filter(conversation__candidature__in=screened),
            "conversation__candidature_id",
        ),
        Metric.CONVERSATIONS: ConversationModel.objects.count(),
        Metric.CONVERSATIONS_OPENED_BY_CANDIDAT: (
            ConversationModel.objects.opened_by_candidat().count()
        ),
        Metric.APPLICATIONS_WITH_CONVERSATION: conversations_per_candidature.count(),
        Metric.APPLICATIONS_WITH_SEVERAL_CONVERSATIONS: (
            conversations_per_candidature.filter(total__gte=2).count()
        ),
        Metric.DOCUMENTS_ADDED_BY_MEMBER: (
            DocumentModel.objects.added_by_member().count()
        ),
        Metric.CANDIDAT_ATTACHMENTS: (
            DocumentModel.objects.candidat_attachments().count()
        ),
        Metric.SCREENED_APPLICATIONS_WITH_COMPLETED_FILE: _count_candidatures(
            DocumentModel.objects.added_in_tool().filter(candidature__in=screened)
        ),
    }


def calculate_daily_stats(target_date: date) -> None:
    metrics = _offer_metrics() | _volume_metrics() | _collaboration_metrics()
    with transaction.atomic():
        StatSnapshotModel.objects.bulk_create(
            [
                StatSnapshotModel(
                    date=target_date, metric_name=name, metric_value=value
                )
                for name, value in metrics.items()
            ],
            update_conflicts=True,
            unique_fields=["date", "metric_name"],
            update_fields=["metric_value", "updated_at"],
        )
