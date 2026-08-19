from unittest.mock import AsyncMock, MagicMock

import pytest
from referentiel.value_objects.siret import SIRET
from referentiel.value_objects.verse import Verse

from application.use_cases.clean_raw_organismes import (
    BATCH_SIZE,
    CleanRawOrganismesUseCase,
)
from domain.entities.organisme import Organisme
from domain.entities.raw_organisme import RawOrganisme
from domain.gateways.organismes_cleaner import IOrganismesCleaner
from domain.repositories.raw_organisme_repository import IRawOrganismeRepository

REFERENTIEL = "FINESS"


def _raw_organismes(count: int) -> list[RawOrganisme]:
    return [
        RawOrganisme(
            referentiel=REFERENTIEL,
            millesime="2026-08-19",
            external_id=str(i),
            data={"i": i},
        )
        for i in range(count)
    ]


def _organisme() -> Organisme:
    return Organisme(
        nom="Test",
        versant=Verse.FPH,
        siret=SIRET(code="26060047300342"),
    )


@pytest.fixture
def mock_cleaner() -> MagicMock:
    return MagicMock(spec=IOrganismesCleaner)


@pytest.fixture
def mock_repo() -> MagicMock:
    repo = MagicMock(spec=IRawOrganismeRepository)
    repo.find_uncleaned = AsyncMock()
    repo.mark_as_cleaned_batch = AsyncMock()
    return repo


@pytest.fixture
def use_case(mock_cleaner, mock_repo) -> CleanRawOrganismesUseCase:
    return CleanRawOrganismesUseCase(
        organismes_cleaner=mock_cleaner, raw_organisme_repository=mock_repo
    )


@pytest.mark.asyncio
async def test_single_partial_batch_stops_after_one_fetch(
    use_case, mock_cleaner, mock_repo
):
    mock_repo.find_uncleaned.return_value = _raw_organismes(3)
    mock_cleaner.clean.return_value = _organisme()

    result = await use_case.execute(REFERENTIEL)

    assert mock_repo.find_uncleaned.call_count == 1
    assert len(result) == 3
    mock_repo.mark_as_cleaned_batch.assert_called_once()


@pytest.mark.asyncio
async def test_fetches_again_when_batch_is_full(use_case, mock_cleaner, mock_repo):
    mock_repo.find_uncleaned.side_effect = [_raw_organismes(BATCH_SIZE), []]
    mock_cleaner.clean.return_value = _organisme()

    result = await use_case.execute(REFERENTIEL)

    assert mock_repo.find_uncleaned.call_count == 2
    assert len(result) == BATCH_SIZE
    assert mock_repo.mark_as_cleaned_batch.call_count == 1


@pytest.mark.asyncio
async def test_marks_all_fetched_ids_as_cleaned(use_case, mock_cleaner, mock_repo):
    raw_batch = _raw_organismes(2)
    mock_repo.find_uncleaned.return_value = raw_batch
    mock_cleaner.clean.return_value = _organisme()

    await use_case.execute(REFERENTIEL)

    cleaned_ids = mock_repo.mark_as_cleaned_batch.call_args.args[0]
    assert cleaned_ids == [raw.id for raw in raw_batch]


@pytest.mark.asyncio
async def test_filtered_out_organismes_are_not_returned_but_marked_cleaned(
    use_case, mock_cleaner, mock_repo
):
    raw_batch = _raw_organismes(2)
    mock_repo.find_uncleaned.return_value = raw_batch
    mock_cleaner.clean.return_value = None

    result = await use_case.execute(REFERENTIEL)

    assert result == []
    mock_repo.mark_as_cleaned_batch.assert_called_once()
    cleaned_ids = mock_repo.mark_as_cleaned_batch.call_args.args[0]
    assert cleaned_ids == [raw.id for raw in raw_batch]


@pytest.mark.asyncio
async def test_cleaner_error_is_skipped_but_still_marked_cleaned(
    use_case, mock_cleaner, mock_repo
):
    raw_batch = _raw_organismes(2)
    mock_repo.find_uncleaned.return_value = raw_batch
    mock_cleaner.clean.side_effect = [ValueError("boom"), _organisme()]

    result = await use_case.execute(REFERENTIEL)

    assert len(result) == 1
    cleaned_ids = mock_repo.mark_as_cleaned_batch.call_args.args[0]
    assert cleaned_ids == [raw.id for raw in raw_batch]


@pytest.mark.asyncio
async def test_no_uncleaned_organismes_does_not_mark_cleaned(
    use_case, mock_cleaner, mock_repo
):
    mock_repo.find_uncleaned.return_value = []

    result = await use_case.execute(REFERENTIEL)

    assert result == []
    mock_repo.mark_as_cleaned_batch.assert_not_called()
