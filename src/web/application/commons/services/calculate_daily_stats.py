from datetime import date

from django.db.models import QuerySet

from domain.recruteur.value_objects.roles import (
    AgentOrganismeRole,
    AgentRecrutementRole,
)
from infrastructure.django_apps.candidate.models.candidature import CandidatureModel
from infrastructure.django_apps.commons.enums import Metric
from infrastructure.django_apps.commons.models import StatSnapshotModel
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


def _volume_querysets() -> dict[Metric, QuerySet]:
    # TODO: recrutements, candidatures et membres d'un organisme supprimé sont
    # comptés, contrairement à nb_organismes_ouverts (PR #2339).
    organisme_agents = OrganismeAgentModel.objects.active()
    recrutement_agents = RecrutementAgentModel.objects.active()
    return {
        Metric.RECEIVED_APPLICATIONS: CandidatureModel.objects.received(),
        Metric.WITHDRAWN_APPLICATIONS: CandidatureModel.objects.withdrawn(),
        Metric.APPLICATIONS_TO_PROCESS: CandidatureModel.objects.to_process(),
        Metric.PROCESSED_APPLICATIONS: CandidatureModel.objects.processed(),
        Metric.APPLICATIONS_SHORTLISTED: CandidatureModel.objects.shortlisted(),
        Metric.REFUSED_APPLICATIONS: CandidatureModel.objects.refused(),
        Metric.SELECTED_APPLICATIONS: CandidatureModel.objects.selected(),
        Metric.RECRUTEMENTS: RecrutementModel.objects.all(),
        Metric.OPEN_ORGANISMES: OrganismeModel.objects.open(),
        Metric.ORGANISME_SUPERVISEURS: organisme_agents.filter(
            role=AgentOrganismeRole.SUPERVISEUR.value
        ),
        Metric.ORGANISME_AGENTS: organisme_agents.filter(
            role=AgentOrganismeRole.AGENT.value
        ),
        Metric.RECRUTEMENT_RESPONSABLES: recrutement_agents.filter(
            role=AgentRecrutementRole.RESPONSABLE.value
        ),
        Metric.RECRUTEMENT_RECRUTEURS: recrutement_agents.filter(
            role=AgentRecrutementRole.RECRUTEUR.value
        ),
        Metric.RECRUTEMENT_CONTRIBUTEURS: recrutement_agents.filter(
            role=AgentRecrutementRole.CONTRIBUTEUR.value
        ),
        Metric.CANDIDAT_ACCOUNTS: ProfilCandidatModel.objects.all(),
    }


def _volume_metrics() -> dict[Metric, int]:
    return {
        metric: queryset.count() for metric, queryset in _volume_querysets().items()
    }


def calculate_daily_stats(target_date: date) -> None:
    metrics = _offer_metrics() | _volume_metrics()
    StatSnapshotModel.objects.bulk_create(
        [
            StatSnapshotModel(date=target_date, metric_name=name, metric_value=value)
            for name, value in metrics.items()
        ],
        update_conflicts=True,
        unique_fields=["date", "metric_name"],
        update_fields=["metric_value", "updated_at"],
    )
