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


def _raw_organisme(data: dict) -> RawOrganisme:
    return RawOrganisme(
        referentiel="FINESS",
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


def test_filters_out_non_finess_referentiel(cleaner: OrganismesCleaner):
    raw_organisme = RawOrganisme(
        referentiel="OTHER_REF",
        millesime="2026-08-19",
        external_id="1",
        data=_ege(),
    )

    assert cleaner.clean(raw_organisme) is None


def test_filters_out_disallowed_categorie(cleaner: OrganismesCleaner):
    raw_organisme = _raw_organisme(_ege(categorie="999"))

    assert cleaner.clean(raw_organisme) is None


def test_returns_none_when_no_data(cleaner: OrganismesCleaner):
    raw_organisme = RawOrganisme(
        referentiel="FINESS", millesime="2026-08-19", external_id="1", data=None
    )

    assert cleaner.clean(raw_organisme) is None


def test_returns_none_when_missing_siret(cleaner: OrganismesCleaner):
    raw_organisme = _raw_organisme(_ege(siret=None))

    assert cleaner.clean(raw_organisme) is None


def test_returns_none_when_invalid_siret(cleaner: OrganismesCleaner):
    raw_organisme = _raw_organisme(_ege(siret="not-a-siret"))

    assert cleaner.clean(raw_organisme) is None


def test_returns_none_when_missing_nom(cleaner: OrganismesCleaner):
    raw_organisme = _raw_organisme(_ege(nom=""))

    assert cleaner.clean(raw_organisme) is None


def test_localisation_is_none_when_no_address(cleaner: OrganismesCleaner):
    raw_organisme = _raw_organisme(_ege(cog_commune=None))

    organisme = cleaner.clean(raw_organisme)

    assert organisme is not None
    assert organisme.localisation is None


def test_localisation_is_none_when_address_has_no_cog_commune(
    cleaner: OrganismesCleaner,
):
    raw_organisme = _raw_organisme(_ege(cog_commune=""))

    organisme = cleaner.clean(raw_organisme)

    assert organisme is not None
    assert organisme.localisation is None


def test_localisation_is_none_when_invalid_commune_code(cleaner: OrganismesCleaner):
    raw_organisme = _raw_organisme(_ege(cog_commune="00042"))

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


def test_coordinates_are_converted_from_lambert93(cleaner: OrganismesCleaner):
    # Lambert-93 projection of Nice (43.697073, 7.254944), the WGS84 point
    # used by the other tests in this file.
    raw_organisme = _raw_organisme(
        _ege(coordonnee_x="1042920.75", coordonnee_y="6297912.66")
    )

    organisme = cleaner.clean(raw_organisme)

    assert organisme is not None
    assert organisme.localisation is not None
    assert organisme.localisation.latitude == pytest.approx(43.697073, abs=1e-4)
    assert organisme.localisation.longitude == pytest.approx(7.254944, abs=1e-4)
