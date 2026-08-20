import csv
from pathlib import Path

import pytest
from referentiel.value_objects.siret import SIRET
from referentiel.value_objects.verse import Verse

from domain.entities.raw_organisme import RawOrganisme
from infrastructure.gateways.organismes_cleaner import OrganismesCleaner

SIRET_VALUE = "26060047300342"


def _ege(
    *,
    categorie: str = "205",
    nom: str = "FOYER RESTAURANT LES ORANGERS   ",
    siret: str | None = SIRET_VALUE,
    cog_commune: str | None = "06088",
    coordonnee_x: str | None = "7.254944",
    coordonnee_y: str | None = "43.697073",
) -> dict:
    return {
        "categorieentiteGeographiqueExercice": categorie,
        "informationsGeneralesEGE": {
            "nomEgeLong": nom,
            "siret": siret,
        },
        "adresse": [
            {
                "cogCommune": cog_commune,
                "coordonneesGeographique": {
                    "coordonneeX": coordonnee_x,
                    "coordonneeY": coordonnee_y,
                },
            }
        ]
        if cog_commune is not None
        else [],
    }


def _raw_organisme(data: dict | None, referentiel: str = "FINESS") -> RawOrganisme:
    return RawOrganisme(
        referentiel=referentiel,
        millesime="2026-08-19",
        external_id="060786738",
        data=data,
    )


@pytest.fixture
def categories_csv(tmp_path: Path) -> Path:
    csv_path = tmp_path / "categories.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(["code", "libelle"])
        writer.writerow(["205", "Etablissement"])
    return csv_path


@pytest.fixture
def cleaner(categories_csv: Path) -> OrganismesCleaner:
    return OrganismesCleaner(categories_csv_path=categories_csv)


def test_cleans_valid_raw_organisme(cleaner: OrganismesCleaner):
    raw_organisme = _raw_organisme(_ege())

    organisme = cleaner.clean(raw_organisme)

    assert organisme is not None
    assert organisme.nom == "FOYER RESTAURANT LES ORANGERS"
    assert organisme.versant == Verse.FPH
    assert organisme.siret == SIRET(code=SIRET_VALUE)
    assert organisme.external_id == "060786738"
    assert organisme.referentiel == "FINESS"
    assert organisme.millesime == "2026-08-19"
    assert organisme.parent_id is None
    assert organisme.localisation is not None
    assert organisme.localisation.department.code == "06"
    assert organisme.localisation.region.code == "93"
    assert organisme.localisation.latitude == 43.697073
    assert organisme.localisation.longitude == 7.254944


@pytest.mark.parametrize(
    "referentiel,data",
    [
        pytest.param("OTHER_REF", _ege(), id="non_finess_referentiel"),
        pytest.param("FINESS", _ege(categorie="999"), id="disallowed_categorie"),
        pytest.param("FINESS", None, id="no_data"),
        pytest.param("FINESS", _ege(siret=None), id="missing_siret"),
        pytest.param("FINESS", _ege(siret="not-a-siret"), id="invalid_siret"),
        pytest.param("FINESS", _ege(nom=""), id="missing_nom"),
    ],
)
def test_finess_returns_none(
    cleaner: OrganismesCleaner, referentiel: str, data: dict | None
):
    raw_organisme = _raw_organisme(data, referentiel=referentiel)

    assert cleaner.clean(raw_organisme) is None


@pytest.mark.parametrize(
    "cog_commune",
    [None, "", "00042"],
    ids=["no_address", "empty_cog_commune", "invalid_commune_code"],
)
def test_finess_localisation_is_none(
    cleaner: OrganismesCleaner, cog_commune: str | None
):
    raw_organisme = _raw_organisme(_ege(cog_commune=cog_commune))

    organisme = cleaner.clean(raw_organisme)

    assert organisme is not None
    assert organisme.localisation is None


def test_coordinates_are_none_when_missing(cleaner: OrganismesCleaner):
    raw_organisme = _raw_organisme(_ege(coordonnee_x=None, coordonnee_y=None))

    organisme = cleaner.clean(raw_organisme)

    assert organisme is not None
    assert organisme.localisation is not None
    assert organisme.localisation.latitude is None
    assert organisme.localisation.longitude is None


def _collectivite(
    *,
    libl_col: str | None = "COMMUNAUTE DE COMMUNES BRIANCONNAIS",
    libc_col: str | None = "CC BRIANCONNAIS",
    siret_col: str | None = "24050043900080",
    cod_dep_col: str | None = "005",
) -> dict:
    return {
        "id_col": 10631,
        "libl_col": libl_col,
        "libc_col": libc_col,
        "siret_col": siret_col,
        "cod_dep_col": cod_dep_col,
    }


def _raw_organisme_gipcdg(data: dict | None) -> RawOrganisme:
    return RawOrganisme(
        referentiel="GIPCDG",
        millesime="2026-08-20",
        external_id="10631",
        data=data,
    )


def test_cleans_valid_gipcdg_raw_organisme(cleaner: OrganismesCleaner):
    raw_organisme = _raw_organisme_gipcdg(_collectivite())

    organisme = cleaner.clean(raw_organisme)

    assert organisme is not None
    assert organisme.nom == "COMMUNAUTE DE COMMUNES BRIANCONNAIS"
    assert organisme.versant == Verse.FPT
    assert organisme.siret == SIRET(code="24050043900080")
    assert organisme.external_id == "10631"
    assert organisme.referentiel == "GIPCDG"
    assert organisme.millesime == "2026-08-20"
    assert organisme.parent_id is None
    assert organisme.localisation is not None
    assert organisme.localisation.department.code == "05"
    assert organisme.localisation.region.code == "93"
    assert organisme.localisation.latitude is None
    assert organisme.localisation.longitude is None


def test_gipcdg_falls_back_to_libc_col_when_no_libl_col(cleaner: OrganismesCleaner):
    raw_organisme = _raw_organisme_gipcdg(_collectivite(libl_col=None))

    organisme = cleaner.clean(raw_organisme)

    assert organisme is not None
    assert organisme.nom == "CC BRIANCONNAIS"


@pytest.mark.parametrize(
    "data",
    [
        pytest.param(None, id="no_data"),
        pytest.param(_collectivite(siret_col=None), id="missing_siret"),
        pytest.param(_collectivite(siret_col="not-a-siret"), id="invalid_siret"),
        pytest.param(_collectivite(libl_col=None, libc_col=""), id="missing_nom"),
    ],
)
def test_gipcdg_returns_none(cleaner: OrganismesCleaner, data: dict | None):
    raw_organisme = _raw_organisme_gipcdg(data)

    assert cleaner.clean(raw_organisme) is None


@pytest.mark.parametrize(
    "cod_dep_col",
    [None, "999", "000", "02A"],
    ids=["missing", "unknown_department", "all_zeros", "not_numeric"],
)
def test_gipcdg_localisation_is_none(
    cleaner: OrganismesCleaner, cod_dep_col: str | None
):
    raw_organisme = _raw_organisme_gipcdg(_collectivite(cod_dep_col=cod_dep_col))

    organisme = cleaner.clean(raw_organisme)

    assert organisme is not None
    assert organisme.localisation is None
