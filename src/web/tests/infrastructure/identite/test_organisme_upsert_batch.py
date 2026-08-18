from uuid import uuid4

import pytest
from referentiel.value_objects.verse import Verse

from domain.commons.errors.organisme_errors import OrganismeNexistePas
from domain.identite.entities.organisme import Organisme
from domain.identite.value_objects.siret import SIRET
from infrastructure.django_apps.recruteur.models.organisme import OrganismeModel
from infrastructure.exceptions.exceptions import DatabaseError
from infrastructure.factories.identite.organisme_factory import OrganismeFactory
from infrastructure.repositories.identite.postgres_organisme_repository import (
    PostgresOrganismeRepository,
)


@pytest.fixture(name="repository")
def repository_fixture():
    return PostgresOrganismeRepository()


def test_upsert_batch_creates_new_organismes(db, repository):
    organisme = Organisme.build(
        entity_id=uuid4(),
        nom="Clinique du Docteur Convert",
        versant=Verse.FPH,
        localisation=None,
        siret=SIRET("77220148900022"),
        parent_id=None,
        external_id="010780195",
        referentiel="FINESS",
        millesime="2026-08-18",
        gestion_ats=True,
    )

    result = repository.upsert_batch([organisme])

    assert result == {"created": 1, "updated": 0, "errors": []}
    model = OrganismeModel.objects.get(siret="77220148900022")
    assert model.nom == "Clinique du Docteur Convert"
    assert model.referentiel == "FINESS"
    assert model.gestion_ats is True


def test_upsert_batch_updates_existing_organisme_by_siret(db, repository):
    parent_id = uuid4()
    existing_model = OrganismeFactory.create_model(
        nom="Ancien nom",
        siret=SIRET("77220148900022"),
        external_id="010780195",
        referentiel="FINESS",
        millesime="2026-08-17",
        gestion_ats=False,
    )
    existing_model.parent_id = parent_id
    existing_model.save()

    updated_organisme = Organisme.build(
        entity_id=uuid4(),
        nom="Nouveau nom",
        versant=Verse.FPH,
        localisation=None,
        siret=SIRET("77220148900022"),
        parent_id=None,
        external_id="010780195",
        referentiel="FINESS",
        millesime="2026-08-18",
        gestion_ats=True,
    )

    result = repository.upsert_batch([updated_organisme])

    assert result == {"created": 0, "updated": 1, "errors": []}
    model = OrganismeModel.objects.get(siret="77220148900022")
    assert model.id == existing_model.id
    assert model.nom == "Nouveau nom"
    assert model.millesime == "2026-08-18"
    # gestion_ats is (re)asserted by the import.
    assert model.gestion_ats is True
    # parent_id is managed manually and never touched by the import.
    assert model.parent_id == parent_id


def test_get_by_siret_returns_organisme(db, repository):
    model = OrganismeFactory.create_model(
        nom="Ministère de la Justice", siret=SIRET("77220148900022")
    )

    organisme = repository.get_by_siret(SIRET("77220148900022"))

    assert organisme.entity_id == model.id
    assert organisme.nom == "Ministère de la Justice"


def test_get_by_siret_nexiste_pas(db, repository):
    with pytest.raises(OrganismeNexistePas):
        repository.get_by_siret(SIRET("77220148900022"))


def test_upsert_batch_raises_database_error_on_failure(db, repository):
    organisme = Organisme.build(
        entity_id=uuid4(),
        nom="x" * 300,  # exceeds the 255-char column limit
        versant=Verse.FPH,
        localisation=None,
        siret=SIRET("77220148900022"),
        parent_id=None,
    )

    with pytest.raises(DatabaseError):
        repository.upsert_batch([organisme])
