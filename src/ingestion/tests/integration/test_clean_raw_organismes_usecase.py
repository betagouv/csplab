import logging
from datetime import datetime, timedelta, timezone
from pathlib import Path
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
from domain.value_objects.siret_candidate import SiretCandidate
from infrastructure.exceptions.exceptions import DilaSiretNotFound
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


ALLOWED_STATUT_JURIDIQUE = "13"  # Etablissement Public Communal d'Hospitalisation


def _ege(*, categorie: str = ALLOWED_CATEGORIE, external_id: str) -> dict:
    return {
        "etatObjet": "A",
        "categorieentiteGeographiqueExercice": categorie,
        "statutJuridique": ALLOWED_STATUT_JURIDIQUE,
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
OTHER_SIRET_VALUE = "35600000000048"
MINISTERE_SIRET_VALUE = "11000601200014"


class _FakeSiretLookupGateway:
    def __init__(
        self,
        candidates: dict[str, list[SiretCandidate]] | None = None,
        error: Exception | None = None,
    ) -> None:
        self.candidates = candidates or {}
        self.error = error
        self.calls: list[str] = []

    def search(self, query: str) -> list[SiretCandidate]:
        self.calls.append(query)
        if self.error is not None:
            raise self.error
        return self.candidates.get(query, [])


def _candidate(
    denomination: str, siret: str = DILA_SIRET_VALUE, nature_juridique: str = "7120"
) -> SiretCandidate:
    return SiretCandidate(
        siret=siret,
        siren=siret[:9],
        denomination=denomination,
        nature_juridique=nature_juridique,
    )


def _raw_organisme_dila(
    external_id: str,
    *,
    nom: str | None = None,
    siret: str | None = None,
    type_organisme: str = "Établissement public",
    ancestors: list[str] | None = None,
) -> RawOrganisme:
    return RawOrganisme(
        referentiel=DILA_REFERENTIEL,
        millesime="2026-08-26",
        external_id=external_id,
        data={
            "nom": nom or f"Ministère {external_id}",
            "siret": siret,
            "type_organisme": type_organisme,
            "code_insee_commune": None,
            "adresse": None,
            "date_creation_datetime": None,
            "ancestors": ancestors or [],
            "homonyms": 1,
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


@pytest.fixture
def dila_sirets_csv(tmp_path: Path) -> Path:
    csv_path = tmp_path / "dila_sirets.csv"
    csv_path.write_text(
        "dila_id;nom_dila;siret;denomination_sirene;nature_juridique;source;score\n"
        f"dila-mapped;Ministère mappé;{MINISTERE_SIRET_VALUE};MINISTERE;7113;"
        "annuaire_dila;\n"
        "dila-excluded;Institut exclu;;;;exclusion;\n",
        encoding="utf-8",
    )
    return csv_path


@pytest.fixture
def dila_usecase_for(raw_organisme_repository, dila_sirets_csv):
    def _build(gateway: _FakeSiretLookupGateway) -> CleanRawOrganismesUsecase:
        return CleanRawOrganismesUsecase(
            organismes_cleaner=OrganismesCleaner(
                dila_sirets_csv_path=dila_sirets_csv,
                dila_siret_lookup_max_age_days=DILA_SIRET_LOOKUP_MAX_AGE_DAYS,
            ),
            raw_organisme_repository=raw_organisme_repository,
            siret_lookup_gateway=gateway,
        )

    return _build


def _siret_not_found_records(caplog) -> list[logging.LogRecord]:
    return [
        record
        for record in caplog.records
        if record.exc_info and isinstance(record.exc_info[1], DilaSiretNotFound)
    ]


@pytest.mark.asyncio
async def test_looks_up_and_persists_missing_dila_siret(
    raw_organisme_repository, db_engine, dila_usecase_for
):
    await raw_organisme_repository.upsert_batch([_raw_organisme_dila("dila-1")])
    gateway = _FakeSiretLookupGateway(
        {"Ministère dila-1": [_candidate("MINISTERE DILA 1")]}
    )

    result = await dila_usecase_for(gateway).execute(DILA_REFERENTIEL)

    assert len(result) == 1
    assert result[0].siret.code == DILA_SIRET_VALUE
    assert gateway.calls == ["Ministère dila-1"]
    saved = _fetch_dila(db_engine, "dila-1")
    assert saved.dila_siret_found == DILA_SIRET_VALUE
    assert saved.dila_siret_found_at is not None


@pytest.mark.asyncio
async def test_does_not_retain_a_private_candidate_found_by_name(
    raw_organisme_repository, db_engine, dila_usecase_for
):
    await raw_organisme_repository.upsert_batch([_raw_organisme_dila("dila-1")])
    gateway = _FakeSiretLookupGateway(
        {"Ministère dila-1": [_candidate("MINISTERE DILA 1", nature_juridique="5710")]}
    )

    result = await dila_usecase_for(gateway).execute(DILA_REFERENTIEL)

    assert result == []
    assert _fetch_dila(db_engine, "dila-1").dila_siret_found == ""


@pytest.mark.parametrize(
    "nature_juridique,expected_siret",
    [("7389", DILA_SIRET_VALUE), ("9220", DILA_SIRET_VALUE), ("5710", "")],
    ids=["public", "associatif", "prive"],
)
@pytest.mark.asyncio
async def test_verifies_the_siret_from_the_dila_export(
    raw_organisme_repository,
    db_engine,
    dila_usecase_for,
    nature_juridique,
    expected_siret,
):
    await raw_organisme_repository.upsert_batch(
        [_raw_organisme_dila("dila-1", siret=DILA_SIRET_VALUE)]
    )
    gateway = _FakeSiretLookupGateway(
        {
            DILA_SIRET_VALUE: [
                _candidate("CONSERVATOIRE", nature_juridique=nature_juridique)
            ]
        }
    )

    result = await dila_usecase_for(gateway).execute(DILA_REFERENTIEL)

    assert gateway.calls == [DILA_SIRET_VALUE]
    assert [o.siret.code for o in result] == (
        [expected_siret] if expected_siret else []
    )
    assert _fetch_dila(db_engine, "dila-1").dila_siret_found == expected_siret


@pytest.mark.asyncio
async def test_does_not_look_up_dila_siret_again_once_cached(
    raw_organisme_repository, dila_usecase_for
):
    await raw_organisme_repository.upsert_batch([_raw_organisme_dila("dila-1")])
    gateway = _FakeSiretLookupGateway(
        {"Ministère dila-1": [_candidate("MINISTERE DILA 1")]}
    )
    usecase = dila_usecase_for(gateway)
    await usecase.execute(DILA_REFERENTIEL)

    # A re-import without any change resets cleaned_at, but must not
    # re-trigger a lookup since dila_siret_found is preserved across upserts.
    await raw_organisme_repository.upsert_batch([_raw_organisme_dila("dila-1")])
    result = await usecase.execute(DILA_REFERENTIEL)

    assert gateway.calls == ["Ministère dila-1"]
    assert [o.siret.code for o in result] == [DILA_SIRET_VALUE]


@pytest.mark.asyncio
async def test_looks_up_dila_siret_again_once_cache_is_older_than_max_age(
    raw_organisme_repository, db_engine, dila_usecase_for
):
    raw_organisme = _raw_organisme_dila("dila-1")
    await raw_organisme_repository.upsert_batch([raw_organisme])
    stale_found_at = datetime.now(tz=timezone.utc) - timedelta(days=31)
    await raw_organisme_repository.mark_dila_siret_found_batch(
        [(raw_organisme.id, OTHER_SIRET_VALUE, stale_found_at)]
    )
    gateway = _FakeSiretLookupGateway(
        {"Ministère dila-1": [_candidate("MINISTERE DILA 1")]}
    )

    result = await dila_usecase_for(gateway).execute(DILA_REFERENTIEL)

    assert len(result) == 1
    assert result[0].siret.code == DILA_SIRET_VALUE
    assert gateway.calls == ["Ministère dila-1"]
    saved = _fetch_dila(db_engine, "dila-1")
    assert saved.dila_siret_found == DILA_SIRET_VALUE
    assert saved.dila_siret_found_at.replace(tzinfo=timezone.utc) > stale_found_at


@pytest.mark.asyncio
async def test_failed_lookup_is_not_cached(
    raw_organisme_repository, db_engine, dila_usecase_for
):
    await raw_organisme_repository.upsert_batch([_raw_organisme_dila("dila-1")])
    gateway = _FakeSiretLookupGateway(error=RuntimeError("API down"))

    result = await dila_usecase_for(gateway).execute(DILA_REFERENTIEL)

    assert result == []
    assert _fetch_dila(db_engine, "dila-1").dila_siret_found is None


@pytest.mark.asyncio
async def test_mapping_takes_precedence_without_lookup(
    raw_organisme_repository, dila_usecase_for
):
    await raw_organisme_repository.upsert_batch(
        [_raw_organisme_dila("dila-mapped", siret=DILA_SIRET_VALUE)]
    )
    gateway = _FakeSiretLookupGateway()

    result = await dila_usecase_for(gateway).execute(DILA_REFERENTIEL)

    assert [o.siret.code for o in result] == [MINISTERE_SIRET_VALUE]
    assert gateway.calls == []


@pytest.mark.asyncio
async def test_attaches_to_closest_imported_ancestor(
    raw_organisme_repository, dila_usecase_for
):
    # "Ambassades et consulats de France" has no SIRET: the embassy is
    # attached to the ministry.
    await raw_organisme_repository.upsert_batch(
        [
            _raw_organisme_dila("dila-mapped"),
            _raw_organisme_dila(
                "grouping",
                nom="Ambassades et consulats de France",
                type_organisme="Administration centrale (ou Ministère)",
                ancestors=["dila-mapped"],
            ),
            _raw_organisme_dila(
                "embassy",
                nom="Ambassade de France au Japon - Tokyo",
                type_organisme="Ambassade ou mission diplomatique",
                ancestors=["grouping", "dila-mapped"],
            ),
        ]
    )
    gateway = _FakeSiretLookupGateway(
        {
            "Ambassade de France au Japon - Tokyo": [
                _candidate("AMBASSADE DE FRANCE AU JAPON", nature_juridique="7179")
            ]
        }
    )

    result = await dila_usecase_for(gateway).execute(DILA_REFERENTIEL)

    by_external_id = {o.external_id: o for o in result}
    assert set(by_external_id) == {"dila-mapped", "embassy"}
    assert by_external_id["dila-mapped"].parent_id is None
    assert (
        by_external_id["embassy"].parent_id == by_external_id["dila-mapped"].entity_id
    )


@pytest.mark.asyncio
async def test_shared_siret_goes_to_the_shallowest_service(
    raw_organisme_repository, dila_usecase_for
):
    await raw_organisme_repository.upsert_batch(
        [
            _raw_organisme_dila("0-direction", ancestors=["dila-mapped"]),
            _raw_organisme_dila("dila-mapped"),
        ]
    )
    gateway = _FakeSiretLookupGateway(
        {
            "Ministère 0-direction": [
                _candidate("MINISTERE 0 DIRECTION", siret=MINISTERE_SIRET_VALUE)
            ]
        }
    )

    result = await dila_usecase_for(gateway).execute(DILA_REFERENTIEL)

    assert [o.external_id for o in result] == ["dila-mapped"]


@pytest.mark.parametrize(
    "candidates,reason",
    [
        ([], "no_result"),
        ([_candidate("AMICALE DU MINISTERE", nature_juridique="9220")], None),
    ],
    ids=["no_result", "no_candidate_retained"],
)
@pytest.mark.asyncio
async def test_logs_dila_siret_not_found_for_a_potential_employer(
    raw_organisme_repository, dila_usecase_for, caplog, candidates, reason
):
    await raw_organisme_repository.upsert_batch(
        [_raw_organisme_dila("dila-1", nom="Agence nationale X")]
    )
    gateway = _FakeSiretLookupGateway({"Agence nationale X": candidates})

    with caplog.at_level(logging.INFO):
        await dila_usecase_for(gateway).execute(DILA_REFERENTIEL)

    [record] = _siret_not_found_records(caplog)
    assert record.levelno == logging.ERROR
    error = record.exc_info[1]
    assert error.external_id == "dila-1"
    assert error.nom == "Agence nationale X"
    assert error.reason == (reason or "no_candidate_retained")


@pytest.mark.asyncio
async def test_does_not_log_dila_siret_not_found_for_a_sub_unit(
    raw_organisme_repository, dila_usecase_for, caplog
):
    await raw_organisme_repository.upsert_batch(
        [_raw_organisme_dila("dila-1", nom="Service juridique et économique")]
    )
    gateway = _FakeSiretLookupGateway()

    with caplog.at_level(logging.INFO):
        await dila_usecase_for(gateway).execute(DILA_REFERENTIEL)

    assert gateway.calls == ["Service juridique et économique"]
    assert _siret_not_found_records(caplog) == []
    assert all(record.levelno < logging.ERROR for record in caplog.records)


@pytest.mark.asyncio
async def test_does_not_look_up_an_office_by_name(
    raw_organisme_repository, dila_usecase_for, caplog
):
    await raw_organisme_repository.upsert_batch(
        [_raw_organisme_dila("dila-1", nom="Bureau des marchés")]
    )
    gateway = _FakeSiretLookupGateway()

    with caplog.at_level(logging.INFO):
        organismes = await dila_usecase_for(gateway).execute(DILA_REFERENTIEL)

    assert gateway.calls == []
    assert organismes == []
    assert _siret_not_found_records(caplog) == []


@pytest.mark.asyncio
async def test_does_not_log_dila_siret_not_found_on_cache_read_or_exclusion(
    raw_organisme_repository, dila_usecase_for, caplog
):
    cached = _raw_organisme_dila("dila-1", nom="Agence nationale X")
    await raw_organisme_repository.upsert_batch(
        [cached, _raw_organisme_dila("dila-excluded", nom="Institut exclu")]
    )
    await raw_organisme_repository.mark_dila_siret_found_batch(
        [(cached.id, "", datetime.now(tz=timezone.utc))]
    )
    gateway = _FakeSiretLookupGateway()

    with caplog.at_level(logging.INFO):
        result = await dila_usecase_for(gateway).execute(DILA_REFERENTIEL)

    assert result == []
    assert gateway.calls == []
    assert _siret_not_found_records(caplog) == []
