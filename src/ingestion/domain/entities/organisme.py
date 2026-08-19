from dataclasses import dataclass, field
from typing import Optional
from uuid import UUID, uuid4

from referentiel.value_objects.localisation import Localisation
from referentiel.value_objects.siret import SIRET
from referentiel.value_objects.verse import Verse


@dataclass
class Organisme:
    nom: str
    versant: Verse
    siret: SIRET
    localisation: Optional[Localisation] = None
    parent_id: Optional[UUID] = None
    external_id: Optional[str] = None
    referentiel: Optional[str] = None
    millesime: Optional[str] = None
    id: UUID = field(default_factory=uuid4)
