from uuid import uuid4

import pytest

from application.recruteur.services.update_recrutement_agent import (
    update_recrutement_agent,
)
from domain.commons.errors.organisme_errors import OrganismeNexistePas
from domain.identite.errors.organisme_permission_errors import AccesOrganismeRefuse
from domain.recruteur.errors.organisme_agent_errors import AgentNonRattache
from domain.recruteur.errors.recrutement_agent_errors import AgentNonMembreRecrutement
from domain.recruteur.errors.recrutement_errors import RecrutementInexistant
from domain.recruteur.value_objects.roles import (
    AgentOrganismeRole,
    AgentRecrutementRole,
)
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


def test_responsable_updates_agent_role(db):
    responsable, organisme = create_organisme_with_agent(
        role=AgentOrganismeRole.RESPONSABLE
    )
    membre = OrganismeAgentDjangoFactory(
        organisme=organisme, role=AgentOrganismeRole.MEMBRE.value
    ).agent
    recrutement = RecrutementDjangoFactory(organisme=organisme)
    RecrutementAgentDjangoFactory(
        recrutement=recrutement,
        agent=membre,
        role=AgentRecrutementRole.CONTRIBUTEUR.value,
    )

    recrutement_agent = update_recrutement_agent(
        organisme_id=organisme.id,
        recrutement_id=recrutement.pk,
        agent_id=membre.utilisateur_id,
        role=AgentRecrutementRole.RECRUTEUR.value,
        utilisateur=_utilisateur(responsable.utilisateur_id),
    )

    assert recrutement_agent.role == AgentRecrutementRole.RECRUTEUR.value
    assert (
        RecrutementAgentModel.objects.get(
            recrutement_id=recrutement.pk, agent_id=membre.utilisateur_id
        ).role
        == AgentRecrutementRole.RECRUTEUR.value
    )

    logs = PostgresAuditLogRepository().get_logs_for_ressource(
        "RecrutementAgent", membre.utilisateur_id
    )
    assert len(logs) == 1
    assert logs[0].event_name == "AgentRecrutementRoleModifie"
    assert logs[0].utilisateur_id == responsable.utilisateur_id


def test_staff_bypasses_role_check(db):
    organisme = OrganismeDjangoFactory()
    membre = OrganismeAgentDjangoFactory(
        organisme=organisme, role=AgentOrganismeRole.MEMBRE.value
    ).agent
    recrutement = RecrutementDjangoFactory(organisme=organisme)
    RecrutementAgentDjangoFactory(
        recrutement=recrutement,
        agent=membre,
        role=AgentRecrutementRole.CONTRIBUTEUR.value,
    )

    recrutement_agent = update_recrutement_agent(
        organisme_id=organisme.id,
        recrutement_id=recrutement.pk,
        agent_id=membre.utilisateur_id,
        role=AgentRecrutementRole.RECRUTEUR.value,
        utilisateur=_utilisateur(uuid4(), is_staff=True),
    )

    assert recrutement_agent.role == AgentRecrutementRole.RECRUTEUR.value


@pytest.mark.parametrize(
    "role", [AgentOrganismeRole.MEMBRE, None], ids=["membre_role", "no_organisme_role"]
)
def test_denied_when_demandeur_is_not_responsable(db, role):
    if role is None:
        organisme = OrganismeDjangoFactory()
        demandeur_id = uuid4()
    else:
        demandeur, organisme = create_organisme_with_agent(role=role)
        demandeur_id = demandeur.utilisateur_id
    membre = OrganismeAgentDjangoFactory(
        organisme=organisme, role=AgentOrganismeRole.MEMBRE.value
    ).agent
    recrutement = RecrutementDjangoFactory(organisme=organisme)
    RecrutementAgentDjangoFactory(
        recrutement=recrutement,
        agent=membre,
        role=AgentRecrutementRole.CONTRIBUTEUR.value,
    )

    with pytest.raises(AccesOrganismeRefuse):
        update_recrutement_agent(
            organisme_id=organisme.id,
            recrutement_id=recrutement.pk,
            agent_id=membre.utilisateur_id,
            role=AgentRecrutementRole.RECRUTEUR.value,
            utilisateur=_utilisateur(demandeur_id),
        )

    assert (
        RecrutementAgentModel.objects.get(
            recrutement_id=recrutement.pk, agent_id=membre.utilisateur_id
        ).role
        == AgentRecrutementRole.CONTRIBUTEUR.value
    )
    assert (
        PostgresAuditLogRepository().get_logs_for_ressource(
            "RecrutementAgent", membre.utilisateur_id
        )
        == []
    )


def test_raises_when_organisme_does_not_exist(db):
    membre = AgentDjangoFactory()

    with pytest.raises(OrganismeNexistePas):
        update_recrutement_agent(
            organisme_id=uuid4(),
            recrutement_id=uuid4(),
            agent_id=membre.utilisateur_id,
            role=AgentRecrutementRole.CONTRIBUTEUR.value,
            utilisateur=_utilisateur(uuid4()),
        )


def test_raises_when_recrutement_does_not_belong_to_organisme(db):
    responsable, organisme = create_organisme_with_agent(
        role=AgentOrganismeRole.RESPONSABLE
    )
    membre = OrganismeAgentDjangoFactory(
        organisme=organisme, role=AgentOrganismeRole.MEMBRE.value
    ).agent
    autre_organisme = OrganismeDjangoFactory()
    recrutement = RecrutementDjangoFactory(organisme=autre_organisme)

    with pytest.raises(RecrutementInexistant):
        update_recrutement_agent(
            organisme_id=organisme.id,
            recrutement_id=recrutement.pk,
            agent_id=membre.utilisateur_id,
            role=AgentRecrutementRole.CONTRIBUTEUR.value,
            utilisateur=_utilisateur(responsable.utilisateur_id),
        )


def test_raises_when_agent_to_update_is_not_attached_to_organisme(db):
    responsable, organisme = create_organisme_with_agent(
        role=AgentOrganismeRole.RESPONSABLE
    )
    bare_agent = AgentDjangoFactory()
    recrutement = RecrutementDjangoFactory(organisme=organisme)

    with pytest.raises(AgentNonRattache):
        update_recrutement_agent(
            organisme_id=organisme.id,
            recrutement_id=recrutement.pk,
            agent_id=bare_agent.utilisateur_id,
            role=AgentRecrutementRole.CONTRIBUTEUR.value,
            utilisateur=_utilisateur(responsable.utilisateur_id),
        )


def test_raises_when_agent_is_not_member_of_recrutement(db):
    responsable, organisme = create_organisme_with_agent(
        role=AgentOrganismeRole.RESPONSABLE
    )
    membre = OrganismeAgentDjangoFactory(
        organisme=organisme, role=AgentOrganismeRole.MEMBRE.value
    ).agent
    recrutement = RecrutementDjangoFactory(organisme=organisme)

    with pytest.raises(AgentNonMembreRecrutement):
        update_recrutement_agent(
            organisme_id=organisme.id,
            recrutement_id=recrutement.pk,
            agent_id=membre.utilisateur_id,
            role=AgentRecrutementRole.CONTRIBUTEUR.value,
            utilisateur=_utilisateur(responsable.utilisateur_id),
        )


def test_rolls_back_role_update_when_audit_log_write_fails(db, monkeypatch):
    responsable, organisme = create_organisme_with_agent(
        role=AgentOrganismeRole.RESPONSABLE
    )
    membre = OrganismeAgentDjangoFactory(
        organisme=organisme, role=AgentOrganismeRole.MEMBRE.value
    ).agent
    recrutement = RecrutementDjangoFactory(organisme=organisme)
    RecrutementAgentDjangoFactory(
        recrutement=recrutement,
        agent=membre,
        role=AgentRecrutementRole.CONTRIBUTEUR.value,
    )

    def _raise(*args, **kwargs):
        raise RuntimeError("audit log write failed")

    monkeypatch.setattr(
        "application.recruteur.services.update_recrutement_agent.AuditLogWriter.log_action",
        _raise,
    )

    with pytest.raises(RuntimeError):
        update_recrutement_agent(
            organisme_id=organisme.id,
            recrutement_id=recrutement.pk,
            agent_id=membre.utilisateur_id,
            role=AgentRecrutementRole.RECRUTEUR.value,
            utilisateur=_utilisateur(responsable.utilisateur_id),
        )

    assert (
        RecrutementAgentModel.objects.get(
            recrutement_id=recrutement.pk, agent_id=membre.utilisateur_id
        ).role
        == AgentRecrutementRole.CONTRIBUTEUR.value
    )
