from unittest.mock import MagicMock

import pytest

from application.ingestion.interfaces.supprimer_organismes_input import (
    OrganismeDeleteData,
    SupprimerOrganismesInput,
)
from application.ingestion.usecases.supprimer_organismes import (
    SupprimerOrganismesUsecase,
)
from infrastructure.factories.identite.organisme_django_factory import (
    OrganismeDjangoFactory,
)
from infrastructure.repositories.identite.postgres_organisme_repository import (
    PostgresOrganismeRepository,
)


def _organisme_data(**overrides) -> OrganismeDeleteData:
    defaults = {"referentiel": "FINESS", "external_id": "ext-123"}
    defaults.update(overrides)
    return OrganismeDeleteData(**defaults)


@pytest.mark.django_db
def test_deletes_organismes_via_the_repository():
    organisme = OrganismeDjangoFactory(referentiel="FINESS", external_id="ext-123")
    usecase = SupprimerOrganismesUsecase(
        organisme_repository=PostgresOrganismeRepository()
    )

    result = usecase.execute(SupprimerOrganismesInput(organismes=[_organisme_data()]))

    assert result == {"deleted": 1, "not_found": []}
    organisme.refresh_from_db()
    assert organisme.supprime_le is not None


def test_looks_up_all_pairs_in_a_single_batch_call():
    organisme_repository = MagicMock()
    organisme_repository.get_by_referentiel_and_external_id_batch.return_value = {}
    organisme_repository.supprimer_batch.return_value = 0
    usecase = SupprimerOrganismesUsecase(organisme_repository=organisme_repository)

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
