from datetime import UTC, date, datetime, timedelta

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
from infrastructure.django_apps.recruteur.enums.etape_par_defaut import EtapeParDefaut
from infrastructure.factories.candidate.candidature_django_factory import (
    CandidatureDjangoFactory,
)
from infrastructure.factories.candidate.document_django_factory import (
    DocumentDjangoFactory,
)
from infrastructure.factories.identite.candidat_django_factory import (
    CandidatDjangoFactory,
)
from infrastructure.factories.identite.organisme_django_factory import (
    OrganismeAgentDjangoFactory,
    OrganismeDjangoFactory,
)
from infrastructure.factories.messagerie.conversation_django_factory import (
    ConversationDjangoFactory,
    MessageDjangoFactory,
    MessageDocumentDjangoFactory,
)
from infrastructure.factories.recruteur.note_django_factory import NoteDjangoFactory
from infrastructure.factories.recruteur.recrutement_django_factory import (
    EtapeDjangoFactory,
    RecrutementAgentDjangoFactory,
    RecrutementDjangoFactory,
)
from infrastructure.factories.referentiel.offer_django_factory import (
    OfferDjangoFactory,
)
from infrastructure.factories.tag.tag_django_factory import (
    CandidatureTagDjangoFactory,
    NoteTagDjangoFactory,
    RecrutementAgentTagDjangoFactory,
    TagDjangoFactory,
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
        Metric.APPLICATIONS_SHORTLISTED,
        Metric.REFUSED_APPLICATIONS,
        Metric.SELECTED_APPLICATIONS,
    ) == {
        Metric.RECEIVED_APPLICATIONS: 6,
        Metric.WITHDRAWN_APPLICATIONS: 1,
        Metric.APPLICATIONS_TO_PROCESS: 2,
        Metric.PROCESSED_APPLICATIONS: 3,
        Metric.APPLICATIONS_SHORTLISTED: 2,
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


@pytest.fixture
def screened(recrutement):
    return create_candidature(recrutement, CategorieEtapeRecrutement.EN_COURS)


@pytest.fixture
def unscreened(recrutement):
    return create_candidature(recrutement, CategorieEtapeRecrutement.ENTREE)


def test_stores_note_counts(screened, unscreened):
    NoteDjangoFactory(candidature=screened)
    NoteDjangoFactory(candidature=screened)
    NoteDjangoFactory(candidature=unscreened)
    NoteDjangoFactory(candidature=screened, est_privee=True)
    NoteDjangoFactory(candidature=screened, supprimee_le=datetime.now(UTC))

    calculate_daily_stats(TARGET_DATE)

    assert values_of(
        Metric.TEAM_NOTES,
        Metric.PERSONAL_NOTES,
        Metric.SCREENED_APPLICATIONS_WITH_TEAM_NOTE,
    ) == {
        Metric.TEAM_NOTES: 3,
        Metric.PERSONAL_NOTES: 1,
        Metric.SCREENED_APPLICATIONS_WITH_TEAM_NOTE: 1,
    }


def test_stores_message_counts(screened, unscreened):
    screened_conversation = ConversationDjangoFactory(candidature=screened)
    MessageDjangoFactory(conversation=screened_conversation)
    MessageDjangoFactory(conversation=screened_conversation)
    MessageDjangoFactory(conversation=screened_conversation, par_candidat=True)
    MessageDjangoFactory(
        conversation=ConversationDjangoFactory(candidature=unscreened),
        par_candidat=True,
    )

    calculate_daily_stats(TARGET_DATE)

    assert values_of(
        Metric.TEAM_MESSAGES,
        Metric.CANDIDAT_MESSAGES,
        Metric.SCREENED_APPLICATIONS_WITH_TEAM_MESSAGE,
    ) == {
        Metric.TEAM_MESSAGES: 2,
        Metric.CANDIDAT_MESSAGES: 2,
        Metric.SCREENED_APPLICATIONS_WITH_TEAM_MESSAGE: 1,
    }


def test_stores_conversation_counts(screened, unscreened):
    ConversationDjangoFactory(candidature=screened)
    ConversationDjangoFactory(candidature=screened)
    ConversationDjangoFactory(candidature=unscreened)

    calculate_daily_stats(TARGET_DATE)

    assert values_of(
        Metric.CONVERSATIONS,
        Metric.APPLICATIONS_WITH_CONVERSATION,
        Metric.APPLICATIONS_WITH_SEVERAL_CONVERSATIONS,
    ) == {
        Metric.CONVERSATIONS: 3,
        Metric.APPLICATIONS_WITH_CONVERSATION: 2,
        Metric.APPLICATIONS_WITH_SEVERAL_CONVERSATIONS: 1,
    }


def candidat_user(candidature):
    return candidature.candidat.utilisateur


def test_stores_document_counts(recrutement, screened, unscreened):
    DocumentDjangoFactory(candidature=screened, depose_par=candidat_user(screened))
    DocumentDjangoFactory(candidature=unscreened)
    with_attachment = create_candidature(
        recrutement, CategorieEtapeRecrutement.EN_COURS
    )
    MessageDocumentDjangoFactory(
        message=MessageDjangoFactory(
            conversation=ConversationDjangoFactory(candidature=with_attachment),
            par_candidat=True,
        ),
        document__depose_par=candidat_user(with_attachment),
    )

    calculate_daily_stats(TARGET_DATE)

    assert values_of(
        Metric.DOCUMENTS_ADDED_BY_MEMBER,
        Metric.CANDIDAT_ATTACHMENTS,
        Metric.SCREENED_APPLICATIONS_WITH_COMPLETED_FILE,
    ) == {
        Metric.DOCUMENTS_ADDED_BY_MEMBER: 1,
        Metric.CANDIDAT_ATTACHMENTS: 1,
        Metric.SCREENED_APPLICATIONS_WITH_COMPLETED_FILE: 1,
    }


def test_member_document_completes_screened_application_file(screened):
    DocumentDjangoFactory(candidature=screened)

    calculate_daily_stats(TARGET_DATE)

    assert values_of(Metric.SCREENED_APPLICATIONS_WITH_COMPLETED_FILE) == {
        Metric.SCREENED_APPLICATIONS_WITH_COMPLETED_FILE: 1
    }


def create_tag(*, days_old):
    tag = TagDjangoFactory()
    tag.created_at = datetime.combine(
        TARGET_DATE - timedelta(days=days_old), datetime.min.time(), tzinfo=UTC
    )
    tag.save(update_fields=["created_at"])
    return tag


def test_stores_tag_counts(screened):
    create_tag(days_old=10)
    create_tag(days_old=31)
    used_old_tag = create_tag(days_old=31)
    CandidatureTagDjangoFactory(candidature=screened, tag=used_old_tag)

    calculate_daily_stats(TARGET_DATE)

    assert values_of(Metric.TAGS, Metric.OLD_TAGS, Metric.OLD_UNUSED_TAGS) == {
        Metric.TAGS: 3,
        Metric.OLD_TAGS: 2,
        Metric.OLD_UNUSED_TAGS: 1,
    }


def test_stores_tagged_item_counts(recrutement, screened):
    CandidatureTagDjangoFactory(candidature=screened)
    CandidatureTagDjangoFactory(candidature=screened)
    NoteTagDjangoFactory(note=NoteDjangoFactory(candidature=screened))
    NoteTagDjangoFactory(
        note=NoteDjangoFactory(candidature=screened, supprimee_le=datetime.now(UTC))
    )
    RecrutementAgentTagDjangoFactory(
        recrutement_agent=RecrutementAgentDjangoFactory(recrutement=recrutement)
    )
    RecrutementAgentTagDjangoFactory(
        recrutement_agent=RecrutementAgentDjangoFactory(
            recrutement=recrutement, date_revocation=datetime.now(UTC)
        )
    )

    calculate_daily_stats(TARGET_DATE)

    assert values_of(
        Metric.TAGGED_APPLICATIONS, Metric.TAGGED_NOTES, Metric.MEMBERS_WITH_FUNCTION
    ) == {
        Metric.TAGGED_APPLICATIONS: 1,
        Metric.TAGGED_NOTES: 1,
        Metric.MEMBERS_WITH_FUNCTION: 1,
    }


def test_stores_open_organismes_with_tag(db):
    open_organisme = OrganismeDjangoFactory(gestion_ats=True)
    TagDjangoFactory.create_batch(2, organisme=open_organisme)
    OrganismeDjangoFactory(gestion_ats=True)
    TagDjangoFactory(organisme=OrganismeDjangoFactory(gestion_ats=False))

    calculate_daily_stats(TARGET_DATE)

    assert values_of(Metric.ORGANISMES_WITH_TAG) == {Metric.ORGANISMES_WITH_TAG: 1}


def test_stores_recrutements_without_responsable(db):
    with_responsable = RecrutementDjangoFactory(agent_link=None)
    RecrutementAgentDjangoFactory(
        recrutement=with_responsable, role=AgentRecrutementRole.RESPONSABLE.value
    )
    revoked_responsable = RecrutementDjangoFactory(agent_link=None)
    RecrutementAgentDjangoFactory(
        recrutement=revoked_responsable,
        role=AgentRecrutementRole.RESPONSABLE.value,
        date_revocation=datetime.now(UTC),
    )
    RecrutementDjangoFactory()

    calculate_daily_stats(TARGET_DATE)

    assert values_of(Metric.RECRUTEMENTS_WITHOUT_RESPONSABLE) == {
        Metric.RECRUTEMENTS_WITHOUT_RESPONSABLE: 2
    }


def open_organisme_with_process(names=None):
    organisme = OrganismeDjangoFactory(gestion_ats=True)
    organisme.initialize_default_etapes()
    if names is not None:
        organisme.etapes = [
            {**etape, "nom": nom}
            for etape, nom in zip(organisme.etapes, names, strict=True)
        ]
    organisme.save(update_fields=["etapes"])
    return organisme


def recrutement_with_process(organisme, process):
    recrutement = RecrutementDjangoFactory(organisme=organisme, etapes=[])
    etapes = [
        EtapeDjangoFactory(recrutement=recrutement, categorie=categorie, nom=nom)
        for categorie, nom in process
    ]
    recrutement.ordre_etapes = [str(etape.id) for etape in etapes]
    recrutement.save(update_fields=["ordre_etapes"])
    return recrutement


DEFAULT_PROCESS = [(etape.categorie.value, etape.nom) for etape in EtapeParDefaut]


def test_stores_custom_process_organismes(db):
    open_organisme_with_process()
    open_organisme_with_process(names=["Dépôt", *[e.nom for e in EtapeParDefaut][1:]])
    OrganismeDjangoFactory(gestion_ats=True)

    calculate_daily_stats(TARGET_DATE)

    assert values_of(Metric.CUSTOM_PROCESS_ORGANISMES) == {
        Metric.CUSTOM_PROCESS_ORGANISMES: 1
    }


def test_stores_custom_process_recrutements(db):
    organisme = open_organisme_with_process()
    recrutement_with_process(organisme, DEFAULT_PROCESS)
    recrutement_with_process(organisme, list(reversed(DEFAULT_PROCESS)))
    recrutement_with_process(organisme, DEFAULT_PROCESS[:-1])
    recrutement_with_process(OrganismeDjangoFactory(), DEFAULT_PROCESS)

    calculate_daily_stats(TARGET_DATE)

    assert values_of(Metric.CUSTOM_PROCESS_RECRUTEMENTS) == {
        Metric.CUSTOM_PROCESS_RECRUTEMENTS: 2
    }
