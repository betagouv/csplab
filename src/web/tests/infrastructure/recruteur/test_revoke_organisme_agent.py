from uuid import uuid4

import pytest

from application.recruteur.usecases.revoke_organisme_agent import (
    RevokeOrganismeAgentCommand,
    RevokeOrganismeAgentUsecase,
)
from config.app_config import AppConfig
from domain.commons.errors.organisme_errors import OrganismeNexistePas
from domain.identite.errors.organisme_permission_errors import AccesOrganismeRefuse
from domain.recruteur.errors.organisme_agent_errors import AgentNonRattache
from domain.recruteur.value_objects.roles import AgentOrganismeRole
from infrastructure.di.recruteur.recruteur_container import RecruteurContainer
from infrastructure.django_apps.recruteur.models.organisme import OrganismeAgentModel
from infrastructure.factories.identite.agent_factory import AgentFactory
from infrastructure.factories.identite.organisme_factory import OrganismeFactory
from infrastructure.factories.identite.utilisateur_factory import UtilisateurFactory
from infrastructure.gateways.shared.logger import LoggerService


@pytest.fixture(name="recruteur_integration_container")
def recruteur_integration_container_fixture(db) -> RecruteurContainer:
    container = RecruteurContainer()
    container.app_config.override(AppConfig.from_django_settings())
    container.logger_service.override(LoggerService())
    return container


@pytest.fixture(name="usecase")
def usecase_fixture(
    recruteur_integration_container,
) -> RevokeOrganismeAgentUsecase:
    return recruteur_integration_container.revoke_organisme_agent_usecase()


def test_responsable_revokes_agent(db, usecase, recruteur_integration_container):
    responsable, organisme = OrganismeFactory.create_model_with_agent(
        role=AgentOrganismeRole.RESPONSABLE
    )
    autre_agent = OrganismeFactory.create_agent_in_organisme(
        organisme.id, role=AgentOrganismeRole.MEMBRE
    )

    agent_organisme = usecase.execute(
        RevokeOrganismeAgentCommand(
            organisme_id=organisme.id,
            agent_id=autre_agent.utilisateur_id,
            utilisateur=UtilisateurFactory.create_entity(
                entity_id=responsable.utilisateur_id, is_staff=False
            ),
        )
    )

    assert agent_organisme.entity_id == autre_agent.utilisateur_id
    assert agent_organisme.date_revocation is not None
    liaison = OrganismeAgentModel.objects.get(
        organisme_id=organisme.id, agent_id=autre_agent.utilisateur_id
    )
    assert liaison.date_revocation is not None

    audit_log_repository = (
        recruteur_integration_container.postgres_audit_log_repository()
    )
    logs = audit_log_repository.get_logs_for_ressource(
        "AgentOrganisme", autre_agent.utilisateur_id
    )
    assert len(logs) == 1
    assert logs[0].event_name == "AgentOrganismeRoleRevoque"
    assert logs[0].utilisateur_id == responsable.utilisateur_id
    assert logs[0].ressource_id == autre_agent.utilisateur_id


def test_staff_bypasses_role_check(db, usecase):
    _, organisme = OrganismeFactory.create_model_with_agent(
        role=AgentOrganismeRole.MEMBRE
    )
    autre_agent = OrganismeFactory.create_agent_in_organisme(
        organisme.id, role=AgentOrganismeRole.MEMBRE
    )

    agent_organisme = usecase.execute(
        RevokeOrganismeAgentCommand(
            organisme_id=organisme.id,
            agent_id=autre_agent.utilisateur_id,
            utilisateur=UtilisateurFactory.create_entity(
                entity_id=uuid4(), is_staff=True
            ),
        )
    )

    assert agent_organisme.date_revocation is not None


def test_membre_is_denied(db, usecase, recruteur_integration_container):
    membre, organisme = OrganismeFactory.create_model_with_agent(
        role=AgentOrganismeRole.MEMBRE
    )
    autre_agent = OrganismeFactory.create_agent_in_organisme(
        organisme.id, role=AgentOrganismeRole.MEMBRE
    )

    with pytest.raises(AccesOrganismeRefuse):
        usecase.execute(
            RevokeOrganismeAgentCommand(
                organisme_id=organisme.id,
                agent_id=autre_agent.utilisateur_id,
                utilisateur=UtilisateurFactory.create_entity(
                    entity_id=membre.utilisateur_id, is_staff=False
                ),
            )
        )

    liaison = OrganismeAgentModel.objects.get(
        organisme_id=organisme.id, agent_id=autre_agent.utilisateur_id
    )
    assert liaison.date_revocation is None
    audit_log_repository = (
        recruteur_integration_container.postgres_audit_log_repository()
    )
    assert (
        audit_log_repository.get_logs_for_ressource(
            "AgentOrganisme", autre_agent.utilisateur_id
        )
        == []
    )


def test_raises_when_agent_not_attached(db, usecase):
    responsable, organisme = OrganismeFactory.create_model_with_agent(
        role=AgentOrganismeRole.RESPONSABLE
    )
    bare_agent = AgentFactory.create_model()

    with pytest.raises(AgentNonRattache):
        usecase.execute(
            RevokeOrganismeAgentCommand(
                organisme_id=organisme.id,
                agent_id=bare_agent.utilisateur_id,
                utilisateur=UtilisateurFactory.create_entity(
                    entity_id=responsable.utilisateur_id, is_staff=False
                ),
            )
        )


def test_raises_when_organisme_does_not_exist(db, usecase):
    bare_agent = AgentFactory.create_model()

    with pytest.raises(OrganismeNexistePas):
        usecase.execute(
            RevokeOrganismeAgentCommand(
                organisme_id=uuid4(),
                agent_id=bare_agent.utilisateur_id,
                utilisateur=UtilisateurFactory.create_entity(
                    entity_id=uuid4(), is_staff=False
                ),
            )
        )
