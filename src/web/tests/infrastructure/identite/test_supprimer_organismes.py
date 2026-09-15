from infrastructure.factories.identite.organisme_django_factory import (
    OrganismeDjangoFactory,
)
from infrastructure.repositories.identite.postgres_organisme_repository import (
    PostgresOrganismeRepository,
)


def test_get_by_referentiel_and_external_id_batch_returns_matching_organismes(db):
    organisme_model = OrganismeDjangoFactory(
        referentiel="FINESS", external_id="ext-123"
    )
    repository = PostgresOrganismeRepository()

    result = repository.get_by_referentiel_and_external_id_batch(
        [("FINESS", "ext-123")]
    )

    assert set(result.keys()) == {("FINESS", "ext-123")}
    assert result[("FINESS", "ext-123")].entity_id == organisme_model.id


def test_get_by_referentiel_and_external_id_batch_excludes_already_deleted(db):
    OrganismeDjangoFactory(
        referentiel="FINESS",
        external_id="ext-123",
        supprime_le="2026-01-01T00:00:00Z",
    )
    repository = PostgresOrganismeRepository()

    result = repository.get_by_referentiel_and_external_id_batch(
        [("FINESS", "ext-123")]
    )

    assert result == {}


def test_get_by_referentiel_and_external_id_batch_returns_empty_dict_for_no_pairs(db):
    repository = PostgresOrganismeRepository()

    assert repository.get_by_referentiel_and_external_id_batch([]) == {}


def test_supprimer_batch_soft_deletes_matching_organismes(db):
    organisme_model = OrganismeDjangoFactory(
        referentiel="FINESS", external_id="ext-123"
    )
    repository = PostgresOrganismeRepository()
    organisme = repository.get_by_referentiel_and_external_id_batch(
        [("FINESS", "ext-123")]
    )[("FINESS", "ext-123")]

    deleted = repository.supprimer_batch([organisme])

    organisme_model.refresh_from_db()
    assert deleted == 1
    assert organisme_model.supprime_le is not None


def test_supprimer_batch_does_not_hard_delete(db):
    organisme_model = OrganismeDjangoFactory(
        referentiel="FINESS", external_id="ext-123"
    )
    repository = PostgresOrganismeRepository()
    organisme = repository.get_by_referentiel_and_external_id_batch(
        [("FINESS", "ext-123")]
    )[("FINESS", "ext-123")]

    repository.supprimer_batch([organisme])

    assert type(organisme_model).objects.filter(id=organisme_model.id).exists()


def test_supprimer_batch_returns_zero_for_empty_list(db):
    repository = PostgresOrganismeRepository()

    assert repository.supprimer_batch([]) == 0
