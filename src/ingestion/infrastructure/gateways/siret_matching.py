"""Pure functions used to pick a reliable SIRET for a DILA service."""

import re
import unicodedata
from dataclasses import dataclass
from difflib import SequenceMatcher
from typing import Iterable, Optional

from domain.value_objects.siret_candidate import SiretCandidate

_STOP_WORDS = frozenset(
    "a au aux d de des du en et l la le les pour sur un une".split()
)

# DILA types of the services likely to be employers.
_POTENTIAL_EMPLOYER_TYPES = frozenset(
    {
        "Établissement public",
        "Établissement d'enseignement",
        "Service à compétence nationale",
        "Autorité administrative indépendante",
        "Autorité publique indépendante",
        "Institution",
        "Juridiction",
        "Groupement d'intérêt public",
        "Ambassade ou mission diplomatique",
    }
)
_POTENTIAL_EMPLOYER_PREFIXES = ("ministere", "premier ministre")
# A sub-unit inherits the DILA type of its parent ("Service juridique et
# économique" is typed "Établissement public"): these name prefixes give it
# away.
_SUB_UNIT_PREFIXES = (
    "bureau",
    "service",
    "direction",
    "sous-direction",
    "pole",
    "departement",
    "mission",
    "division",
    "cellule",
    "section",
    "secretariat",
    "unite",
    "delegation",
    "laboratoire",
    "antenne",
    "site ",
    "agence comptable",
    "cabinet",
    "conseiller",
    "inspection",
    "groupe",
    "atelier",
    "plateforme",
    "consulat",
    "college",
    "greffe",
    "parquet",
    "etat-major",
    "aides de camp",
    "premiere ",
    "deuxieme ",
    "troisieme ",
    "mediation",
    "communication",
)
# In DILA, "X - Y" names a sub-unit Y of X ("Université X - IUT").
_SUB_UNIT_SEPARATOR = " - "


@dataclass(frozen=True)
class ScoredCandidate:
    candidate: SiretCandidate
    score: float


def _strip_accents(text: str) -> str:
    return (
        unicodedata.normalize("NFKD", text or "")
        .encode("ascii", "ignore")
        .decode()
        .lower()
    )


def _words(name: str) -> list[str]:
    text = re.sub(r"[^a-z0-9]+", " ", _strip_accents(name))
    return [word for word in text.split() if word not in _STOP_WORDS]


def normalize_name(name: str) -> str:
    return " ".join(_words(name))


def name_score(dila_name: str, denomination: str) -> float:
    dila_words, denomination_words = _words(dila_name), _words(denomination)
    if not dila_words or not denomination_words:
        return 0.0
    coverage = len(set(dila_words) & set(denomination_words)) / len(set(dila_words))
    similarity = SequenceMatcher(
        None, " ".join(dila_words), " ".join(denomination_words)
    ).ratio()
    return round(0.6 * coverage + 0.4 * similarity, 3)


def _best(name: str, candidates: Iterable[SiretCandidate]) -> Optional[ScoredCandidate]:
    best: Optional[ScoredCandidate] = None
    for candidate in candidates:
        if not candidate.siret:
            continue
        scored = ScoredCandidate(candidate, name_score(name, candidate.denomination))
        if best is None or scored.score > best.score:
            best = scored
    return best


def best_public_candidate(
    name: str, candidates: Iterable[SiretCandidate]
) -> Optional[ScoredCandidate]:
    return _best(name, (c for c in candidates if c.is_public))


def best_associative_candidate(
    name: str, candidates: Iterable[SiretCandidate]
) -> Optional[ScoredCandidate]:
    return _best(name, (c for c in candidates if c.is_associative))


def best_candidate(
    name: str, candidates: Iterable[SiretCandidate], threshold: float
) -> Optional[ScoredCandidate]:
    """Best public candidate, if its score reaches the threshold.

    An associative candidate is never retained: those matching a service's
    name are almost always unrelated namesakes (sports club, staff
    association…).
    """
    best = best_public_candidate(name, candidates)
    if best is None or best.score < threshold:
        return None
    return best


def embassy_matches(name: str, denomination: str) -> bool:
    """ "Ambassade de France PAYS - Ville" ↔ "AMBASSADE DE FRANCE EN PAYS"."""
    name_without_city = name.split(_SUB_UNIT_SEPARATOR, maxsplit=1)[0]
    match = re.match(
        r"ambassade de france (.+)", " ".join(_strip_accents(name_without_city).split())
    )
    if match is None:
        return False
    denomination_words = re.sub(r"[^a-z]+", " ", _strip_accents(denomination)).split()
    if (
        denomination_words[:1] != ["ambassade"]
        or "france" not in denomination_words[:4]
    ):
        return False
    country = [
        word
        for word in re.sub(r"[^a-z]+", " ", match.group(1)).split()
        if word not in _STOP_WORDS
    ]
    return bool(country) and set(country) <= set(denomination_words) - _STOP_WORDS


def is_potential_employer(name: str, type_organisme: str) -> bool:
    """Whether a DILA service without SIRET is worth an alert: a ministry,
    public body, authority, court… but not one of its offices or units."""
    name = (name or "").strip()
    normalized = _strip_accents(name)
    if not (
        (type_organisme or "").strip() in _POTENTIAL_EMPLOYER_TYPES
        or normalized.startswith(_POTENTIAL_EMPLOYER_PREFIXES)
    ):
        return False
    return _SUB_UNIT_SEPARATOR not in name and not normalized.startswith(
        _SUB_UNIT_PREFIXES
    )
