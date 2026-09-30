from unittest.mock import Mock, patch

import pytest
from faker import Faker

from application.identite.usecases.create_agent import CreateAgentInput
from config.app_config import AppConfig
from domain.identite.errors.agent_errors import ProfilAgentExisteDeja
from infrastructure.di.identite.identite_container import IdentiteContainer
from infrastructure.django_apps.commons.models import AuditLogModel
from infrastructure.django_apps.users.models import UserModel
from infrastructure.factories.identite.agent_django_factory import (
    AgentDjangoFactory,
)
from infrastructure.factories.identite.organisme_django_factory import (
    OrganismeDjangoFactory,
)
from infrastructure.factories.identite.utilisateur_django_factory import (
    UtilisateurDjangoFactory,
)
from infrastructure.factories.identite.utilisateur_factory import UtilisateurFactory
from infrastructure.gateways.shared.logger import LoggerService
from infrastructure.repositories.identite.postgres_agent_repository import (
    PostgresAgentRepository,
)

fake = Faker()

STAFF_UTILISATEUR = UtilisateurFactory.create_entity(is_staff=True)


@pytest.fixture(name="identite_integration_container")
def identite_integration_container_fixture(db):
    container = IdentiteContainer()
    app_config = AppConfig.from_django_settings()
    logger_service = LoggerService()
    container.app_config.override(app_config)
    container.logger_service.override(logger_service)
    return container


@pytest.fixture(name="organisme_id")
def organisme_id_fixture(db):
    return OrganismeDjangoFactory().id


def _agent_logs(container, ressource_id):
    return container.postgres_audit_log_repository().get_logs_for_ressource(
        "Agent", ressource_id
    )


def test_create_agent(identite_integration_container, organisme_id):
    input_data = CreateAgentInput(
        email=fake.email(),
        organisme_id=organisme_id,
        utilisateur=STAFF_UTILISATEUR,
    )

    result = identite_integration_container.create_agent_usecase().execute(input_data)

    assert result.email == input_data.email
    utilisateur = UserModel.objects.get(email=input_data.email)
    assert utilisateur.first_name == ""
    assert utilisateur.last_name == ""
    assert utilisateur.profil_agent.intitule_poste == ""

    [log] = _agent_logs(identite_integration_container, result.entity_id)
    assert log.event_name == "ProfilAgentCree"
    assert log.utilisateur_id == STAFF_UTILISATEUR.entity_id
    assert log.ressource_id == utilisateur.username


def test_create_agent_with_existing_user(identite_integration_container, organisme_id):
    existing_user = UtilisateurDjangoFactory(email=fake.email())
    input_data = CreateAgentInput(
        email=existing_user.email,
        organisme_id=organisme_id,
        utilisateur=STAFF_UTILISATEUR,
    )

    result = identite_integration_container.create_agent_usecase().execute(input_data)

    assert result.entity_id == existing_user.username
    [log] = _agent_logs(identite_integration_container, existing_user.username)
    assert log.event_name == "ProfilAgentCree"


def test_cannot_create_agent_twice(identite_integration_container, organisme_id):
    existing_agent = AgentDjangoFactory()
    input_data = CreateAgentInput(
        email=existing_agent.utilisateur.email,
        organisme_id=organisme_id,
        utilisateur=STAFF_UTILISATEUR,
    )

    with pytest.raises(ProfilAgentExisteDeja):
        identite_integration_container.create_agent_usecase().execute(input_data)

    assert not AuditLogModel.objects.exists()


@patch.object(
    PostgresAgentRepository,
    "create",
    new=Mock(side_effect=RuntimeError("write failed")),
)
def test_create_agent_does_not_log_when_write_fails(
    identite_integration_container, organisme_id
):
    existing_user = UtilisateurDjangoFactory(email=fake.email())
    input_data = CreateAgentInput(
        email=existing_user.email,
        organisme_id=organisme_id,
        utilisateur=STAFF_UTILISATEUR,
    )

    with pytest.raises(RuntimeError):
        identite_integration_container.create_agent_usecase().execute(input_data)

    assert not AuditLogModel.objects.exists()
