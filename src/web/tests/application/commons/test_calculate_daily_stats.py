from datetime import UTC, date, datetime

import pytest

from application.commons.services.calculate_daily_stats import calculate_daily_stats
from domain.candidate.value_objects.statut_candidature import StatutCandidature
from domain.recruteur.value_objects.categorie_etapes_recrutement import (
    CategorieEtapeRecrutement,
)
from domain.recruteur.value_objects.roles import (
    AgentOrganismeRole,
    AgentRecrutementRole,
)
from infrastructure.django_apps.commons.enums import Metric
from infrastructure.django_apps.commons.models import StatSnapshotModel
from infrastructure.factories.candidate.candidature_django_factory import (
    CandidatureDjangoFactory,
)
from infrastructure.factories.identite.candidat_django_factory import (
    CandidatDjangoFactory,
)
from infrastructure.factories.identite.organisme_django_factory import (
    OrganismeAgentDjangoFactory,
    OrganismeDjangoFactory,
)
from infrastructure.factories.recruteur.recrutement_django_factory import (
    EtapeDjangoFactory,
    RecrutementAgentDjangoFactory,
    RecrutementDjangoFactory,
)
from infrastructure.factories.referentiel.offer_django_factory import (
    OfferDjangoFactory,
)

TARGET_DATE = date(2026, 6, 30)


def snapshot_values(target_date: date = TARGET_DATE) -> dict[str, int]:
    return dict(
        StatSnapshotModel.objects.filter(date=target_date).values_list(
            "metric_name", "metric_value"
        )
    )


def values_of(*metrics: Metric) -> dict[str, int]:
    values = snapshot_values()
    return {metric.value: values[metric] for metric in metrics}


OFFER_METRICS = (Metric.PUBLISHED_OFFERS, Metric.ARCHIVED_OFFERS)


def test_stores_every_metric(db):
    calculate_daily_stats(TARGET_DATE)

    assert snapshot_values() == {metric.value: 0 for metric in Metric}


def test_stores_offer_counts(db):
    OfferDjangoFactory.create_batch(3)
    OfferDjangoFactory.create_batch(2, archived_at=datetime.now(UTC))

    calculate_daily_stats(TARGET_DATE)

    assert values_of(*OFFER_METRICS) == {
        Metric.PUBLISHED_OFFERS: 3,
        Metric.ARCHIVED_OFFERS: 2,
    }


def test_rerun_for_same_date_replaces_values(db):
    calculate_daily_stats(TARGET_DATE)
    OfferDjangoFactory.create_batch(4)

    calculate_daily_stats(TARGET_DATE)

    assert values_of(*OFFER_METRICS) == {
        Metric.PUBLISHED_OFFERS: 4,
        Metric.ARCHIVED_OFFERS: 0,
    }


def test_keeps_snapshots_of_other_dates(db):
    other_date = date(2026, 6, 29)
    StatSnapshotModel.objects.create(
        date=other_date, metric_name=Metric.PUBLISHED_OFFERS, metric_value=7
    )

    calculate_daily_stats(TARGET_DATE)

    assert snapshot_values(other_date) == {Metric.PUBLISHED_OFFERS: 7}


@pytest.fixture
def recrutement(db):
    return RecrutementDjangoFactory(etapes=[], agent_link=None)


def create_candidature(recrutement, categorie, statut=StatutCandidature.SOUMISE):
    etape = EtapeDjangoFactory(recrutement=recrutement, categorie=categorie.value)
    return CandidatureDjangoFactory(etape=etape, statut=statut.value)


def test_stores_application_counts(recrutement):
    create_candidature(
        recrutement, CategorieEtapeRecrutement.ENTREE, StatutCandidature.INITIAL
    )
    create_candidature(recrutement, CategorieEtapeRecrutement.ENTREE)
    create_candidature(recrutement, CategorieEtapeRecrutement.ENTREE)
    create_candidature(recrutement, CategorieEtapeRecrutement.EN_COURS)
    create_candidature(recrutement, CategorieEtapeRecrutement.ACCEPTE)
    create_candidature(recrutement, CategorieEtapeRecrutement.REFUS)
    create_candidature(
        recrutement, CategorieEtapeRecrutement.ENTREE, StatutCandidature.RETIREE
    )

    calculate_daily_stats(TARGET_DATE)

    assert values_of(
        Metric.RECEIVED_APPLICATIONS,
        Metric.WITHDRAWN_APPLICATIONS,
        Metric.APPLICATIONS_TO_PROCESS,
        Metric.PROCESSED_APPLICATIONS,
        Metric.APPLICATIONS_PAST_FIRST_SCREENING,
        Metric.REFUSED_APPLICATIONS,
        Metric.SELECTED_APPLICATIONS,
    ) == {
        Metric.RECEIVED_APPLICATIONS: 6,
        Metric.WITHDRAWN_APPLICATIONS: 1,
        Metric.APPLICATIONS_TO_PROCESS: 2,
        Metric.PROCESSED_APPLICATIONS: 3,
        Metric.APPLICATIONS_PAST_FIRST_SCREENING: 2,
        Metric.REFUSED_APPLICATIONS: 1,
        Metric.SELECTED_APPLICATIONS: 1,
    }


def test_stores_recrutement_and_organisme_counts(recrutement):
    OrganismeDjangoFactory(gestion_ats=True)
    OrganismeDjangoFactory(gestion_ats=True, supprime_le=datetime.now(UTC))
    OrganismeDjangoFactory(gestion_ats=False)

    calculate_daily_stats(TARGET_DATE)

    assert values_of(Metric.RECRUTEMENTS, Metric.OPEN_ORGANISMES) == {
        Metric.RECRUTEMENTS: 1,
        Metric.OPEN_ORGANISMES: 1,
    }


def test_stores_active_members_by_role(recrutement):
    OrganismeAgentDjangoFactory(role=AgentOrganismeRole.SUPERVISEUR.value)
    OrganismeAgentDjangoFactory(role=AgentOrganismeRole.AGENT.value)
    OrganismeAgentDjangoFactory(
        role=AgentOrganismeRole.AGENT.value, date_revocation=datetime.now(UTC)
    )
    for role in AgentRecrutementRole:
        RecrutementAgentDjangoFactory(recrutement=recrutement, role=role.value)
    RecrutementAgentDjangoFactory(
        recrutement=recrutement,
        role=AgentRecrutementRole.CONTRIBUTEUR.value,
        date_revocation=datetime.now(UTC),
    )

    calculate_daily_stats(TARGET_DATE)

    assert values_of(
        Metric.ORGANISME_SUPERVISEURS,
        Metric.ORGANISME_AGENTS,
        Metric.RECRUTEMENT_RESPONSABLES,
        Metric.RECRUTEMENT_RECRUTEURS,
        Metric.RECRUTEMENT_CONTRIBUTEURS,
    ) == {
        Metric.ORGANISME_SUPERVISEURS: 1,
        Metric.ORGANISME_AGENTS: 1,
        Metric.RECRUTEMENT_RESPONSABLES: 1,
        Metric.RECRUTEMENT_RECRUTEURS: 1,
        Metric.RECRUTEMENT_CONTRIBUTEURS: 1,
    }


def test_stores_candidat_accounts(db):
    CandidatDjangoFactory.create_batch(2)

    calculate_daily_stats(TARGET_DATE)

    assert values_of(Metric.CANDIDAT_ACCOUNTS) == {Metric.CANDIDAT_ACCOUNTS: 2}
