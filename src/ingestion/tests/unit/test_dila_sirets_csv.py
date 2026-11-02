import csv
from collections import Counter
from uuid import UUID

from referentiel.value_objects.siret import SIRET

from domain.value_objects.siret_candidate import SiretCandidate
from infrastructure.gateways.organismes_cleaner import DILA_SIRETS_CSV

COLUMNS = [
    "dila_id",
    "nom_dila",
    "siret",
    "denomination_sirene",
    "nature_juridique",
    "source",
    "score",
]
EXCLUSION = "exclusion"
# Automatic name searches: only a public SIRET may come from them.
SEARCH_SOURCES = {
    "recherche_entreprises",
    "recherche_entreprises_ambassade",
    "recherche_entreprises_revue_manuelle",
}
# Manual decisions: the only sources allowed to carry a private SIRET.
MANUAL_SOURCES = {"recherche_siren_manuelle", "recherche_etablissement_manuelle"}
SOURCES = {"annuaire_dila", EXCLUSION} | SEARCH_SOURCES | MANUAL_SOURCES
SCORED_SOURCES = SEARCH_SOURCES
MIN_AUTOMATIC_SCORE = 0.85


def _rows() -> list[dict[str, str]]:
    with DILA_SIRETS_CSV.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter=";"))


def _candidate(row: dict[str, str]) -> SiretCandidate:
    return SiretCandidate(
        siret=row["siret"],
        siren=row["siret"][:9],
        denomination=row["denomination_sirene"],
        nature_juridique=row["nature_juridique"],
    )


ROWS = _rows()
MAPPED_ROWS = [row for row in ROWS if row["source"] != EXCLUSION]


def test_is_utf8_with_lf_line_endings():
    content = DILA_SIRETS_CSV.read_bytes()

    content.decode("utf-8")
    assert b"\r" not in content
    assert content.endswith(b"\n")


def test_has_the_expected_header():
    with DILA_SIRETS_CSV.open(encoding="utf-8") as f:
        assert next(csv.reader(f, delimiter=";")) == COLUMNS


def test_every_row_has_every_column():
    assert ROWS
    assert all(None not in row and len(row) == len(COLUMNS) for row in ROWS)


def test_dila_ids_are_unique_uuids():
    dila_ids = [row["dila_id"] for row in ROWS]

    for dila_id in dila_ids:
        UUID(dila_id)
    assert [i for i, n in Counter(dila_ids).items() if n > 1] == []


def test_every_row_has_a_name_and_a_known_source():
    assert all(row["nom_dila"].strip() for row in ROWS)
    assert {row["source"] for row in ROWS} <= SOURCES


def test_exclusions_have_no_siret():
    exclusions = [row for row in ROWS if row["source"] == EXCLUSION]

    assert exclusions
    assert all(not row["siret"] and not row["score"] for row in exclusions)


def _is_valid_siret(code: str) -> bool:
    try:
        SIRET(code=code)
    except ValueError:
        return False
    return True


def test_mapped_rows_have_a_valid_siret_and_legal_category():
    invalid = [
        row["dila_id"]
        for row in MAPPED_ROWS
        if not _is_valid_siret(row["siret"])
        or not row["denomination_sirene"].strip()
        or not (len(row["nature_juridique"]) == 4 and row["nature_juridique"].isdigit())
    ]

    assert invalid == []


def test_sirets_are_unique():
    sirets = [row["siret"] for row in MAPPED_ROWS]

    assert [s for s, n in Counter(sirets).items() if n > 1] == []


def test_legal_category_matches_the_source():
    def allowed(row: dict[str, str]) -> bool:
        candidate = _candidate(row)
        if row["source"] in SEARCH_SOURCES:
            return candidate.is_public
        if row["source"] == "annuaire_dila":
            return candidate.is_public or candidate.is_associative
        # MANUAL_SOURCES: any legal category, decided case by case.
        return True

    assert [row["dila_id"] for row in MAPPED_ROWS if not allowed(row)] == []


def test_score_matches_the_source():
    def valid(row: dict[str, str]) -> bool:
        if row["source"] not in SCORED_SOURCES:
            return row["score"] == ""
        try:
            score = float(row["score"])
        except ValueError:
            return False
        minimum = MIN_AUTOMATIC_SCORE if row["source"] == "recherche_entreprises" else 0
        return minimum <= score <= 1

    assert [row["dila_id"] for row in MAPPED_ROWS if not valid(row)] == []
