import pytest

from domain.recruteur.value_objects.roles import AgentOrganismeRole
from infrastructure.factories.identite.agent_factory import AgentFactory
from infrastructure.factories.identite.organisme_factory import OrganismeFactory
from infrastructure.repositories.recruteur.postgres_organisme_agent_repository import (
    PostgresOrganismeAgentRepository,
)


@pytest.fixture(name="repository")
def repository_fixture():
    return PostgresOrganismeAgentRepository()


def test_get_role_returns_responsable(db, repository):
    agent = AgentFactory.create_model()
    organisme_model = OrganismeFactory.create_model(
        agent_id=agent.utilisateur_id, role=AgentOrganismeRole.RESPONSABLE
    )

    role = repository.get_role(
        organisme_id=organisme_model.id, agent_id=agent.utilisateur_id
    )

    assert role == AgentOrganismeRole.RESPONSABLE


def test_get_role_returns_membre(db, repository):
    agent = AgentFactory.create_model()
    organisme_model = OrganismeFactory.create_model(agent_id=agent.utilisateur_id)

    role = repository.get_role(
        organisme_id=organisme_model.id, agent_id=agent.utilisateur_id
    )

    assert role == AgentOrganismeRole.MEMBRE


def test_get_role_returns_none_when_no_liaison(db, repository):
    organisme_model = OrganismeFactory.create_model()
    agent = AgentFactory.create_model()

    role = repository.get_role(
        organisme_id=organisme_model.id, agent_id=agent.utilisateur_id
    )

    assert role is None
