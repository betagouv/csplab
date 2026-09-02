import pytest

from config.app_config import AppConfig
from domain.recruteur.errors.organisme_agent_errors import (
    AgentDejaRattache,
    AgentNonRattache,
)
from domain.recruteur.value_objects.roles import AgentOrganismeRole
from infrastructure.di.recruteur.recruteur_container import RecruteurContainer
from infrastructure.django_apps.recruteur.models.organisme import OrganismeAgentModel
from infrastructure.factories.identite.agent_factory import AgentFactory
from infrastructure.factories.identite.organisme_factory import OrganismeFactory
from infrastructure.gateways.shared.logger import LoggerService
from infrastructure.repositories.recruteur.postgres_organisme_agent_repository import (
    PostgresOrganismeAgentRepository,
)


@pytest.fixture(name="recruteur_integration_container")
def recruteur_integration_container_fixture(db) -> RecruteurContainer:
    container = RecruteurContainer()
    container.app_config.override(AppConfig.from_django_settings())
    container.logger_service.override(LoggerService())
    return container


@pytest.fixture(name="repository")
def repository_fixture(
    recruteur_integration_container,
) -> PostgresOrganismeAgentRepository:
    return recruteur_integration_container.postgres_organisme_agent_repository()


def test_get_role_returns_responsable(db, repository):
    agent, organisme_model = OrganismeFactory.create_model_with_agent(
        role=AgentOrganismeRole.RESPONSABLE
    )

    role = repository.get_role(
        organisme_id=organisme_model.id, agent_id=agent.utilisateur_id
    )

    assert role == AgentOrganismeRole.RESPONSABLE


def test_get_role_returns_membre(db, repository):
    agent, organisme_model = OrganismeFactory.create_model_with_agent(
        role=AgentOrganismeRole.MEMBRE
    )

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


def test_attach_persists_liaison(db, repository):
    organisme_model = OrganismeFactory.create_model()
    agent = AgentFactory.create_model()

    repository.attach(
        organisme_id=organisme_model.id,
        agent_id=agent.utilisateur_id,
        role=AgentOrganismeRole.MEMBRE,
    )

    liaison = OrganismeAgentModel.objects.get(
        organisme_id=organisme_model.id, agent_id=agent.utilisateur_id
    )
    assert liaison.role == AgentOrganismeRole.MEMBRE.value


def test_attach_raises_when_already_attached(db, repository):
    agent, organisme_model = OrganismeFactory.create_model_with_agent(
        role=AgentOrganismeRole.MEMBRE
    )

    with pytest.raises(AgentDejaRattache):
        repository.attach(
            organisme_id=organisme_model.id,
            agent_id=agent.utilisateur_id,
            role=AgentOrganismeRole.RESPONSABLE,
        )


def test_update_role_persists_change(db, repository):
    agent, organisme_model = OrganismeFactory.create_model_with_agent(
        role=AgentOrganismeRole.MEMBRE
    )

    repository.update_role(
        organisme_id=organisme_model.id,
        agent_id=agent.utilisateur_id,
        role=AgentOrganismeRole.RESPONSABLE,
    )

    liaison = OrganismeAgentModel.objects.get(
        organisme_id=organisme_model.id, agent_id=agent.utilisateur_id
    )
    assert liaison.role == AgentOrganismeRole.RESPONSABLE.value


def test_update_role_raises_when_no_liaison(db, repository):
    organisme_model = OrganismeFactory.create_model()
    agent = AgentFactory.create_model()

    with pytest.raises(AgentNonRattache):
        repository.update_role(
            organisme_id=organisme_model.id,
            agent_id=agent.utilisateur_id,
            role=AgentOrganismeRole.RESPONSABLE,
        )
