import pytest

from application.recruteur.usecases.get_organisme_recruteur import (
    GetOrganismeRecruteurQuery,
)
from application.recruteur.usecases.initialize_organisme_steps import (
    InitializeOrganismeStepsCommand,
)
from config.app_config import AppConfig
from infrastructure.di.recruteur.recruteur_container import RecruteurContainer
from infrastructure.gateways.shared.logger import LoggerService
from tests.factories.identite.organisme_factory import OrganismeFactory

NB_ETAPES_PAR_DEFAUT = 6


@pytest.fixture(name="recruteur_integration_container")
def recruteur_integration_container_fixture(db):
    container = RecruteurContainer()
    app_config = AppConfig.from_django_settings()
    logger_service = LoggerService()
    container.app_config.override(app_config)
    container.logger_service.override(logger_service)
    return container


def test_get_organisme_steps(recruteur_integration_container):
    organisme_model = OrganismeFactory.create_model()
    organisme_model.save()
    usecase = recruteur_integration_container.get_organisme_recruteur_usecase()

    organisme = usecase.execute(command=GetOrganismeRecruteurQuery(organisme_model.id))
    events = organisme.collect_events()
    assert len(events) == 0
    assert organisme.entity_id == organisme_model.id


def test_initialize_organisme_steps(recruteur_integration_container):
    organisme_model = OrganismeFactory.create_model()
    usecase = recruteur_integration_container.initialize_organisme_steps_usecase()

    organisme = usecase.execute(
        command=InitializeOrganismeStepsCommand(organisme_id=organisme_model.id)
    )

    events = organisme.collect_events()
    assert len(events) == 1
    assert organisme.etapes is not None
    assert len(organisme.etapes) == NB_ETAPES_PAR_DEFAUT
