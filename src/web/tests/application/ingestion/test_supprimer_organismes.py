from unittest.mock import MagicMock
from uuid import uuid4

from referentiel.entities.organisme import Organisme
from referentiel.value_objects.siret import SIRET
from referentiel.value_objects.verse import Verse

from application.ingestion.interfaces.supprimer_organismes_input import (
    OrganismeDeleteData,
    SupprimerOrganismesInput,
)
from application.ingestion.usecases.supprimer_organismes import (
    SupprimerOrganismesUsecase,
)


def _organisme_data(**overrides) -> OrganismeDeleteData:
    defaults = {"referentiel": "FINESS", "external_id": "ext-123"}
    defaults.update(overrides)
    return OrganismeDeleteData(**defaults)


def _organisme_entity(**overrides) -> Organisme:
    defaults = {
        "entity_id": uuid4(),
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
    return Organisme.build(**defaults)


def _usecase(organisme_repository=None) -> SupprimerOrganismesUsecase:
    return SupprimerOrganismesUsecase(
        organisme_repository=organisme_repository or MagicMock(),
    )


def test_deletes_organismes_via_the_repository():
    organisme = _organisme_entity()
    organisme_repository = MagicMock()
    organisme_repository.get_by_referentiel_and_external_id_batch.return_value = {
        ("FINESS", "ext-123"): organisme
    }
    organisme_repository.supprimer_batch.return_value = 1
    usecase = _usecase(organisme_repository)

    result = usecase.execute(SupprimerOrganismesInput(organismes=[_organisme_data()]))

    assert result == {"deleted": 1, "not_found": []}
    deleted_organismes = organisme_repository.supprimer_batch.call_args[0][0]
    assert deleted_organismes == [organisme]


def test_looks_up_all_pairs_in_a_single_batch_call():
    organisme_repository = MagicMock()
    organisme_repository.get_by_referentiel_and_external_id_batch.return_value = {}
    organisme_repository.supprimer_batch.return_value = 0
    usecase = _usecase(organisme_repository)

    usecase.execute(
        SupprimerOrganismesInput(
            organismes=[
                _organisme_data(external_id="ext-1", referentiel="FINESS"),
                _organisme_data(external_id="ext-2", referentiel="RNE"),
            ]
        )
    )

    organisme_repository.get_by_referentiel_and_external_id_batch.assert_called_once_with(
        [("FINESS", "ext-1"), ("RNE", "ext-2")]
    )


def test_returns_unknown_pairs_as_not_found_and_does_not_emit_events_for_them():
    organisme_repository = MagicMock()
    organisme_repository.get_by_referentiel_and_external_id_batch.return_value = {}
    organisme_repository.supprimer_batch.return_value = 0
    usecase = _usecase(organisme_repository)

    result = usecase.execute(SupprimerOrganismesInput(organismes=[_organisme_data()]))

    assert result == {
        "deleted": 0,
        "not_found": [{"referentiel": "FINESS", "external_id": "ext-123"}],
    }
    organisme_repository.supprimer_batch.assert_called_once_with([])
