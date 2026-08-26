from unittest.mock import MagicMock
from uuid import uuid4

from referentiel.events.organisme_events import OrganismeCree, OrganismeRemplace
from referentiel.value_objects.siret import SIRET
from referentiel.value_objects.verse import Verse

from application.ingestion.interfaces.upsert_organismes_input import (
    OrganismeUpsertData,
    UpsertOrganismesInput,
)
from application.ingestion.usecases.upsert_organismes import UpsertOrganismesUsecase


def _organisme_data(**overrides) -> OrganismeUpsertData:
    defaults = {
        "nom": "Commune de Paris",
        "versant": Verse.FPT,
        "siret": SIRET(code="19754687200015"),
        "localisation": None,
        "parent_id": None,
        "external_id": "ext-123",
        "referentiel": "FINESS",
        "millesime": "2026-08-19",
    }
    defaults.update(overrides)
    return OrganismeUpsertData(**defaults)


def _usecase(organisme_repository=None) -> UpsertOrganismesUsecase:
    return UpsertOrganismesUsecase(
        organisme_repository=organisme_repository or MagicMock(),
        logger=MagicMock(),
    )


def test_creates_organisme_when_not_found():
    organisme_repository = MagicMock()
    organisme_repository.get_ids_by_referentiel_and_external_id.return_value = {}
    organisme_repository.upsert_batch.return_value = {
        "created": 1,
        "updated": 0,
        "errors": [],
    }
    usecase = _usecase(organisme_repository)

    result = usecase.execute(UpsertOrganismesInput(organismes=[_organisme_data()]))

    assert result == {"created": 1, "updated": 0, "errors": []}
    organismes = organisme_repository.upsert_batch.call_args[0][0]
    assert len(organismes) == 1
    events = organismes[0].collect_events()
    assert len(events) == 1
    assert isinstance(events[0], OrganismeCree)


def test_updates_existing_organisme_found_by_referentiel_and_external_id():
    existing_id = uuid4()
    organisme_repository = MagicMock()
    organisme_repository.get_ids_by_referentiel_and_external_id.return_value = {
        ("FINESS", "ext-123"): existing_id
    }
    organisme_repository.upsert_batch.return_value = {
        "created": 0,
        "updated": 1,
        "errors": [],
    }
    usecase = _usecase(organisme_repository)

    result = usecase.execute(
        UpsertOrganismesInput(organismes=[_organisme_data(nom="Nouveau nom")])
    )

    assert result == {"created": 0, "updated": 1, "errors": []}
    organismes = organisme_repository.upsert_batch.call_args[0][0]
    assert len(organismes) == 1
    assert organismes[0].entity_id == existing_id
    assert organismes[0].nom == "Nouveau nom"
    events = organismes[0].collect_events()
    assert len(events) == 1
    assert isinstance(events[0], OrganismeRemplace)


def test_looks_up_all_pairs_in_a_single_batch_call():
    organisme_repository = MagicMock()
    organisme_repository.get_ids_by_referentiel_and_external_id.return_value = {}
    organisme_repository.upsert_batch.return_value = {
        "created": 2,
        "updated": 0,
        "errors": [],
    }
    usecase = _usecase(organisme_repository)

    usecase.execute(
        UpsertOrganismesInput(
            organismes=[
                _organisme_data(external_id="ext-1", referentiel="FINESS"),
                _organisme_data(external_id="ext-2", referentiel="RNE"),
            ]
        )
    )

    organisme_repository.get_ids_by_referentiel_and_external_id.assert_called_once_with(
        [("FINESS", "ext-1"), ("RNE", "ext-2")]
    )


def test_returns_errors_from_the_batch_upsert():
    organisme_repository = MagicMock()
    organisme_repository.get_ids_by_referentiel_and_external_id.return_value = {}
    organisme_repository.upsert_batch.return_value = {
        "created": 0,
        "updated": 0,
        "errors": [{"entity_id": None, "error": "db error", "exception": None}],
    }
    usecase = _usecase(organisme_repository)

    result = usecase.execute(UpsertOrganismesInput(organismes=[_organisme_data()]))

    assert result["errors"] == [
        {"entity_id": None, "error": "db error", "exception": None}
    ]
