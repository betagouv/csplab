import pytest
from faker import Faker

from application.identite.usecases.create_agent import CreateAgentInput
from config.app_config import AppConfig
from domain.identite.errors.agent_errors import ProfilAgentAlreadyExists
from infrastructure.di.identite.identite_container import IdentiteContainer
from infrastructure.gateways.shared.logger import LoggerService
from tests.factories.identite.utilisateur_factory import UtilisateurFactory
from tests.factories.recruteur.agent_factory import AgentFactory

fake = Faker()


@pytest.fixture(name="identite_integration_container")
def identite_integration_container_fixture(db):
    container = IdentiteContainer()
    app_config = AppConfig.from_django_settings()
    logger_service = LoggerService()
    container.app_config.override(app_config)
    container.logger_service.override(logger_service)
    return container


def test_create_agent(identite_integration_container):
    input_data = CreateAgentInput(
        email=fake.email(),
        prenom=fake.first_name(),
        nom=fake.last_name(),
        matricule=fake.bothify("MAT-####"),
    )

    result = identite_integration_container.create_agent_usecase().execute(input_data)

    assert result.email == input_data.email
    assert result.prenom == input_data.prenom
    assert result.nom == input_data.nom
    assert result.matricule == input_data.matricule


def test_create_agent_with_existing_user(identite_integration_container):
    existing_user = UtilisateurFactory.create_model(email=fake.email())
    input_data = CreateAgentInput(
        email=existing_user.email,
        prenom=fake.first_name(),
        nom=fake.last_name(),
        matricule=fake.bothify("MAT-####"),
    )

    result = identite_integration_container.create_agent_usecase().execute(input_data)

    assert str(result.entity_id) == existing_user.username


def test_cannot_create_agent_twice(identite_integration_container):
    existing_agent = AgentFactory.create_model()
    input_data = CreateAgentInput(
        email=existing_agent.utilisateur.email,
        prenom=fake.first_name(),
        nom=fake.last_name(),
        matricule=fake.bothify("MAT-####"),
    )

    with pytest.raises(ProfilAgentAlreadyExists):
        identite_integration_container.create_agent_usecase().execute(input_data)
