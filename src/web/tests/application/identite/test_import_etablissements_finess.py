from datetime import date
from unittest.mock import MagicMock

from referentiel.value_objects.verse import Verse

from application.identite.usecases.import_etablissements_finess import (
    BATCH_SIZE,
    REFERENTIEL_FINESS,
    ImportEtablissementsFinessUsecase,
)
from domain.identite.gateways.finess_gateway_interface import (
    FinessEtablissement,
    FinessResource,
)
from infrastructure.gateways.shared.logger import LoggerService

LATITUDE = 46.211257
LONGITUDE = 5.254203


def _make_usecase(etablissements, upsert_batch_result=None):
    finess_gateway = MagicMock()
    finess_gateway.find_latest_journalier.return_value = FinessResource(
        url="https://static.data.gouv.fr/finess.json.gz",
        millesime=date(2026, 8, 18),
    )
    finess_gateway.stream_etablissements.return_value = iter(etablissements)

    organisme_repository = MagicMock()
    organisme_repository.upsert_batch.return_value = upsert_batch_result or {
        "created": len(etablissements),
        "updated": 0,
        "errors": [],
    }

    usecase = ImportEtablissementsFinessUsecase(
        finess_gateway=finess_gateway,
        organisme_repository=organisme_repository,
        logger=LoggerService(),
    )
    return usecase, finess_gateway, organisme_repository


def test_import_builds_organismes_from_finess_data():
    etablissement = FinessEtablissement(
        nom="Clinique du Docteur Convert",
        external_id="010780195",
        siret="77220148900022",
        latitude=LATITUDE,
        longitude=LONGITUDE,
        departement="01",
    )
    usecase, finess_gateway, organisme_repository = _make_usecase([etablissement])

    result = usecase.execute()

    assert result == {"created": 1, "updated": 0, "errors": []}
    finess_gateway.stream_etablissements.assert_called_once_with(
        "https://static.data.gouv.fr/finess.json.gz"
    )
    (batch,), _ = organisme_repository.upsert_batch.call_args
    assert len(batch) == 1
    organisme = batch[0]
    assert organisme.nom == "Clinique du Docteur Convert"
    assert organisme.versant == Verse.FPH
    assert organisme.siret.value == "77220148900022"
    assert organisme.external_id == "010780195"
    assert organisme.referentiel == REFERENTIEL_FINESS
    assert organisme.millesime == "2026-08-18"
    assert organisme.gestion_ats is True
    assert organisme.localisation is not None
    assert organisme.localisation.latitude == LATITUDE
    assert organisme.localisation.longitude == LONGITUDE
    assert organisme.localisation.department.code == "01"
    assert organisme.localisation.region.code == "84"


def test_import_skips_etablissement_with_invalid_siret_and_reports_error():
    invalid_etablissement = FinessEtablissement(
        nom="Etablissement invalide",
        external_id="010780195",
        siret="1234567890123",  # 13 digits: fails SIRET validation
        latitude=None,
        longitude=None,
        departement=None,
    )
    usecase, _, organisme_repository = _make_usecase(
        [invalid_etablissement],
        upsert_batch_result={
            "created": 0,
            "updated": 0,
            "errors": [],
        },
    )

    result = usecase.execute()

    assert result["created"] == 0
    assert len(result["errors"]) == 1
    assert result["errors"][0]["entity_id"] == "010780195"
    organisme_repository.upsert_batch.assert_not_called()


def test_import_without_departement_has_no_localisation():
    etablissement = FinessEtablissement(
        nom="Etablissement sans commune",
        external_id="010787190",
        siret="77220148900022",
        latitude=None,
        longitude=None,
        departement=None,
    )
    usecase, _, organisme_repository = _make_usecase([etablissement])

    usecase.execute()

    (batch,), _ = organisme_repository.upsert_batch.call_args
    assert batch[0].localisation is None


def test_import_with_invalid_departement_code_has_no_localisation():
    etablissement = FinessEtablissement(
        nom="Etablissement departement invalide",
        external_id="010787190",
        siret="77220148900022",
        latitude=None,
        longitude=None,
        departement="99",  # not a valid INSEE department code
    )
    usecase, _, organisme_repository = _make_usecase([etablissement])

    usecase.execute()

    (batch,), _ = organisme_repository.upsert_batch.call_args
    assert batch[0].localisation is None


def test_import_with_unmapped_departement_has_no_localisation():
    etablissement = FinessEtablissement(
        nom="Etablissement Saint-Pierre-et-Miquelon",
        external_id="010787190",
        siret="77220148900022",
        latitude=None,
        longitude=None,
        departement="975",  # valid department, not covered by the region table
    )
    usecase, _, organisme_repository = _make_usecase([etablissement])

    usecase.execute()

    (batch,), _ = organisme_repository.upsert_batch.call_args
    assert batch[0].localisation is None


def test_import_flushes_in_batches():
    etablissements_count = BATCH_SIZE + 1
    etablissements = [
        FinessEtablissement(
            nom=f"Etablissement {i}",
            external_id=f"01078{i:04d}",
            siret="77220148900022",
            latitude=None,
            longitude=None,
            departement=None,
        )
        for i in range(etablissements_count)
    ]
    usecase, _, organisme_repository = _make_usecase(etablissements)
    organisme_repository.upsert_batch.side_effect = lambda batch: {
        "created": len(batch),
        "updated": 0,
        "errors": [],
    }

    result = usecase.execute()

    expected_batch_count = 2
    assert organisme_repository.upsert_batch.call_count == expected_batch_count
    first_call_batch, second_call_batch = (
        call.args[0] for call in organisme_repository.upsert_batch.call_args_list
    )
    assert len(first_call_batch) == BATCH_SIZE
    assert len(second_call_batch) == 1
    assert result["created"] == etablissements_count
