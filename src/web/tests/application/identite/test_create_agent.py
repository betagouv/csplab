from unittest.mock import Mock
from uuid import uuid4

import pytest
from faker import Faker

from application.identite.usecases.create_agent import (
    CreateAgentInput,
    CreateAgentUsecase,
)
from domain.commons.errors.organisme_errors import OrganismeNexistePas
from domain.identite.errors.organisme_permission_errors import AccesOrganismeRefuse
from domain.identite.repositories.agent_repository_interface import IAgentRepository
from domain.identite.repositories.utilisateur_repository_interface import (
    IUtilisateurRepository,
)
from domain.identite.value_objects.organisme_action import OrganismeAction
from domain.recruteur.value_objects.roles import AgentOrganismeRole
from infrastructure.factories.identite.utilisateur_factory import UtilisateurFactory

fake = Faker()


@pytest.fixture(name="can_execute")
def can_execute_fixture(monkeypatch):
    mock = Mock(return_value=AgentOrganismeRole.RESPONSABLE)
    monkeypatch.setattr("application.identite.usecases.create_agent.can_execute", mock)
    return mock


@pytest.fixture(name="agent_repository")
def agent_repository_fixture():
    repository = Mock(spec=IAgentRepository)
    repository.get_by_email.return_value = None
    return repository


@pytest.fixture(name="utilisateur_repository")
def utilisateur_repository_fixture():
    repository = Mock(spec=IUtilisateurRepository)
    repository.get_by_email.return_value = UtilisateurFactory.create_entity()
    return repository


@pytest.fixture(name="usecase")
def usecase_fixture(can_execute, agent_repository, utilisateur_repository):
    return CreateAgentUsecase(
        agent_repository=agent_repository,
        utilisateur_repository=utilisateur_repository,
    )


def _input() -> CreateAgentInput:
    return CreateAgentInput(
        email=fake.email(),
        organisme_id=uuid4(),
        utilisateur=UtilisateurFactory.create_entity(),
    )


def test_create_agent_checks_permission(can_execute, usecase):
    input_data = _input()

    usecase.execute(input_data)

    can_execute.assert_called_once_with(
        action=OrganismeAction.CREATE_AGENT,
        utilisateur=input_data.utilisateur,
        organisme_id=input_data.organisme_id,
    )


@pytest.mark.parametrize(
    "exception", [AccesOrganismeRefuse(uuid4()), OrganismeNexistePas(str(uuid4()))]
)
def test_create_agent_propagates_permission_errors(
    can_execute, agent_repository, usecase, exception
):
    can_execute.side_effect = exception

    with pytest.raises(type(exception)):
        usecase.execute(_input())

    agent_repository.get_by_email.assert_not_called()
