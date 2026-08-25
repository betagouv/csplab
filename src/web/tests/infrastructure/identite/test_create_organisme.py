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


def test_get_by_referentiel_and_external_id(identite_integration_container):
    model = OrganismeFactory.create_model(
        nom="Ministère de la Justice", referentiel="FINESS", external_id="ext-123"
    )
    repo = identite_integration_container.postgres_organisme_repository()

    organisme = repo.get_by_referentiel_and_external_id(
        referentiel="FINESS", external_id="ext-123"
    )

    assert organisme is not None
    assert organisme.entity_id == model.id
    assert organisme.nom == "Ministère de la Justice"


def test_get_by_referentiel_and_external_id_nexiste_pas(
    identite_integration_container,
):
    repo = identite_integration_container.postgres_organisme_repository()

    organisme = repo.get_by_referentiel_and_external_id(
        referentiel="FINESS", external_id="unknown"
    )

    assert organisme is None


def test_save_updates_existing_organisme(identite_integration_container):
    model = OrganismeFactory.create_model(
        nom="Ancien nom", referentiel="FINESS", external_id="ext-456"
    )
    repo = identite_integration_container.postgres_organisme_repository()
    organisme = repo.get_by_id(model.id)

    organisme.modifier(
        nom="Nouveau nom",
        versant=organisme.versant,
        localisation=organisme.localisation,
        siret=organisme.siret,
        parent_id=organisme.parent_id,
        external_id=organisme.external_id,
        referentiel=organisme.referentiel,
    )
    repo.save(organisme)

    updated = repo.get_by_id(model.id)
    assert updated.nom == "Nouveau nom"


def test_save_preserves_created_at_and_etapes(identite_integration_container):
    etapes = [{"entity_id": str(uuid4()), "categorie": "AUTRE", "nom": "Tri CV"}]
    model = OrganismeFactory.create_model(nom="Ancien nom")
    model.etapes = etapes
    model.save()
    created_at_before = model.created_at
    repo = identite_integration_container.postgres_organisme_repository()
    organisme = repo.get_by_id(model.id)

    organisme.modifier(
        nom="Nouveau nom",
        versant=organisme.versant,
        localisation=organisme.localisation,
        siret=organisme.siret,
        parent_id=organisme.parent_id,
        external_id=organisme.external_id,
        referentiel=organisme.referentiel,
    )
    repo.save(organisme)

    model.refresh_from_db()
    assert model.nom == "Nouveau nom"
    assert model.etapes == etapes
    assert model.created_at == created_at_before


def test_save_organisme_inexistant_leve_organisme_nexiste_pas(
    identite_integration_container,
):
    organisme = OrganismeFactory.create_entity()
    repo = identite_integration_container.postgres_organisme_repository()

    with pytest.raises(OrganismeNexistePas):
        repo.save(organisme)
