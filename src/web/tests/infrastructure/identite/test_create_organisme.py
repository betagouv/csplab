from uuid import uuid4

import pytest
from referentiel.value_objects.verse import Verse

from application.identite.usecases.create_organisme import CreateOrganismeCommand
from config.app_config import AppConfig
from domain.identite.errors.organisme_errors import OrganismeNexistePas
from domain.identite.value_objects.siret import SIRET
from infrastructure.di.identite.identite_container import IdentiteContainer
from infrastructure.factories.identite.organisme_factory import OrganismeFactory
from infrastructure.gateways.shared.logger import LoggerService


@pytest.fixture(name="identite_integration_container")
def identite_integration_container_fixture(db):
    container = IdentiteContainer()
    app_config = AppConfig.from_django_settings()
    logger_service = LoggerService()
    container.app_config.override(app_config)
    container.logger_service.override(logger_service)
    return container


def test_create_organisme(identite_integration_container):
    command = CreateOrganismeCommand(
        nom="Commune de Paris",
        versant=Verse.FPT,
        localisation=None,
        siret=SIRET("19754687200015"),
        parent_id=None,
    )

    organisme = identite_integration_container.create_organisme_usecase().execute(
        command
    )

    assert organisme.nom == "Commune de Paris"
    assert organisme.versant == Verse.FPT
    assert organisme.entity_id is not None
    assert organisme.siret == SIRET("19754687200015")


def test_create_organisme_avec_siret(identite_integration_container):

    command = CreateOrganismeCommand(
        nom="Ecole du Louvre",
        versant=Verse.FPE,
        localisation=None,
        siret=SIRET("19754687200015"),
        parent_id=None,
    )

    organisme = identite_integration_container.create_organisme_usecase().execute(
        command
    )

    assert organisme.siret == SIRET("19754687200015")


def test_get_organisme_by_id(identite_integration_container):
    model = OrganismeFactory.create_model(nom="Ministère de la Justice")
    repo = identite_integration_container.postgres_organisme_repository()

    organisme = repo.get_by_id(model.id)

    assert organisme.nom == "Ministère de la Justice"
    assert organisme.entity_id == model.id


def test_get_organisme_by_id_nexiste_pas(identite_integration_container):
    repo = identite_integration_container.postgres_organisme_repository()

    with pytest.raises(OrganismeNexistePas):
        repo.get_by_id(uuid4())
