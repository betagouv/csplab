import pytest
from faker import Faker

from application.identite.usecases.create_agent import CreateAgentInput
from config.app_config import AppConfig
from domain.identite.errors.agent_errors import ProfilAgentExisteDeja
from infrastructure.di.identite.identite_container import IdentiteContainer
from infrastructure.factories.identite.agent_factory import AgentFactory
from infrastructure.factories.identite.organisme_factory import OrganismeFactory
from infrastructure.factories.identite.utilisateur_factory import UtilisateurFactory
from infrastructure.gateways.shared.logger import LoggerService

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
    return OrganismeFactory.create_model().id


def test_create_agent(identite_integration_container, organisme_id):
    input_data = CreateAgentInput(
        email=fake.email(),
        prenom=fake.first_name(),
        nom=fake.last_name(),
        intitule_poste=fake.bothify("MAT-####"),
        organisme_id=organisme_id,
        utilisateur=STAFF_UTILISATEUR,
    )

    result = identite_integration_container.create_agent_usecase().execute(input_data)

    assert result.email == input_data.email
    assert result.prenom == input_data.prenom
    assert result.nom == input_data.nom
    assert result.intitule_poste == input_data.intitule_poste


def test_create_agent_with_existing_user(identite_integration_container, organisme_id):
    existing_user = UtilisateurFactory.create_model(email=fake.email())
    input_data = CreateAgentInput(
        email=existing_user.email,
        prenom=fake.first_name(),
        nom=fake.last_name(),
        intitule_poste=fake.bothify("MAT-####"),
        organisme_id=organisme_id,
        utilisateur=STAFF_UTILISATEUR,
    )

    result = identite_integration_container.create_agent_usecase().execute(input_data)

    assert result.entity_id == existing_user.username


def test_cannot_create_agent_twice(identite_integration_container, organisme_id):
    existing_agent = AgentFactory.create_model()
    input_data = CreateAgentInput(
        email=existing_agent.utilisateur.email,
        prenom=fake.first_name(),
        nom=fake.last_name(),
        intitule_poste=fake.bothify("MAT-####"),
        organisme_id=organisme_id,
        utilisateur=STAFF_UTILISATEUR,
    )

    with pytest.raises(ProfilAgentExisteDeja):
        identite_integration_container.create_agent_usecase().execute(input_data)
