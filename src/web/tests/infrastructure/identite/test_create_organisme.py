from unittest.mock import Mock

import pytest
from referentiel.value_objects.siret import SIRET
from referentiel.value_objects.verse import Verse

from application.identite.usecases.create_organisme import CreateOrganismeCommand
from config.app_config import AppConfig
from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.identite.errors.organisme_errors import OrganismeSiretExisteDeja
from domain.identite.errors.organisme_permission_errors import (
    OperationOrganismeRefusee,
)
from infrastructure.di.identite.identite_container import IdentiteContainer
from infrastructure.factories.identite.organisme_factory import OrganismeFactory
from infrastructure.factories.identite.utilisateur_factory import UtilisateurFactory
from infrastructure.gateways.shared.logger import LoggerService


@pytest.fixture(name="identite_integration_container")
def identite_integration_container_fixture(db):
    container = IdentiteContainer()
    app_config = AppConfig.from_django_settings()
    logger_service = LoggerService()
    container.app_config.override(app_config)
    container.logger_service.override(logger_service)
    container.audit_log_writer.override(Mock(spec=AuditLogWriter))
    return container


def test_create_organisme(db, identite_integration_container):
    command = CreateOrganismeCommand(
        name="Commune de Paris",
        verse=Verse.FPT,
        localisation=None,
        siret=SIRET(code="19754687200015"),
        parent_id=None,
        utilisateur=UtilisateurFactory.create_entity(is_staff=True),
    )

    organisme = identite_integration_container.create_organisme_usecase().execute(
        command
    )

    assert organisme.nom == "Commune de Paris"
    assert organisme.versant == Verse.FPT
    assert organisme.entity_id is not None
    assert organisme.siret == SIRET(code="19754687200015")
    assert not organisme.gestion_ats


def test_create_organisme_refuse_non_staff(db, identite_integration_container):
    command = CreateOrganismeCommand(
        name="Commune de Paris",
        verse=Verse.FPT,
        localisation=None,
        siret=SIRET(code="19754687200015"),
        parent_id=None,
        utilisateur=UtilisateurFactory.create_entity(is_staff=False),
    )

    with pytest.raises(OperationOrganismeRefusee):
        identite_integration_container.create_organisme_usecase().execute(command)


def test_raise_siret_already_exists(db, identite_integration_container):
    organisme = OrganismeFactory.create_model()
    command = CreateOrganismeCommand(
        name=organisme.nom,
        verse=organisme.versant,
        localisation=organisme.localisation,
        siret=organisme.siret,
        parent_id=organisme.parent_id,
        utilisateur=UtilisateurFactory.create_entity(is_staff=True),
    )

    with pytest.raises(OrganismeSiretExisteDeja):
        identite_integration_container.create_organisme_usecase().execute(command)
