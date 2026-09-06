import pytest

from domain.recruteur.value_objects.roles import AgentRecrutementRole
from infrastructure.factories.identite.agent_django_factory import (
    AgentDjangoFactory,
)
from infrastructure.factories.recruteur.recrutement_django_factory import (
    RecrutementDjangoFactory,
)
from infrastructure.repositories.recruteur.postgres_recrutement_agent_repository import (  # noqa: E501
    PostgresRecrutementAgentRepository,
)


@pytest.fixture(name="repository")
def repository_fixture():
    return PostgresRecrutementAgentRepository()


def test_get_role_returns_assigned_role(db, repository):
    agent = AgentDjangoFactory()
    agent_id = agent.utilisateur_id
    recrutement = RecrutementDjangoFactory(
        agent_link__agent=agent,
        agent_link__role=AgentRecrutementRole.RECRUTEUR.value,
    )

    role = repository.get_role(recrutement_id=recrutement.offre_id, agent_id=agent_id)

    assert role == AgentRecrutementRole.RECRUTEUR


def test_get_role_returns_none_when_no_liaison(db, repository):
    agent = AgentDjangoFactory()
    recrutement = RecrutementDjangoFactory()

    role = repository.get_role(
        recrutement_id=recrutement.offre_id, agent_id=agent.utilisateur_id
    )

    assert role is None
