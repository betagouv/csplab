from unittest.mock import Mock, patch

import pytest
from django.utils import timezone

from application.recruteur.services.add_recrutement_agent import add_recrutement_agent
from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.identite.errors.organisme_permission_errors import (
    AccesRecrutementRefuse,
)
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
    create_organisme_with_agent,
)
from infrastructure.factories.recruteur.recrutement_django_factory import (
    RecrutementAgentDjangoFactory,
    RecrutementDjangoFactory,
)
from infrastructure.repositories.commons.postgres_audit_log_repository import (
    PostgresAuditLogRepository,
)


def test_responsable_adds_agent_to_recrutement(db):
    responsable, organisme = create_organisme_with_agent(
        role=AgentOrganismeRole.SUPERVISEUR
    )
    membre = OrganismeAgentDjangoFactory(
        organisme=organisme, role=AgentOrganismeRole.AGENT.value
    ).agent
    recrutement = RecrutementDjangoFactory(organisme=organisme)

    recrutement_agent = add_recrutement_agent(
        organisme_id=organisme.id,
        recrutement_id=recrutement.pk,
        agent_id=membre.utilisateur_id,
        role=AgentRecrutementRole.CONTRIBUTEUR.value,
        utilisateur=responsable.utilisateur,
    )

    assert recrutement_agent.recrutement_id == recrutement.pk
    assert recrutement_agent.agent_id == membre.utilisateur_id
    assert recrutement_agent.role == AgentRecrutementRole.CONTRIBUTEUR.value
    assert RecrutementAgentModel.objects.filter(
        recrutement_id=recrutement.pk, agent_id=membre.utilisateur_id
    ).exists()

    logs = PostgresAuditLogRepository().get_logs_for_ressource(
        "RecrutementAgent", membre.utilisateur_id
    )
    assert len(logs) == 1
    assert logs[0].event_name == "AgentRecrutementAjoute"
    assert logs[0].utilisateur_id == responsable.utilisateur_id


def test_denied_when_demandeur_responsable_role_is_revoked(db):
    demandeur, organisme = create_organisme_with_agent(role=AgentOrganismeRole.AGENT)
    membre = OrganismeAgentDjangoFactory(
        organisme=organisme, role=AgentOrganismeRole.AGENT.value
    ).agent
    recrutement = RecrutementDjangoFactory(organisme=organisme)
    RecrutementAgentDjangoFactory(
        recrutement=recrutement,
        agent=demandeur,
        role=AgentRecrutementRole.RESPONSABLE.value,
        date_revocation=timezone.now(),
    )

    with pytest.raises(AccesRecrutementRefuse):
        add_recrutement_agent(
            organisme_id=organisme.id,
            recrutement_id=recrutement.pk,
            agent_id=membre.utilisateur_id,
            role=AgentRecrutementRole.CONTRIBUTEUR.value,
            utilisateur=demandeur.utilisateur,
        )

    assert not RecrutementAgentModel.objects.filter(
        recrutement_id=recrutement.pk, agent_id=membre.utilisateur_id
    ).exists()


def test_attaches_agent_to_organisme_when_not_attached(db):
    responsable, organisme = create_organisme_with_agent(
        role=AgentOrganismeRole.SUPERVISEUR
    )
    bare_agent = AgentDjangoFactory()
    recrutement = RecrutementDjangoFactory(organisme=organisme)

    recrutement_agent = add_recrutement_agent(
        organisme_id=organisme.id,
        recrutement_id=recrutement.pk,
        agent_id=bare_agent.utilisateur_id,
        role=AgentRecrutementRole.CONTRIBUTEUR.value,
        utilisateur=responsable.utilisateur,
    )

    assert recrutement_agent.agent_id == bare_agent.utilisateur_id
    liaison = OrganismeAgentModel.objects.get(
        organisme_id=organisme.id, agent_id=bare_agent.utilisateur_id
    )
    assert liaison.role == AgentOrganismeRole.AGENT.value
    assert liaison.date_revocation is None

    organisme_logs = PostgresAuditLogRepository().get_logs_for_ressource(
        "AgentOrganisme", bare_agent.utilisateur_id
    )
    assert [log.event_name for log in organisme_logs] == ["AgentOrganismeRoleAttache"]
    assert organisme_logs[0].utilisateur_id == responsable.utilisateur_id
    recrutement_logs = PostgresAuditLogRepository().get_logs_for_ressource(
        "RecrutementAgent", bare_agent.utilisateur_id
    )
    assert [log.event_name for log in recrutement_logs] == ["AgentRecrutementAjoute"]


def test_reattaches_revoked_organisme_agent_with_agent_role(db):
    responsable, organisme = create_organisme_with_agent(
        role=AgentOrganismeRole.SUPERVISEUR
    )
    revoked = OrganismeAgentDjangoFactory(
        organisme=organisme,
        role=AgentOrganismeRole.SUPERVISEUR.value,
        date_revocation=timezone.now(),
    )
    recrutement = RecrutementDjangoFactory(organisme=organisme)

    add_recrutement_agent(
        organisme_id=organisme.id,
        recrutement_id=recrutement.pk,
        agent_id=revoked.agent.utilisateur_id,
        role=AgentRecrutementRole.CONTRIBUTEUR.value,
        utilisateur=responsable.utilisateur,
    )

    liaison = OrganismeAgentModel.objects.get(
        organisme_id=organisme.id, agent_id=revoked.agent.utilisateur_id
    )
    assert liaison.id == revoked.id
    assert liaison.role == AgentOrganismeRole.AGENT.value
    assert liaison.date_revocation is None


def test_keeps_existing_organisme_role_of_attached_agent(db):
    responsable, organisme = create_organisme_with_agent(
        role=AgentOrganismeRole.SUPERVISEUR
    )
    superviseur = OrganismeAgentDjangoFactory(
        organisme=organisme, role=AgentOrganismeRole.SUPERVISEUR.value
    ).agent
    recrutement = RecrutementDjangoFactory(organisme=organisme)

    add_recrutement_agent(
        organisme_id=organisme.id,
        recrutement_id=recrutement.pk,
        agent_id=superviseur.utilisateur_id,
        role=AgentRecrutementRole.CONTRIBUTEUR.value,
        utilisateur=responsable.utilisateur,
    )

    assert (
        OrganismeAgentModel.objects.get(
            organisme_id=organisme.id, agent_id=superviseur.utilisateur_id
        ).role
        == AgentOrganismeRole.SUPERVISEUR.value
    )
    assert (
        PostgresAuditLogRepository().get_logs_for_ressource(
            "AgentOrganisme", superviseur.utilisateur_id
        )
        == []
    )


@patch.object(
    AuditLogWriter,
    "log_action",
    new=Mock(side_effect=[None, RuntimeError("audit log write failed")]),
)
def test_rolls_back_organisme_attachment_when_recrutement_audit_log_fails(db):
    responsable, organisme = create_organisme_with_agent(
        role=AgentOrganismeRole.SUPERVISEUR
    )
    bare_agent = AgentDjangoFactory()
    recrutement = RecrutementDjangoFactory(organisme=organisme)
    with pytest.raises(RuntimeError):
        add_recrutement_agent(
            organisme_id=organisme.id,
            recrutement_id=recrutement.pk,
            agent_id=bare_agent.utilisateur_id,
            role=AgentRecrutementRole.CONTRIBUTEUR.value,
            utilisateur=responsable.utilisateur,
        )

    assert not OrganismeAgentModel.objects.filter(
        organisme_id=organisme.id, agent_id=bare_agent.utilisateur_id
    ).exists()
    assert not RecrutementAgentModel.objects.filter(
        recrutement_id=recrutement.pk, agent_id=bare_agent.utilisateur_id
    ).exists()


@patch.object(
    AuditLogWriter,
    "log_action",
    new=Mock(side_effect=RuntimeError("audit log write failed")),
)
def test_rolls_back_membership_when_audit_log_write_fails(db):
    responsable, organisme = create_organisme_with_agent(
        role=AgentOrganismeRole.SUPERVISEUR
    )
    membre = OrganismeAgentDjangoFactory(
        organisme=organisme, role=AgentOrganismeRole.AGENT.value
    ).agent
    recrutement = RecrutementDjangoFactory(organisme=organisme)

    with pytest.raises(RuntimeError):
        add_recrutement_agent(
            organisme_id=organisme.id,
            recrutement_id=recrutement.pk,
            agent_id=membre.utilisateur_id,
            role=AgentRecrutementRole.CONTRIBUTEUR.value,
            utilisateur=responsable.utilisateur,
        )

    assert not RecrutementAgentModel.objects.filter(
        recrutement_id=recrutement.pk, agent_id=membre.utilisateur_id
    ).exists()


def test_reintegrates_previously_revoked_agent(db):
    responsable, organisme = create_organisme_with_agent(
        role=AgentOrganismeRole.SUPERVISEUR
    )
    membre = OrganismeAgentDjangoFactory(
        organisme=organisme, role=AgentOrganismeRole.AGENT.value
    ).agent
    recrutement = RecrutementDjangoFactory(organisme=organisme)
    revoked = RecrutementAgentDjangoFactory(
        recrutement=recrutement,
        agent=membre,
        role=AgentRecrutementRole.CONTRIBUTEUR.value,
        date_revocation=timezone.now(),
    )

    recrutement_agent = add_recrutement_agent(
        organisme_id=organisme.id,
        recrutement_id=recrutement.pk,
        agent_id=membre.utilisateur_id,
        role=AgentRecrutementRole.RECRUTEUR.value,
        utilisateur=responsable.utilisateur,
    )

    assert recrutement_agent.id == revoked.id
    assert recrutement_agent.role == AgentRecrutementRole.RECRUTEUR.value
    assert recrutement_agent.date_revocation is None

    logs = PostgresAuditLogRepository().get_logs_for_ressource(
        "RecrutementAgent", membre.utilisateur_id
    )
    assert len(logs) == 1
    assert logs[0].event_name == "AgentRecrutementReintegre"


@patch.object(
    AuditLogWriter,
    "log_action",
    new=Mock(side_effect=RuntimeError("audit log write failed")),
)
def test_rolls_back_reintegration_when_audit_log_write_fails(db):
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

    with pytest.raises(RuntimeError):
        add_recrutement_agent(
            organisme_id=organisme.id,
            recrutement_id=recrutement.pk,
            agent_id=membre.utilisateur_id,
            role=AgentRecrutementRole.RECRUTEUR.value,
            utilisateur=responsable.utilisateur,
        )

    assert (
        RecrutementAgentModel.objects.get(
            recrutement_id=recrutement.pk, agent_id=membre.utilisateur_id
        ).date_revocation
        is not None
    )
