from unittest.mock import MagicMock

import pytest
from referentiel.entities.organisme import Organisme
from sqlmodel import Session, select

from application.usecases.clean_raw_organismes import (
    BATCH_SIZE,
    CleanRawOrganismesUsecase,
)
from domain.entities.raw_organisme import RawOrganisme
from domain.gateways.organismes_cleaner import IOrganismesCleaner
from infrastructure.gateways.organismes_cleaner import OrganismesCleaner
from infrastructure.models.raw_organisme import RawOrganismeModel

pytestmark = pytest.mark.usefixtures("clean_db")

REFERENTIEL = "FINESS"
SIRET_VALUE = "26060047300342"
ALLOWED_CATEGORIE = "101"
DISALLOWED_CATEGORIE = "999"


def _ege(*, categorie: str = ALLOWED_CATEGORIE, external_id: str) -> dict:
    return {
        "categorieentiteGeographiqueExercice": categorie,
        "informationsGeneralesEGE": {
            "nomEgeLong": f"ORGANISME {external_id}",
            "siret": SIRET_VALUE,
        },
        "adresse": [
            {
                "cogCommune": "06088",
                "coordonneesGeographique": {
                    "coordonneeX": "7.254944",
                    "coordonneeY": "43.697073",
                },
            }
        ],
    }


def _raw_organismes(
    count: int, *, categorie: str = ALLOWED_CATEGORIE
) -> list[RawOrganisme]:
    return [
        RawOrganisme(
            referentiel=REFERENTIEL,
            millesime="2026-08-19",
            external_id=str(i),
            data=_ege(categorie=categorie, external_id=str(i)),
        )
        for i in range(count)
    ]


def _fetch_all(db_engine) -> list[RawOrganismeModel]:
    with Session(db_engine) as session:
        return list(
            session.exec(
                select(RawOrganismeModel).where(
                    RawOrganismeModel.referentiel == REFERENTIEL
                )
            )
        )


@pytest.fixture
def cleaner() -> OrganismesCleaner:
    return OrganismesCleaner()


@pytest.fixture
def repository_spy(raw_organisme_repository) -> MagicMock:
    return MagicMock(wraps=raw_organisme_repository)


@pytest.fixture
def usecase(cleaner, repository_spy) -> CleanRawOrganismesUsecase:
    return CleanRawOrganismesUsecase(
        organismes_cleaner=cleaner, raw_organisme_repository=repository_spy
    )


@pytest.mark.asyncio
async def test_single_partial_batch_stops_after_one_fetch(
    usecase, repository_spy, raw_organisme_repository, db_engine
):
    await raw_organisme_repository.upsert_batch(_raw_organismes(3))

    result = await usecase.execute(REFERENTIEL)

    assert repository_spy.find_uncleaned.call_count == 1
    assert len(result) == 3
    assert all(isinstance(organisme, Organisme) for organisme in result)
    assert all(row.cleaned_at is not None for row in _fetch_all(db_engine))


@pytest.mark.asyncio
async def test_fetches_again_when_batch_is_full(
    usecase, repository_spy, raw_organisme_repository, db_engine
):
    await raw_organisme_repository.upsert_batch(_raw_organismes(BATCH_SIZE))

    result = await usecase.execute(REFERENTIEL)

    assert repository_spy.find_uncleaned.call_count == 2
    assert len(result) == BATCH_SIZE
    assert repository_spy.mark_as_cleaned_batch.call_count == 1
    assert all(row.cleaned_at is not None for row in _fetch_all(db_engine))


@pytest.mark.asyncio
async def test_marks_all_fetched_ids_as_cleaned(
    usecase, raw_organisme_repository, db_engine
):
    raw_batch = _raw_organismes(2)
    await raw_organisme_repository.upsert_batch(raw_batch)

    await usecase.execute(REFERENTIEL)

    saved = _fetch_all(db_engine)
    assert {row.id for row in saved} == {raw.id for raw in raw_batch}
    assert all(row.cleaned_at is not None for row in saved)


@pytest.mark.asyncio
async def test_filtered_out_organismes_are_not_returned_but_marked_cleaned(
    usecase, raw_organisme_repository, db_engine
):
    await raw_organisme_repository.upsert_batch(
        _raw_organismes(2, categorie=DISALLOWED_CATEGORIE)
    )

    result = await usecase.execute(REFERENTIEL)

    assert result == []
    assert all(row.cleaned_at is not None for row in _fetch_all(db_engine))


@pytest.mark.asyncio
async def test_no_uncleaned_organismes_does_not_mark_cleaned(usecase, repository_spy):
    result = await usecase.execute(REFERENTIEL)

    assert result == []
    repository_spy.mark_as_cleaned_batch.assert_not_called()


@pytest.mark.asyncio
async def test_cleaner_error_is_skipped_but_still_marked_cleaned(
    repository_spy, raw_organisme_repository, db_engine
):
    raw_batch = _raw_organismes(2)
    await raw_organisme_repository.upsert_batch(raw_batch)
    real_cleaner = OrganismesCleaner()
    mock_cleaner = MagicMock(spec=IOrganismesCleaner)

    def _clean_side_effect(raw_organisme):
        if raw_organisme.external_id == raw_batch[0].external_id:
            raise ValueError("boom")
        return real_cleaner.clean(raw_organisme)

    mock_cleaner.clean.side_effect = _clean_side_effect
    usecase = CleanRawOrganismesUsecase(
        organismes_cleaner=mock_cleaner, raw_organisme_repository=repository_spy
    )

    result = await usecase.execute(REFERENTIEL)

    assert len(result) == 1
    assert all(row.cleaned_at is not None for row in _fetch_all(db_engine))
