import csv
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest
from pydantic import ValidationError
from referentiel.value_objects.siret import SIRET
from referentiel.value_objects.verse import Verse

from domain.entities.raw_organisme import RawOrganisme
from infrastructure.gateways.organismes_cleaner import OrganismesCleaner

SIRET_VALUE = "26060047300342"
DILA_SIRET_LOOKUP_MAX_AGE_DAYS = 30


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
    role_ege: list[dict] | None = None,
    statut_juridique: str | None = "13",
) -> dict:
    return {
        "etatObjet": etat_objet,
        "categorieentiteGeographiqueExercice": categorie,
        "statutJuridique": statut_juridique,
        "informationsGeneralesEGE": {
            "nomEgeLong": nom,
            "siret": siret,
            "egeId": ege_id,
        },
        "roleEge": role_ege if role_ege is not None else [],
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
def statuts_juridiques_publics_csv(tmp_path: Path) -> Path:
    csv_path = tmp_path / "statuts_juridiques_publics.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(["code", "libelle"])
        writer.writerow(["13", "Etablissement Public Communal d'Hospitalisation"])
    return csv_path


@pytest.fixture
def cleaner(
    categories_csv: Path, statuts_juridiques_publics_csv: Path
) -> OrganismesCleaner:
    return OrganismesCleaner(
        categories_csv_path=categories_csv,
        statuts_juridiques_publics_csv_path=statuts_juridiques_publics_csv,
        dila_siret_lookup_max_age_days=DILA_SIRET_LOOKUP_MAX_AGE_DAYS,
    )


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


def test_filters_out_private_statut_juridique(cleaner: OrganismesCleaner):
    raw_organisme = _raw_organisme(
        _ege(statut_juridique="60")  # Association Loi 1901 non R.U.P.
    )

    assert cleaner.clean(raw_organisme) is None


def test_filters_out_missing_statut_juridique(cleaner: OrganismesCleaner):
    raw_organisme = _raw_organisme(_ege(statut_juridique=None))

    assert cleaner.clean(raw_organisme) is None


def test_keeps_public_statut_juridique(cleaner: OrganismesCleaner):
    raw_organisme = _raw_organisme(_ege(statut_juridique="13"))

    organisme = cleaner.clean(raw_organisme)

    assert organisme is not None


@pytest.fixture
def default_statuts_cleaner(categories_csv: Path) -> OrganismesCleaner:
    return OrganismesCleaner(
        categories_csv_path=categories_csv,
        dila_siret_lookup_max_age_days=DILA_SIRET_LOOKUP_MAX_AGE_DAYS,
    )


@pytest.mark.parametrize(
    "statut_juridique",
    [
        "11",  # Etablissement Public Départemental d'Hospitalisation
        "13",  # Etablissement Public Communal d'Hospitalisation
        "16",  # Syndicat Inter Hospitalier
        "19",  # Etablissement Social et Médico-Social Départemental
        "21",  # Etablissement Social et Médico-Social Communal
    ],
)
def test_default_statuts_keep_fph_employeurs(
    default_statuts_cleaner: OrganismesCleaner, statut_juridique: str
):
    raw_organisme = _raw_organisme(_ege(statut_juridique=statut_juridique))

    assert default_statuts_cleaner.clean(raw_organisme) is not None


@pytest.mark.parametrize(
    "statut_juridique",
    [
        "02",  # Département
        "03",  # Commune
        "08",  # Centre Intercommunal d'Action Sociale
        "17",  # Centre Communal d'Action Sociale
        "26",  # Autre Etablissement Public à Caractère Administratif
        "28",  # Groupement d'Intérêt Public (G.I.P.)
        "29",  # Groupement de Coopération Sanitaire public
    ],
)
def test_default_statuts_filter_out_non_fph_publics(
    default_statuts_cleaner: OrganismesCleaner, statut_juridique: str
):
    raw_organisme = _raw_organisme(_ege(statut_juridique=statut_juridique))

    assert default_statuts_cleaner.clean(raw_organisme) is None


def test_filters_out_non_active_etat_objet(cleaner: OrganismesCleaner):
    raw_organisme = _raw_organisme(_ege(etat_objet="I"))

    assert cleaner.clean(raw_organisme) is None


def test_filters_out_when_attached_to_another_porteuse(cleaner: OrganismesCleaner):
    raw_organisme = _raw_organisme(
        _ege(
            ege_id="50477",
            role_ege=[{"idEgePorteuse": "99999", "idEgeNonPorteuse": "50477"}],
        )
    )

    assert cleaner.clean(raw_organisme) is None


def test_cleans_porteuse_with_rattachements(cleaner: OrganismesCleaner):
    raw_organisme = _raw_organisme(
        _ege(
            ege_id="50477",
            role_ege=[{"idEgePorteuse": "50477", "idEgeNonPorteuse": "50478"}],
        )
    )

    organisme = cleaner.clean(raw_organisme)

    assert organisme is not None


def test_cleans_standalone_organisme_without_role_ege(cleaner: OrganismesCleaner):
    raw_organisme = _raw_organisme(_ege(ege_id="50477", role_ege=[]))

    organisme = cleaner.clean(raw_organisme)

    assert organisme is not None


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
    smaller = cleaner.clean(_raw_organisme(_ege(ege_id="1"), external_id="123456789"))
    bigger = cleaner.clean(_raw_organisme(_ege(ege_id="2"), external_id="987654321"))
    assert smaller is not None
    assert bigger is not None

    result = cleaner.dedupe_by_siret([bigger, smaller])

    assert result == [smaller]


def test_dedupe_by_siret_keeps_distinct_sirets(cleaner: OrganismesCleaner):
    other_siret = "35600000000048"
    first = cleaner.clean(_raw_organisme(_ege(ege_id="1"), external_id="123456789"))
    second = cleaner.clean(
        _raw_organisme(
            _ege(ege_id="2", siret=other_siret),
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
    is_attached: bool = False,
) -> dict:
    return {
        "id_col": 10631,
        "libl_col": libl_col,
        "libc_col": libc_col,
        "siret_col": siret_col,
        "cod_dep_col": cod_dep_col,
        "date_insert_col": date_insert_col,
        "is_attached": is_attached,
    }


def _raw_organisme_gipcdg(
    data: dict | None, external_id: str = "10631"
) -> RawOrganisme:
    return RawOrganisme(
        referentiel="GIPCDG",
        millesime="2026-08-20",
        external_id=external_id,
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
    assert organisme.date_creation == datetime(2014, 6, 10, tzinfo=timezone.utc)


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


def test_gipcdg_returns_none_when_attached_to_another_collectivite(
    cleaner: OrganismesCleaner,
):
    raw_organisme = _raw_organisme_gipcdg(_collectivite(is_attached=True))

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


def test_dedupe_by_siret_keeps_most_recently_created(cleaner: OrganismesCleaner):
    older = cleaner.clean(
        _raw_organisme_gipcdg(
            _collectivite(date_insert_col="25/10/2010"), external_id="26529"
        )
    )
    newer = cleaner.clean(
        _raw_organisme_gipcdg(
            _collectivite(date_insert_col="12/11/2021"), external_id="99819"
        )
    )
    assert older is not None
    assert newer is not None

    result = cleaner.dedupe_by_siret([older, newer])

    assert result == [newer]


def test_dedupe_by_siret_falls_back_to_smallest_external_id_when_same_date(
    cleaner: OrganismesCleaner,
):
    smaller = cleaner.clean(
        _raw_organisme_gipcdg(
            _collectivite(date_insert_col="12/11/2021"), external_id="99819"
        )
    )
    bigger = cleaner.clean(
        _raw_organisme_gipcdg(
            _collectivite(date_insert_col="12/11/2021"), external_id="99945"
        )
    )
    assert smaller is not None
    assert bigger is not None

    result = cleaner.dedupe_by_siret([bigger, smaller])

    assert result == [smaller]


DILA_SIRET_VALUE = "26060047300342"
MAPPED_SIRET_VALUE = "11000007200014"
_SENAT_DILA_ID = "59003280-8fff-4bc0-b5df-a27299c4d588"


@pytest.fixture
def dila_sirets_csv(tmp_path: Path) -> Path:
    csv_path = tmp_path / "dila_sirets.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(
            [
                "dila_id",
                "nom_dila",
                "siret",
                "denomination_sirene",
                "nature_juridique",
                "source",
                "score",
            ]
        )
        writer.writerow(
            [
                "dila-mapped",
                "Ministère du Travail",
                MAPPED_SIRET_VALUE,
                "MINISTERE DU TRAVAIL",
                "7113",
                "annuaire_dila",
                "",
            ]
        )
        writer.writerow(
            ["dila-excluded", "Bureau", "", "", "", "exclusion", ""],
        )
    return csv_path


@pytest.fixture
def dila_cleaner(categories_csv: Path, dila_sirets_csv: Path) -> OrganismesCleaner:
    return OrganismesCleaner(
        categories_csv_path=categories_csv,
        dila_sirets_csv_path=dila_sirets_csv,
        dila_siret_lookup_max_age_days=DILA_SIRET_LOOKUP_MAX_AGE_DAYS,
    )


def _dila_service(
    *,
    nom: str | None = "Ministère de l'Intérieur",
    siret: str | None = None,
    code_insee_commune: str | None = "75101",
    adresse: str | None = '[{"longitude": "2.309103", "latitude": "48.852116"}]',
    date_creation_datetime: str | None = "2008-06-30T00:00:00+00:00",
    ancestors: list[str] | None = None,
    homonyms: int = 1,
) -> dict:
    return {
        "nom": nom,
        "siret": siret,
        "type_organisme": "Administration centrale (ou Ministère)",
        "code_insee_commune": code_insee_commune,
        "adresse": adresse,
        "date_creation_datetime": date_creation_datetime,
        "ancestors": ancestors or [],
        "homonyms": homonyms,
    }


def _raw_organisme_dila(
    data: dict | None,
    external_id: str = "dila-1",
    *,
    siret_found: str | None = DILA_SIRET_VALUE,
) -> RawOrganisme:
    return RawOrganisme(
        referentiel="DILA",
        millesime="2026-08-26",
        external_id=external_id,
        data=data,
        dila_siret_found=siret_found,
    )


def test_cleans_valid_dila_raw_organisme(dila_cleaner: OrganismesCleaner):
    raw_organisme = _raw_organisme_dila(_dila_service())

    organisme = dila_cleaner.clean(raw_organisme)

    assert organisme is not None
    assert organisme.nom == "Ministère de l'Intérieur"
    assert organisme.versant == Verse.FPE
    assert organisme.siret == SIRET(code=DILA_SIRET_VALUE)
    assert organisme.external_id == "dila-1"
    assert organisme.referentiel == "DILA"
    assert organisme.millesime == "2026-08-26"
    assert organisme.parent_id is None
    assert organisme.localisation is not None
    assert organisme.localisation.department.code == "75"
    assert organisme.localisation.region.code == "11"
    assert organisme.localisation.latitude == 48.852116
    assert organisme.localisation.longitude == 2.309103
    assert organisme.date_creation == datetime(2008, 6, 30, tzinfo=timezone.utc)


def test_dila_returns_none_when_no_data(dila_cleaner: OrganismesCleaner):
    raw_organisme = _raw_organisme_dila(None)

    assert dila_cleaner.clean(raw_organisme) is None


@pytest.mark.parametrize(
    "raw_organisme",
    [
        pytest.param(
            _raw_organisme_dila(_dila_service(), siret_found="not-a-siret"),
            id="invalid_siret",
        ),
        pytest.param(_raw_organisme_dila(_dila_service(nom="")), id="missing_nom"),
    ],
)
def test_dila_raises_on_invalid_data(
    dila_cleaner: OrganismesCleaner, raw_organisme: RawOrganisme
):
    with pytest.raises(ValidationError):
        dila_cleaner.clean(raw_organisme)


@pytest.mark.parametrize(
    "siret_found", [None, ""], ids=["no_lookup", "lookup_found_nothing"]
)
def test_dila_service_without_siret_is_not_imported(
    dila_cleaner: OrganismesCleaner, siret_found: str | None
):
    raw_organisme = _raw_organisme_dila(_dila_service(), siret_found=siret_found)

    assert dila_cleaner.clean(raw_organisme) is None


def test_dila_does_not_read_unverified_siret_from_export(
    dila_cleaner: OrganismesCleaner,
):
    raw_organisme = _raw_organisme_dila(
        _dila_service(siret=DILA_SIRET_VALUE), siret_found=None
    )

    assert dila_cleaner.clean(raw_organisme) is None


def test_dila_mapping_takes_precedence_over_lookup(dila_cleaner: OrganismesCleaner):
    raw_organisme = _raw_organisme_dila(
        _dila_service(siret=DILA_SIRET_VALUE), external_id="dila-mapped"
    )

    organisme = dila_cleaner.clean(raw_organisme)

    assert organisme is not None
    assert organisme.siret == SIRET(code=MAPPED_SIRET_VALUE)


def test_dila_excluded_service_is_not_imported(dila_cleaner: OrganismesCleaner):
    raw_organisme = _raw_organisme_dila(_dila_service(), external_id="dila-excluded")

    assert dila_cleaner.clean(raw_organisme) is None


def test_dila_parent_id_is_the_direct_ancestor(dila_cleaner: OrganismesCleaner):
    parent = dila_cleaner.clean(
        _raw_organisme_dila(_dila_service(), external_id="parent-id")
    )
    child = dila_cleaner.clean(
        _raw_organisme_dila(
            _dila_service(ancestors=["parent-id", "root-id"]),
            external_id="child-id",
            siret_found="35600000000048",
        )
    )

    assert parent is not None
    assert child is not None
    assert child.parent_id == parent.entity_id


def test_dila_parent_id_is_none_when_no_ancestor(dila_cleaner: OrganismesCleaner):
    organisme = dila_cleaner.clean(_raw_organisme_dila(_dila_service(ancestors=[])))

    assert organisme is not None
    assert organisme.parent_id is None


def test_dila_ancestor_ids(dila_cleaner: OrganismesCleaner):
    parent = dila_cleaner.clean(
        _raw_organisme_dila(_dila_service(), external_id="parent-id")
    )
    root = dila_cleaner.clean(
        _raw_organisme_dila(
            _dila_service(), external_id="root-id", siret_found="35600000000048"
        )
    )
    raw_child = _raw_organisme_dila(
        _dila_service(ancestors=["parent-id", "root-id"]), external_id="child-id"
    )

    assert parent is not None
    assert root is not None
    assert dila_cleaner.dila_ancestor_ids(raw_child) == [
        parent.entity_id,
        root.entity_id,
    ]
    assert dila_cleaner.dila_ancestor_ids(_raw_organisme(_ege())) == []


def test_dila_entity_id_is_stable_across_cleans(dila_cleaner: OrganismesCleaner):
    first = dila_cleaner.clean(
        _raw_organisme_dila(_dila_service(), external_id="dila-42")
    )
    second = dila_cleaner.clean(
        _raw_organisme_dila(_dila_service(), external_id="dila-42")
    )

    assert first is not None
    assert second is not None
    assert first.entity_id == second.entity_id


@pytest.mark.parametrize(
    "code_insee_commune",
    [None, "", "00042"],
    ids=["missing", "empty", "invalid_commune_code"],
)
def test_dila_localisation_is_none(
    dila_cleaner: OrganismesCleaner, code_insee_commune: str | None
):
    raw_organisme = _raw_organisme_dila(
        _dila_service(code_insee_commune=code_insee_commune)
    )

    organisme = dila_cleaner.clean(raw_organisme)

    assert organisme is not None
    assert organisme.localisation is None


def test_dila_coordinates_are_none_when_no_adresse(dila_cleaner: OrganismesCleaner):
    raw_organisme = _raw_organisme_dila(_dila_service(adresse=None))

    organisme = dila_cleaner.clean(raw_organisme)

    assert organisme is not None
    assert organisme.localisation is not None
    assert organisme.localisation.latitude is None
    assert organisme.localisation.longitude is None


def test_dila_date_creation_is_none_when_unparseable(dila_cleaner: OrganismesCleaner):
    raw_organisme = _raw_organisme_dila(
        _dila_service(date_creation_datetime="not-a-date")
    )

    organisme = dila_cleaner.clean(raw_organisme)

    assert organisme is not None
    assert organisme.date_creation is None


def test_dila_dedupe_by_siret_keeps_shallowest_service(
    dila_cleaner: OrganismesCleaner,
):
    root = dila_cleaner.clean(
        _raw_organisme_dila(_dila_service(), external_id="9-root")
    )
    direction = dila_cleaner.clean(
        _raw_organisme_dila(
            _dila_service(ancestors=["9-root"]), external_id="1-direction"
        )
    )
    assert root is not None
    assert direction is not None

    result = dila_cleaner.dedupe_by_siret(
        [direction, root], {direction.entity_id: 1, root.entity_id: 0}
    )

    assert result == [root]


def test_dila_dedupe_by_siret_falls_back_to_smallest_external_id_at_same_depth(
    dila_cleaner: OrganismesCleaner,
):
    first = dila_cleaner.clean(_raw_organisme_dila(_dila_service(), external_id="a"))
    second = dila_cleaner.clean(_raw_organisme_dila(_dila_service(), external_id="b"))
    assert first is not None
    assert second is not None

    result = dila_cleaner.dedupe_by_siret(
        [second, first], {first.entity_id: 2, second.entity_id: 2}
    )

    assert result == [first]


def _dila_with_cached_lookup(
    *,
    found: str | None = None,
    found_at: datetime | None = None,
    siret: str | None = None,
    homonyms: int = 1,
    external_id: str = "dila-1",
) -> RawOrganisme:
    raw_organisme = _raw_organisme_dila(
        _dila_service(siret=siret, homonyms=homonyms),
        external_id=external_id,
        siret_found=found,
    )
    raw_organisme.dila_siret_found_at = found_at
    return raw_organisme


DILA_NOM = "Ministère de l'Intérieur"


@pytest.mark.parametrize(
    "raw_organisme,expected",
    [
        pytest.param(
            _dila_with_cached_lookup(), DILA_NOM, id="siret_missing_and_uncached"
        ),
        pytest.param(
            _dila_with_cached_lookup(siret=DILA_SIRET_VALUE),
            DILA_SIRET_VALUE,
            id="export_siret_to_verify",
        ),
        pytest.param(
            _dila_with_cached_lookup(siret="260 600 473 00342"),
            DILA_SIRET_VALUE,
            id="export_siret_with_spaces",
        ),
        pytest.param(
            _dila_with_cached_lookup(siret=DILA_SIRET_VALUE, homonyms=3),
            DILA_SIRET_VALUE,
            id="export_siret_of_homonym",
        ),
        pytest.param(_dila_with_cached_lookup(homonyms=2), None, id="homonym_name"),
        pytest.param(
            _dila_with_cached_lookup(external_id="dila-mapped"), None, id="mapped"
        ),
        pytest.param(
            _dila_with_cached_lookup(external_id="dila-excluded"), None, id="excluded"
        ),
        pytest.param(
            _dila_with_cached_lookup(found="", found_at=datetime.now(timezone.utc)),
            None,
            id="recently_cached",
        ),
        pytest.param(
            _dila_with_cached_lookup(
                found="", found_at=datetime.now(timezone.utc) - timedelta(days=31)
            ),
            DILA_NOM,
            id="cache_older_than_max_age",
        ),
        pytest.param(
            _dila_with_cached_lookup(
                found="",
                found_at=datetime.now(timezone.utc)
                - timedelta(days=30)
                + timedelta(minutes=1),
            ),
            None,
            id="cache_just_under_max_age",
        ),
        pytest.param(
            _dila_with_cached_lookup(found=""),
            DILA_NOM,
            id="cached_without_timestamp",
        ),
        pytest.param(_raw_organisme(_ege()), None, id="other_referentiel"),
        pytest.param(_raw_organisme_dila(None), None, id="no_data"),
        pytest.param(
            _raw_organisme_dila(_dila_service(nom="   "), siret_found=None),
            None,
            id="nom_blank",
        ),
    ],
)
def test_dila_siret_query(
    dila_cleaner: OrganismesCleaner,
    raw_organisme: RawOrganisme,
    expected: str | None,
):
    assert dila_cleaner.dila_siret_query(raw_organisme) == expected


def test_dila_siret_query_respects_configured_max_age(categories_csv: Path):
    cleaner = OrganismesCleaner(
        categories_csv_path=categories_csv, dila_siret_lookup_max_age_days=7
    )
    raw_organisme = _dila_with_cached_lookup(
        found="", found_at=datetime.now(timezone.utc) - timedelta(days=8)
    )

    assert cleaner.dila_siret_query(raw_organisme) == DILA_NOM


def test_default_dila_mapping_is_loaded(categories_csv: Path):
    cleaner = OrganismesCleaner(
        categories_csv_path=categories_csv,
        dila_siret_lookup_max_age_days=DILA_SIRET_LOOKUP_MAX_AGE_DAYS,
    )
    # "Sénat": a SIRET found by a targeted manual search.
    raw_organisme = _raw_organisme_dila(
        _dila_service(nom="Sénat"),
        external_id=_SENAT_DILA_ID,
        siret_found=None,
    )

    organisme = cleaner.clean(raw_organisme)

    assert organisme is not None
    assert organisme.siret == SIRET(code="11000002300017")
