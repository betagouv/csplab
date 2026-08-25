from unittest.mock import MagicMock

from referentiel.events.organisme_events import OrganismeCree, OrganismeRemplace
from referentiel.value_objects.siret import SIRET
from referentiel.value_objects.verse import Verse

from application.ingestion.interfaces.upsert_organismes_input import (
    OrganismeUpsertData,
    UpsertOrganismesInput,
)
from application.ingestion.usecases.upsert_organismes import UpsertOrganismesUsecase
from infrastructure.factories.identite.organisme_factory import OrganismeFactory


def _organisme_data(**overrides) -> OrganismeUpsertData:
    defaults = {
        "nom": "Commune de Paris",
        "versant": Verse.FPT,
        "siret": SIRET(code="19754687200015"),
        "localisation": None,
        "external_id": "ext-123",
        "referentiel": "FINESS",
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
    organisme_repository.get_by_referentiel_and_external_id.return_value = None
    usecase = _usecase(organisme_repository)

    result = usecase.execute(UpsertOrganismesInput(organismes=[_organisme_data()]))

    assert result == {"created": 1, "updated": 0, "errors": []}
    organisme_repository.create.assert_called_once()
    created_organisme = organisme_repository.create.call_args[0][0]
    events = created_organisme.collect_events()
    assert len(events) == 1
    assert isinstance(events[0], OrganismeCree)


def test_updates_existing_organisme_found_by_referentiel_and_external_id():
    existing = OrganismeFactory.create_entity(
        nom="Ancien nom", external_id="ext-123", referentiel="FINESS"
    )
    organisme_repository = MagicMock()
    organisme_repository.get_by_referentiel_and_external_id.return_value = existing
    usecase = _usecase(organisme_repository)

    result = usecase.execute(
        UpsertOrganismesInput(organismes=[_organisme_data(nom="Nouveau nom")])
    )

    assert result == {"created": 0, "updated": 1, "errors": []}
    organisme_repository.create.assert_not_called()
    organisme_repository.save.assert_called_once_with(existing)
    assert existing.nom == "Nouveau nom"
    events = existing.collect_events()
    assert len(events) == 1
    assert isinstance(events[0], OrganismeRemplace)


def test_does_not_lookup_when_referentiel_or_external_id_missing():
    organisme_repository = MagicMock()
    usecase = _usecase(organisme_repository)

    result = usecase.execute(
        UpsertOrganismesInput(
            organismes=[_organisme_data(external_id=None, referentiel=None)]
        )
    )

    assert result == {"created": 1, "updated": 0, "errors": []}
    organisme_repository.get_by_referentiel_and_external_id.assert_not_called()
    organisme_repository.create.assert_called_once()


def test_collects_error_for_failing_item_without_stopping_the_batch():
    organisme_repository = MagicMock()
    organisme_repository.get_by_referentiel_and_external_id.return_value = None
    organisme_repository.create.side_effect = [Exception("db error"), None]
    usecase = _usecase(organisme_repository)

    result = usecase.execute(
        UpsertOrganismesInput(
            organismes=[
                _organisme_data(external_id="ext-1"),
                _organisme_data(external_id="ext-2"),
            ]
        )
    )

    assert result["created"] == 1
    assert result["updated"] == 0
    assert result["errors"] == [
        {"referentiel": "FINESS", "external_id": "ext-1", "error": "db error"}
    ]
