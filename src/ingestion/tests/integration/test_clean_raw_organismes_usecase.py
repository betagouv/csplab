from datetime import datetime, timedelta, timezone
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
ALLOWED_CATEGORIE = "101"
DILA_SIRET_LOOKUP_MAX_AGE_DAYS = 30
DISALLOWED_CATEGORIE = "999"


def _siret_for(external_id: str) -> str:
    # SIRETs starting with the La Poste SIREN skip the Luhn checksum,
    # so distinct valid SIRETs can be derived from any external_id.
    return f"356000000{int(external_id):05d}"


def _ege(*, categorie: str = ALLOWED_CATEGORIE, external_id: str) -> dict:
    return {
        "etatObjet": "A",
        "categorieentiteGeographiqueExercice": categorie,
        "informationsGeneralesEGE": {
            "nomEgeLong": f"ORGANISME {external_id}",
            "siret": _siret_for(external_id),
            "egeId": external_id,
        },
        "roleEge": [{"idEgePorteuse": external_id}],
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
    return OrganismesCleaner(
        dila_siret_lookup_max_age_days=DILA_SIRET_LOOKUP_MAX_AGE_DAYS
    )


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
    real_cleaner = OrganismesCleaner(
        dila_siret_lookup_max_age_days=DILA_SIRET_LOOKUP_MAX_AGE_DAYS
    )
    mock_cleaner = MagicMock(spec=IOrganismesCleaner)

    def _clean_side_effect(raw_organisme):
        if raw_organisme.external_id == raw_batch[0].external_id:
            raise ValueError("boom")
        return real_cleaner.clean(raw_organisme)

    mock_cleaner.clean.side_effect = _clean_side_effect
    mock_cleaner.dedupe_by_siret.side_effect = real_cleaner.dedupe_by_siret
    usecase = CleanRawOrganismesUsecase(
        organismes_cleaner=mock_cleaner, raw_organisme_repository=repository_spy
    )

    result = await usecase.execute(REFERENTIEL)

    assert len(result) == 1
    assert all(row.cleaned_at is not None for row in _fetch_all(db_engine))


DILA_REFERENTIEL = "DILA"
DILA_SIRET_VALUE = "26060047300342"


class _FakeSiretLookupGateway:
    def __init__(self, siret: str | None) -> None:
        self.siret = siret
        self.calls: list[str] = []

    def find_siret(self, nom: str) -> str | None:
        self.calls.append(nom)
        return self.siret


def _raw_organisme_dila(external_id: str, *, siret: str | None = None) -> RawOrganisme:
    return RawOrganisme(
        referentiel=DILA_REFERENTIEL,
        millesime="2026-08-26",
        external_id=external_id,
        data={
            "nom": f"Ministère {external_id}",
            "siret": siret,
            "code_insee_commune": None,
            "adresse": None,
            "date_creation_datetime": None,
            "parent_id": None,
        },
    )


def _fetch_dila(db_engine, external_id: str) -> RawOrganismeModel:
    with Session(db_engine) as session:
        row = session.exec(
            select(RawOrganismeModel).where(
                RawOrganismeModel.referentiel == DILA_REFERENTIEL,
                RawOrganismeModel.external_id == external_id,
            )
        ).first()
        assert row is not None
        return row


@pytest.mark.asyncio
async def test_looks_up_and_persists_missing_dila_siret(
    raw_organisme_repository, db_engine
):
    await raw_organisme_repository.upsert_batch([_raw_organisme_dila("dila-1")])
    gateway = _FakeSiretLookupGateway(siret=DILA_SIRET_VALUE)
    usecase = CleanRawOrganismesUsecase(
        organismes_cleaner=OrganismesCleaner(
            dila_siret_lookup_max_age_days=DILA_SIRET_LOOKUP_MAX_AGE_DAYS
        ),
        raw_organisme_repository=raw_organisme_repository,
        siret_lookup_gateway=gateway,
    )

    result = await usecase.execute(DILA_REFERENTIEL)

    assert len(result) == 1
    assert result[0].siret.code == DILA_SIRET_VALUE
    assert gateway.calls == ["Ministère dila-1"]
    saved = _fetch_dila(db_engine, "dila-1")
    assert saved.dila_siret_found == DILA_SIRET_VALUE
    assert saved.dila_siret_found_at is not None


@pytest.mark.asyncio
async def test_does_not_look_up_dila_siret_again_once_cached(
    raw_organisme_repository, db_engine
):
    await raw_organisme_repository.upsert_batch([_raw_organisme_dila("dila-1")])
    gateway = _FakeSiretLookupGateway(siret=DILA_SIRET_VALUE)
    usecase = CleanRawOrganismesUsecase(
        organismes_cleaner=OrganismesCleaner(
            dila_siret_lookup_max_age_days=DILA_SIRET_LOOKUP_MAX_AGE_DAYS
        ),
        raw_organisme_repository=raw_organisme_repository,
        siret_lookup_gateway=gateway,
    )
    await usecase.execute(DILA_REFERENTIEL)

    # A re-import without any change resets cleaned_at, but must not
    # re-trigger a lookup since dila_siret_found is preserved across upserts.
    await raw_organisme_repository.upsert_batch([_raw_organisme_dila("dila-1")])
    await usecase.execute(DILA_REFERENTIEL)

    assert gateway.calls == ["Ministère dila-1"]


@pytest.mark.asyncio
async def test_looks_up_dila_siret_again_once_cache_is_older_than_max_age(
    raw_organisme_repository, db_engine
):
    raw_organisme = _raw_organisme_dila("dila-1")
    await raw_organisme_repository.upsert_batch([raw_organisme])
    stale_found_at = datetime.now(tz=timezone.utc) - timedelta(days=31)
    await raw_organisme_repository.mark_dila_siret_found_batch(
        [(raw_organisme.id, "35600000000048", stale_found_at)]
    )
    gateway = _FakeSiretLookupGateway(siret=DILA_SIRET_VALUE)
    usecase = CleanRawOrganismesUsecase(
        organismes_cleaner=OrganismesCleaner(
            dila_siret_lookup_max_age_days=DILA_SIRET_LOOKUP_MAX_AGE_DAYS
        ),
        raw_organisme_repository=raw_organisme_repository,
        siret_lookup_gateway=gateway,
    )

    result = await usecase.execute(DILA_REFERENTIEL)

    assert len(result) == 1
    assert result[0].siret.code == DILA_SIRET_VALUE
    assert gateway.calls == ["Ministère dila-1"]
    saved = _fetch_dila(db_engine, "dila-1")
    assert saved.dila_siret_found == DILA_SIRET_VALUE
    assert saved.dila_siret_found_at.replace(tzinfo=timezone.utc) > stale_found_at


@pytest.mark.asyncio
async def test_does_not_look_up_dila_siret_when_present_in_data(
    raw_organisme_repository,
):
    await raw_organisme_repository.upsert_batch(
        [_raw_organisme_dila("dila-1", siret=DILA_SIRET_VALUE)]
    )
    gateway = _FakeSiretLookupGateway(siret="35600000000048")
    usecase = CleanRawOrganismesUsecase(
        organismes_cleaner=OrganismesCleaner(
            dila_siret_lookup_max_age_days=DILA_SIRET_LOOKUP_MAX_AGE_DAYS
        ),
        raw_organisme_repository=raw_organisme_repository,
        siret_lookup_gateway=gateway,
    )

    result = await usecase.execute(DILA_REFERENTIEL)

    assert len(result) == 1
    assert result[0].siret.code == DILA_SIRET_VALUE
    assert gateway.calls == []
