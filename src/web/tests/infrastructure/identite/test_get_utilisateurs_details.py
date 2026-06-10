import pytest
from faker import Faker

from config.app_config import AppConfig
from domain.identite.errors.identite_errors import UtilisateurDoesNotExist
from infrastructure.di.identite.identite_container import IdentiteContainer
from infrastructure.gateways.shared.logger import LoggerService

fake = Faker()


@pytest.fixture(name="identite_integration_container")
def identite_integration_container_fixture(db):
    container = IdentiteContainer()
    app_config = AppConfig.from_django_settings()
    logger_service = LoggerService()
    container.app_config.override(app_config)
    container.logger_service.override(logger_service)
    return container


def test_get_existing_user(db, test_user, identite_integration_container):
    usecase = identite_integration_container.get_utilisateur_details_usecase()
    result = usecase.execute(test_user.username)

    assert result == test_user.to_entity()


def test_get_unknown_uuid(db, identite_integration_container):
    usecase = identite_integration_container.get_utilisateur_details_usecase()

    with pytest.raises(UtilisateurDoesNotExist):
        usecase.execute(str(fake.uuid4()))
