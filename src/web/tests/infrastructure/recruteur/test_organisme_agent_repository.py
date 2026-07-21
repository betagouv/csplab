from uuid import uuid4

import pytest

from domain.recruteur.value_objects.roles import AgentOrganismeRole
from infrastructure.django_apps.recruteur.models.organisme import OrganismeAgentModel
from infrastructure.factories.identite.agent_factory import AgentFactory
from infrastructure.factories.identite.organisme_factory import OrganismeFactory
from infrastructure.repositories.recruteur.postgres_organisme_agent_repository import (
    PostgresOrganismeAgentRepository,
)


@pytest.fixture(name="repository")
def repository_fixture():
    return PostgresOrganismeAgentRepository()


def test_get_role_returns_responsable(db, repository):
    organisme_model = OrganismeFactory.create_model()
    agent = AgentFactory.create_model()
    OrganismeAgentModel(
        id=uuid4(),
        organisme_id=organisme_model.id,
        agent_id=agent.utilisateur_id,
        role=AgentOrganismeRole.RESPONSABLE.value,
    ).save()

    role = repository.get_role(
        organisme_id=organisme_model.id, agent_id=agent.utilisateur_id
    )

    assert role == AgentOrganismeRole.RESPONSABLE


def test_get_role_returns_membre(db, repository):
    organisme_model = OrganismeFactory.create_model()
    agent = AgentFactory.create_model()
    OrganismeAgentModel(
        id=uuid4(),
        organisme_id=organisme_model.id,
        agent_id=agent.utilisateur_id,
        role=AgentOrganismeRole.MEMBRE.value,
    ).save()

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
