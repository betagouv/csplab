from uuid import uuid4

import pytest
from django.utils import timezone

from application.recruteur.services.set_recrutements_responsable import (
    set_recrutements_responsable,
)
from domain.commons.errors.organisme_errors import OrganismeNexistePas
from domain.identite.errors.agent_errors import ProfilAgentNexistePas
from domain.identite.errors.organisme_permission_errors import AccesOrganismeRefuse
from domain.recruteur.value_objects.roles import (
    AgentOrganismeRole,
    AgentRecrutementRole,
)
from infrastructure.django_apps.recruteur.models.organisme import OrganismeAgentModel
from infrastructure.django_apps.recruteur.models.recrutement import (
    RecrutementAgentModel,
)
from infrastructure.factories.identite.agent_django_factory import AgentDjangoFactory
from infrastructure.factories.identite.organisme_django_factory import (
    OrganismeAgentDjangoFactory,
    OrganismeDjangoFactory,
    create_organisme_with_agent,
)
from infrastructure.factories.identite.utilisateur_factory import UtilisateurFactory
from infrastructure.factories.recruteur.recrutement_django_factory import (
    RecrutementAgentDjangoFactory,
    RecrutementDjangoFactory,
)
from infrastructure.repositories.commons.postgres_audit_log_repository import (
    PostgresAuditLogRepository,
)


def _utilisateur(entity_id, *, is_staff=False):
    return UtilisateurFactory.create_entity(entity_id=entity_id, is_staff=is_staff)


def test_returns_reussite_for_each_recrutement_belonging_to_organisme(db):
    responsable, organisme = create_organisme_with_agent(
        role=AgentOrganismeRole.SUPERVISEUR
    )
    membre = OrganismeAgentDjangoFactory(
        organisme=organisme, role=AgentOrganismeRole.AGENT.value
    ).agent
    recrutements = [RecrutementDjangoFactory(organisme=organisme) for _ in range(3)]

    resultats = set_recrutements_responsable(
        organisme_id=organisme.id,
        recrutement_ids=[r.pk for r in recrutements],
        agent_id=membre.utilisateur_id,
        utilisateur=_utilisateur(responsable.utilisateur_id),
    )

    assert resultats["reussites"] == [r.pk for r in recrutements]
    assert resultats["echecs"] == []
    for recrutement in recrutements:
        recrutement_agent = RecrutementAgentModel.objects.get(
            recrutement_id=recrutement.pk, agent_id=membre.utilisateur_id
        )
        assert recrutement_agent.role == AgentRecrutementRole.RESPONSABLE.value
        assert recrutement_agent.date_revocation is None
        logs = PostgresAuditLogRepository().get_logs_for_ressource(
            "RecrutementAgent", recrutement.pk
        )
        assert len(logs) == 1
        assert logs[0].event_name == "AgentRecrutementAjoute"
        assert logs[0].utilisateur_id == responsable.utilisateur_id


def test_staff_bypasses_role_check(db):
    organisme = OrganismeDjangoFactory()
    membre = OrganismeAgentDjangoFactory(
        organisme=organisme, role=AgentOrganismeRole.AGENT.value
    ).agent
    recrutement = RecrutementDjangoFactory(organisme=organisme)

    resultats = set_recrutements_responsable(
        organisme_id=organisme.id,
        recrutement_ids=[recrutement.pk],
        agent_id=membre.utilisateur_id,
        utilisateur=_utilisateur(uuid4(), is_staff=True),
    )

    assert resultats["reussites"] == [recrutement.pk]


@pytest.mark.parametrize(
    "role", [AgentOrganismeRole.AGENT, None], ids=["membre_role", "no_organisme_role"]
)
def test_denied_when_demandeur_is_not_superviseur(db, role):
    if role is None:
        organisme = OrganismeDjangoFactory()
        demandeur_id = uuid4()
    else:
        demandeur, organisme = create_organisme_with_agent(role=role)
        demandeur_id = demandeur.utilisateur_id
    membre = OrganismeAgentDjangoFactory(
        organisme=organisme, role=AgentOrganismeRole.AGENT.value
    ).agent
    recrutement = RecrutementDjangoFactory(organisme=organisme)

    with pytest.raises(AccesOrganismeRefuse):
        set_recrutements_responsable(
            organisme_id=organisme.id,
            recrutement_ids=[recrutement.pk],
            agent_id=membre.utilisateur_id,
            utilisateur=_utilisateur(demandeur_id),
        )


def test_denied_for_superviseur_of_another_organisme(db):
    _, organisme = create_organisme_with_agent(role=AgentOrganismeRole.SUPERVISEUR)
    autre_superviseur, _ = create_organisme_with_agent(
        role=AgentOrganismeRole.SUPERVISEUR
    )
    membre = OrganismeAgentDjangoFactory(
        organisme=organisme, role=AgentOrganismeRole.AGENT.value
    ).agent
    recrutement = RecrutementDjangoFactory(organisme=organisme)

    with pytest.raises(AccesOrganismeRefuse):
        set_recrutements_responsable(
            organisme_id=organisme.id,
            recrutement_ids=[recrutement.pk],
            agent_id=membre.utilisateur_id,
            utilisateur=_utilisateur(autre_superviseur.utilisateur_id),
        )


def test_raises_when_organisme_does_not_exist(db):
    membre = AgentDjangoFactory()

    with pytest.raises(OrganismeNexistePas):
        set_recrutements_responsable(
            organisme_id=uuid4(),
            recrutement_ids=[uuid4()],
            agent_id=membre.utilisateur_id,
            utilisateur=_utilisateur(uuid4()),
        )


def test_raises_when_agent_does_not_exist(db):
    responsable, organisme = create_organisme_with_agent(
        role=AgentOrganismeRole.SUPERVISEUR
    )
    recrutement = RecrutementDjangoFactory(organisme=organisme)

    with pytest.raises(ProfilAgentNexistePas):
        set_recrutements_responsable(
            organisme_id=organisme.id,
            recrutement_ids=[recrutement.pk],
            agent_id=uuid4(),
            utilisateur=_utilisateur(responsable.utilisateur_id),
        )


def test_does_not_raise_when_agent_has_profile_but_is_not_attached_to_organisme(db):
    responsable, organisme = create_organisme_with_agent(
        role=AgentOrganismeRole.SUPERVISEUR
    )
    bare_agent = AgentDjangoFactory()
    recrutement = RecrutementDjangoFactory(organisme=organisme)

    resultats = set_recrutements_responsable(
        organisme_id=organisme.id,
        recrutement_ids=[recrutement.pk],
        agent_id=bare_agent.utilisateur_id,
        utilisateur=_utilisateur(responsable.utilisateur_id),
    )

    assert resultats["reussites"] == [recrutement.pk]
    organisme_agent = OrganismeAgentModel.objects.get(
        organisme_id=organisme.id, agent_id=bare_agent.utilisateur_id
    )
    assert organisme_agent.role == AgentOrganismeRole.AGENT.value
    assert organisme_agent.date_revocation is None


def test_reattaches_agent_previously_revoked_from_organisme(db):
    responsable, organisme = create_organisme_with_agent(
        role=AgentOrganismeRole.SUPERVISEUR
    )
    membre = OrganismeAgentDjangoFactory(
        organisme=organisme,
        role=AgentOrganismeRole.SUPERVISEUR.value,
        date_revocation=timezone.now(),
    ).agent
    recrutement = RecrutementDjangoFactory(organisme=organisme)

    resultats = set_recrutements_responsable(
        organisme_id=organisme.id,
        recrutement_ids=[recrutement.pk],
        agent_id=membre.utilisateur_id,
        utilisateur=_utilisateur(responsable.utilisateur_id),
    )

    assert resultats["reussites"] == [recrutement.pk]
    organisme_agent = OrganismeAgentModel.objects.get(
        organisme_id=organisme.id, agent_id=membre.utilisateur_id
    )
    assert organisme_agent.role == AgentOrganismeRole.AGENT.value
    assert organisme_agent.date_revocation is None


def test_upgrades_existing_membership_to_responsable(db):
    responsable, organisme = create_organisme_with_agent(
        role=AgentOrganismeRole.SUPERVISEUR
    )
    membre = OrganismeAgentDjangoFactory(
        organisme=organisme, role=AgentOrganismeRole.AGENT.value
    ).agent
    recrutement = RecrutementDjangoFactory(organisme=organisme)
    existant = RecrutementAgentDjangoFactory(
        recrutement=recrutement,
        agent=membre,
        role=AgentRecrutementRole.CONTRIBUTEUR.value,
    )

    resultats = set_recrutements_responsable(
        organisme_id=organisme.id,
        recrutement_ids=[recrutement.pk],
        agent_id=membre.utilisateur_id,
        utilisateur=_utilisateur(responsable.utilisateur_id),
    )

    assert resultats["reussites"] == [recrutement.pk]
    recrutement_agent = RecrutementAgentModel.objects.get(
        recrutement_id=recrutement.pk, agent_id=membre.utilisateur_id
    )
    assert recrutement_agent.id == existant.id
    assert recrutement_agent.role == AgentRecrutementRole.RESPONSABLE.value
    logs = PostgresAuditLogRepository().get_logs_for_ressource(
        "RecrutementAgent", recrutement.pk
    )
    assert len(logs) == 1
    assert logs[0].event_name == "AgentRecrutementModifie"


def test_reintegrates_agent_previously_revoked_from_recrutement(db):
    responsable, organisme = create_organisme_with_agent(
        role=AgentOrganismeRole.SUPERVISEUR
    )
    membre = OrganismeAgentDjangoFactory(
        organisme=organisme, role=AgentOrganismeRole.AGENT.value
    ).agent
    recrutement = RecrutementDjangoFactory(organisme=organisme)
    RecrutementAgentDjangoFactory(
        recrutement=recrutement,
        agent=membre,
        role=AgentRecrutementRole.CONTRIBUTEUR.value,
        date_revocation=timezone.now(),
    )

    resultats = set_recrutements_responsable(
        organisme_id=organisme.id,
        recrutement_ids=[recrutement.pk],
        agent_id=membre.utilisateur_id,
        utilisateur=_utilisateur(responsable.utilisateur_id),
    )

    assert resultats["reussites"] == [recrutement.pk]
    recrutement_agent = RecrutementAgentModel.objects.get(
        recrutement_id=recrutement.pk, agent_id=membre.utilisateur_id
    )
    assert recrutement_agent.role == AgentRecrutementRole.RESPONSABLE.value
    assert recrutement_agent.date_revocation is None


def test_allows_multiple_responsables_on_same_recrutement(db):
    responsable, organisme = create_organisme_with_agent(
        role=AgentOrganismeRole.SUPERVISEUR
    )
    membre = OrganismeAgentDjangoFactory(
        organisme=organisme, role=AgentOrganismeRole.AGENT.value
    ).agent
    recrutement = RecrutementDjangoFactory(organisme=organisme)
    autre_membre = OrganismeAgentDjangoFactory(
        organisme=organisme, role=AgentOrganismeRole.AGENT.value
    ).agent
    RecrutementAgentDjangoFactory(
        recrutement=recrutement,
        agent=autre_membre,
        role=AgentRecrutementRole.RESPONSABLE.value,
    )

    resultats = set_recrutements_responsable(
        organisme_id=organisme.id,
        recrutement_ids=[recrutement.pk],
        agent_id=membre.utilisateur_id,
        utilisateur=_utilisateur(responsable.utilisateur_id),
    )

    assert resultats["reussites"] == [recrutement.pk]
    assert (
        RecrutementAgentModel.objects.get(
            recrutement_id=recrutement.pk, agent_id=membre.utilisateur_id
        ).role
        == AgentRecrutementRole.RESPONSABLE.value
    )
    assert (
        RecrutementAgentModel.objects.get(
            recrutement_id=recrutement.pk, agent_id=autre_membre.utilisateur_id
        ).role
        == AgentRecrutementRole.RESPONSABLE.value
    )


@pytest.mark.parametrize(
    "position", ["first", "last"], ids=["invalid_first", "invalid_last"]
)
def test_reports_echec_for_recrutement_belonging_to_another_organisme(db, position):
    responsable, organisme = create_organisme_with_agent(
        role=AgentOrganismeRole.SUPERVISEUR
    )
    membre = OrganismeAgentDjangoFactory(
        organisme=organisme, role=AgentOrganismeRole.AGENT.value
    ).agent
    valide = RecrutementDjangoFactory(organisme=organisme)
    autre_organisme = OrganismeDjangoFactory()
    invalide = RecrutementDjangoFactory(organisme=autre_organisme)
    ids = [invalide.pk, valide.pk] if position == "first" else [valide.pk, invalide.pk]

    resultats = set_recrutements_responsable(
        organisme_id=organisme.id,
        recrutement_ids=ids,
        agent_id=membre.utilisateur_id,
        utilisateur=_utilisateur(responsable.utilisateur_id),
    )

    assert resultats["reussites"] == [valide.pk]
    assert [echec["recrutement_id"] for echec in resultats["echecs"]] == [invalide.pk]
    assert resultats["echecs"][0]["raison"]
    assert not RecrutementAgentModel.objects.filter(
        recrutement_id=invalide.pk, agent_id=membre.utilisateur_id
    ).exists()
    assert (
        PostgresAuditLogRepository().get_logs_for_ressource(
            "RecrutementAgent", invalide.pk
        )
        == []
    )
