import pytest

from domain.value_objects.siret_candidate import SiretCandidate
from infrastructure.gateways.siret_matching import (
    best_candidate,
    embassy_matches,
    is_potential_employer,
    name_score,
    normalize_name,
)


def _candidate(
    denomination: str,
    nature_juridique: str | None = "7120",
    siret: str | None = "11000007200014",
) -> SiretCandidate:
    return SiretCandidate(
        siret=siret,
        siren=(siret or "000000000")[:9],
        denomination=denomination,
        nature_juridique=nature_juridique,
    )


@pytest.mark.parametrize(
    "nature_juridique,is_public,is_associative",
    [
        ("4110", True, False),
        ("7113", True, False),
        ("7220", True, False),
        ("7389", True, False),
        ("7490", True, False),
        ("9220", False, True),
        ("5710", False, False),
        ("6220", False, False),
        (None, False, False),
    ],
)
def test_legal_category(nature_juridique, is_public, is_associative):
    candidate = _candidate("X", nature_juridique=nature_juridique)

    assert candidate.is_public is is_public
    assert candidate.is_associative is is_associative


def test_normalize_name():
    assert (
        normalize_name("  Ministère de l'Europe et des Affaires étrangères ")
        == "ministere europe affaires etrangeres"
    )


def test_name_score_identical():
    assert name_score("Sénat", "SENAT") == 1.0


def test_name_score_without_common_word():
    assert name_score("Direction de la communication", "ELECTRICITE DE FRANCE") < 0.5


class TestBestCandidate:
    def test_retains_the_best_scored_public_candidate(self):
        retained = best_candidate(
            "Agence nationale de la recherche",
            [
                _candidate("AGENCE NATIONALE DE LA RECHERCHE", nature_juridique="5710"),
                _candidate("AGENCE NATIONALE DU SPORT", siret="13001926300015"),
                _candidate("AGENCE NATIONALE DE LA RECHERCHE", siret="13000250400020"),
            ],
            threshold=0.85,
        )

        assert retained is not None
        assert retained.candidate.siret == "13000250400020"
        assert retained.score == 1.0

    def test_never_retains_an_associative_candidate(self):
        retained = best_candidate(
            "Mission Sport",
            [_candidate("MISSION SPORT", nature_juridique="9220")],
            0.85,
        )

        assert retained is None

    def test_does_not_retain_a_candidate_below_the_threshold(self):
        retained = best_candidate(
            "Bureau gestion officiers",
            [_candidate("MINISTERE DES ARMEES")],
            threshold=0.85,
        )

        assert retained is None

    def test_ignores_a_candidate_without_siret(self):
        retained = best_candidate("Sénat", [_candidate("SENAT", siret=None)], 0.85)

        assert retained is None


@pytest.mark.parametrize(
    "name,denomination,expected",
    [
        ("Ambassade de France au Japon - Tokyo", "AMBASSADE DE FRANCE AU JAPON", True),
        (
            "Ambassade de France en Côte d'Ivoire - Abidjan",
            "AMBASSADE DE FRANCE EN COTE D IVOIRE",
            True,
        ),
        ("Ambassade de France au Japon - Tokyo", "AMBASSADE DE FRANCE EN CHINE", False),
        ("Consulat de France à Osaka", "AMBASSADE DE FRANCE AU JAPON", False),
        ("Ambassade de France au Japon", "AMICALE DES FRANCAIS DU JAPON", False),
    ],
)
def test_embassy_matches(name, denomination, expected):
    assert embassy_matches(name, denomination) is expected


@pytest.mark.parametrize(
    "name,type_organisme,expected",
    [
        ("Télécom Paris", "Établissement d'enseignement", True),
        ("Ministère de la Culture", "Administration centrale (ou Ministère)", True),
        ("Premier ministre", "Administration centrale (ou Ministère)", True),
        ("Cour des comptes", "Juridiction", True),
        ("Bureau des marchés", "Administration centrale (ou Ministère)", False),
        ("Bureau des marchés", "Établissement public", False),
        ("Service juridique et économique", "Établissement public", False),
        (
            "Agence de l'eau Loire-Bretagne - Délégation Centre-Loire",
            "Établissement public",
            False,
        ),
        ("Pôle numérique", "Service à compétence nationale", False),
        ("Sous-direction des affaires financières", "Établissement public", False),
        ("Préfecture du Rhône", "Service déconcentré", False),
    ],
)
def test_is_potential_employer(name, type_organisme, expected):
    assert is_potential_employer(name, type_organisme) is expected
