import pytest
from faker import Faker

from application.identite.usecases.create_candidat import CreateCandidatInput
from config.app_config import AppConfig
from domain.identite.errors.candidat_errors import ProfilCandidatAlreadyExists
from infrastructure.di.identite.identite_container import IdentiteContainer
from infrastructure.gateways.shared.logger import LoggerService
from tests.factories.identite.candidat_factory import CandidatFactory
from tests.factories.identite.utilisateur_factory import UtilisateurFactory

fake = Faker()


@pytest.fixture(name="identite_integration_container")
def identite_integration_container_fixture(db):
    container = IdentiteContainer()
    app_config = AppConfig.from_django_settings()
    logger_service = LoggerService()
    container.app_config.override(app_config)
    container.logger_service.override(logger_service)
    return container


def test_create_candidat(identite_integration_container):
    input_data = CreateCandidatInput(
        email=fake.email(),
        prenom=fake.first_name(),
        nom=fake.last_name(),
        resume=fake.text(max_nb_chars=200),
    )

    result = identite_integration_container.create_candidat_usecase().execute(
        input_data
    )

    assert result.email == input_data.email
    assert result.prenom == input_data.prenom
    assert result.nom == input_data.nom
    assert result.resume == input_data.resume


def test_create_candidat_with_existing_user(identite_integration_container):
    existing_user = UtilisateurFactory.create_model(email=fake.email())
    input_data = CreateCandidatInput(
        email=existing_user.email,
        prenom=fake.first_name(),
        nom=fake.last_name(),
        resume=fake.text(max_nb_chars=200),
    )

    result = identite_integration_container.create_candidat_usecase().execute(
        input_data
    )

    assert str(result.entity_id) == existing_user.username


def test_cannot_create_candidat_twice(identite_integration_container):
    existing_candidat = CandidatFactory.create_model()
    input_data = CreateCandidatInput(
        email=existing_candidat.utilisateur.email,
        prenom=fake.first_name(),
        nom=fake.last_name(),
        resume=fake.text(max_nb_chars=200),
    )

    with pytest.raises(ProfilCandidatAlreadyExists):
        identite_integration_container.create_candidat_usecase().execute(input_data)
