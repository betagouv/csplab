import csv
from datetime import date
from pathlib import Path

import pytest
from pydantic import ValidationError
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
    etat_objet: str = "A",
    ege_id: str = "50477",
    role_ege_porteuse: str | None = "50477",
) -> dict:
    return {
        "etatObjet": etat_objet,
        "categorieentiteGeographiqueExercice": categorie,
        "informationsGeneralesEGE": {
            "nomEgeLong": nom,
            "siret": siret,
            "egeId": ege_id,
        },
        "roleEge": [{"idEgePorteuse": role_ege_porteuse}],
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


def _raw_organisme(data: dict, external_id: str = "060786738") -> RawOrganisme:
    return RawOrganisme(
        referentiel="FINESS",
        millesime="2026-08-19",
        external_id=external_id,
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


def test_filters_out_non_active_etat_objet(cleaner: OrganismesCleaner):
    raw_organisme = _raw_organisme(_ege(etat_objet="I"))

    assert cleaner.clean(raw_organisme) is None


def test_filters_out_when_not_porteuse(cleaner: OrganismesCleaner):
    raw_organisme = _raw_organisme(_ege(ege_id="50477", role_ege_porteuse="99999"))

    assert cleaner.clean(raw_organisme) is None


def test_returns_none_when_no_data(cleaner: OrganismesCleaner):
    raw_organisme = RawOrganisme(
        referentiel="FINESS", millesime="2026-08-19", external_id="1", data=None
    )

    assert cleaner.clean(raw_organisme) is None


@pytest.mark.parametrize(
    "data",
    [
        pytest.param(_ege(siret=None), id="missing_siret"),
        pytest.param(_ege(siret="not-a-siret"), id="invalid_siret"),
        pytest.param(_ege(nom=""), id="missing_nom"),
    ],
)
def test_finess_raises_on_invalid_data(cleaner: OrganismesCleaner, data: dict):
    raw_organisme = _raw_organisme(data)

    with pytest.raises(ValidationError):
        cleaner.clean(raw_organisme)


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


def test_dedupe_by_siret_keeps_smallest_external_id(cleaner: OrganismesCleaner):
    smaller = cleaner.clean(
        _raw_organisme(_ege(ege_id="1", role_ege_porteuse="1"), external_id="123456789")
    )
    bigger = cleaner.clean(
        _raw_organisme(_ege(ege_id="2", role_ege_porteuse="2"), external_id="987654321")
    )
    assert smaller is not None
    assert bigger is not None

    result = cleaner.dedupe_by_siret([bigger, smaller])

    assert result == [smaller]


def test_dedupe_by_siret_keeps_distinct_sirets(cleaner: OrganismesCleaner):
    other_siret = "35600000000048"
    first = cleaner.clean(
        _raw_organisme(_ege(ege_id="1", role_ege_porteuse="1"), external_id="123456789")
    )
    second = cleaner.clean(
        _raw_organisme(
            _ege(ege_id="2", role_ege_porteuse="2", siret=other_siret),
            external_id="987654321",
        )
    )
    assert first is not None
    assert second is not None

    result = cleaner.dedupe_by_siret([first, second])

    assert {o.external_id for o in result} == {"123456789", "987654321"}


def _collectivite(
    *,
    libl_col: str | None = "COMMUNAUTE DE COMMUNES BRIANCONNAIS",
    libc_col: str | None = "CC BRIANCONNAIS",
    siret_col: str | None = "24050043900080",
    cod_dep_col: str | None = "005",
    date_insert_col: str | None = "10/06/2014",
) -> dict:
    return {
        "id_col": 10631,
        "libl_col": libl_col,
        "libc_col": libc_col,
        "siret_col": siret_col,
        "cod_dep_col": cod_dep_col,
        "date_insert_col": date_insert_col,
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
    assert organisme.date_creation == date(2014, 6, 10)


@pytest.mark.parametrize(
    "date_insert_col",
    [None, "", "2014-06-10", "31/06/2014"],
    ids=["missing", "empty", "iso_format", "invalid_date"],
)
def test_gipcdg_date_creation_is_none_when_unparseable(
    cleaner: OrganismesCleaner, date_insert_col: str | None
):
    raw_organisme = _raw_organisme_gipcdg(
        _collectivite(date_insert_col=date_insert_col)
    )

    organisme = cleaner.clean(raw_organisme)

    assert organisme is not None
    assert organisme.date_creation is None


def test_gipcdg_falls_back_to_libc_col_when_no_libl_col(cleaner: OrganismesCleaner):
    raw_organisme = _raw_organisme_gipcdg(_collectivite(libl_col=None))

    organisme = cleaner.clean(raw_organisme)

    assert organisme is not None
    assert organisme.nom == "CC BRIANCONNAIS"


def test_gipcdg_returns_none_when_no_data(cleaner: OrganismesCleaner):
    raw_organisme = _raw_organisme_gipcdg(None)

    assert cleaner.clean(raw_organisme) is None


@pytest.mark.parametrize(
    "data",
    [
        pytest.param(_collectivite(siret_col=None), id="missing_siret"),
        pytest.param(_collectivite(siret_col="not-a-siret"), id="invalid_siret"),
        pytest.param(_collectivite(libl_col=None, libc_col=""), id="missing_nom"),
    ],
)
def test_gipcdg_raises_on_invalid_data(cleaner: OrganismesCleaner, data: dict | None):
    raw_organisme = _raw_organisme_gipcdg(data)

    with pytest.raises(ValidationError):
        cleaner.clean(raw_organisme)


@pytest.mark.parametrize(
    "cod_dep_col",
    [None, "999", "000", "ZZZ"],
    ids=["missing", "unknown_department", "all_zeros", "invalid_code"],
)
def test_gipcdg_localisation_is_none(
    cleaner: OrganismesCleaner, cod_dep_col: str | None
):
    raw_organisme = _raw_organisme_gipcdg(_collectivite(cod_dep_col=cod_dep_col))

    organisme = cleaner.clean(raw_organisme)

    assert organisme is not None
    assert organisme.localisation is None
