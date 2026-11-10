from unittest.mock import Mock

import pytest

from config.app_config import AppConfig
from domain.commons.services.audit_log_writer import AuditLogWriter
from infrastructure.di.identite.identite_container import IdentiteContainer
from infrastructure.django_apps.recruteur.models.organisme import OrganismeModel
from infrastructure.factories.identite.organisme_django_factory import (
    OrganismeDjangoFactory,
)
from infrastructure.factories.identite.organisme_factory import OrganismeFactory
from infrastructure.gateways.shared.logger import LoggerService
from infrastructure.mappers.organisme_identite_mapper import OrganismeIdentiteMapper


@pytest.fixture(name="identite_integration_container")
def identite_integration_container_fixture(db):
    container = IdentiteContainer()
    app_config = AppConfig.from_django_settings()
    logger_service = LoggerService()
    container.app_config.override(app_config)
    container.logger_service.override(logger_service)
    container.audit_log_writer.override(Mock(spec=AuditLogWriter))
    return container


def test_get_ids_by_referentiel_and_external_id_batch(identite_integration_container):
    model_a = OrganismeDjangoFactory(referentiel="FINESS", external_id="ext-a")
    model_b = OrganismeDjangoFactory(referentiel="RNE", external_id="ext-b")
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
    existing = OrganismeDjangoFactory(
        nom="Ancien nom", referentiel="FINESS", external_id="ext-existing"
    )
    repo = identite_integration_container.postgres_organisme_repository()

    organisme_modifie = OrganismeIdentiteMapper().to_domain(existing)
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
    assert OrganismeModel.objects.get(pk=existing.id).nom == "Nouveau nom"
    assert OrganismeModel.objects.get(pk=organisme_nouveau.entity_id).nom == (
        "Organisme neuf"
    )
