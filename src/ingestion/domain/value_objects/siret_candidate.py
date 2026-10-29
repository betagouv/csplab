from dataclasses import dataclass
from typing import Optional

# INSEE legal categories (level 2) of public-law legal entities: EPIC (41),
# State (71), local authorities (72), public administrative bodies (73), other
# public-law legal entities (74). The first digit of the SIREN is not enough:
# ONF, CEA, CNES or the Université de Toulouse have a SIREN starting with
# neither 1 nor 2.
_PUBLIC_LEGAL_CATEGORIES = ("41", "71", "72", "73", "74")
_ASSOCIATIVE_LEGAL_CATEGORY = "92"


@dataclass(frozen=True)
class SiretCandidate:
    siret: Optional[str]
    siren: str
    denomination: str
    nature_juridique: Optional[str]

    @property
    def is_public(self) -> bool:
        return (self.nature_juridique or "")[:2] in _PUBLIC_LEGAL_CATEGORIES

    @property
    def is_associative(self) -> bool:
        return (self.nature_juridique or "")[:2] == _ASSOCIATIVE_LEGAL_CATEGORY
