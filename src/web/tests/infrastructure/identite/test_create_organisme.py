from unittest.mock import Mock
from uuid import uuid4

import pytest
from referentiel.value_objects.siret import SIRET
from referentiel.value_objects.verse import Verse

from application.identite.usecases.create_organisme import CreateOrganismeCommand
from config.app_config import AppConfig
from domain.commons.errors.organisme_errors import OrganismeNexistePas
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


def test_save_updates_existing_organisme(identite_integration_container):
    model = OrganismeFactory.create_model(
        nom="Ancien nom", referentiel="FINESS", external_id="ext-456"
    )
    repo = identite_integration_container.postgres_organisme_repository()
    organisme = repo.get_by_id(model.id)

    organisme.remplacer(
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

    organisme.remplacer(
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


def test_get_ids_by_referentiel_and_external_id_batch(identite_integration_container):
    model_a = OrganismeFactory.create_model(referentiel="FINESS", external_id="ext-a")
    model_b = OrganismeFactory.create_model(referentiel="RNE", external_id="ext-b")
    repo = identite_integration_container.postgres_organisme_repository()

    ids = repo.get_ids_by_referentiel_and_external_id(
        [("FINESS", "ext-a"), ("RNE", "ext-b"), ("RNE", "unknown")]
    )

    assert ids == {
        ("FINESS", "ext-a"): model_a.id,
        ("RNE", "ext-b"): model_b.id,
    }


def test_get_ids_by_referentiel_and_external_id_batch_vide(
    identite_integration_container,
):
    repo = identite_integration_container.postgres_organisme_repository()

    assert repo.get_ids_by_referentiel_and_external_id([]) == {}


def test_upsert_batch_cree_et_met_a_jour(identite_integration_container):
    existing = OrganismeFactory.create_model(
        nom="Ancien nom", referentiel="FINESS", external_id="ext-existing"
    )
    repo = identite_integration_container.postgres_organisme_repository()

    organisme_modifie = repo.get_by_id(existing.id)
    organisme_modifie.remplacer(
        nom="Nouveau nom",
        versant=organisme_modifie.versant,
        localisation=organisme_modifie.localisation,
        siret=organisme_modifie.siret,
        parent_id=organisme_modifie.parent_id,
        external_id=organisme_modifie.external_id,
        referentiel=organisme_modifie.referentiel,
    )
    organisme_nouveau = OrganismeFactory.create_entity(
        nom="Organisme neuf", referentiel="FINESS", external_id="ext-neuf"
    )

    result = repo.upsert_batch([organisme_modifie, organisme_nouveau])

    assert result == {"created": 1, "updated": 1, "errors": []}
    assert repo.get_by_id(existing.id).nom == "Nouveau nom"
    assert repo.get_by_id(organisme_nouveau.entity_id).nom == "Organisme neuf"
