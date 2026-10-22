from dataclasses import dataclass, field
from typing import List, Optional
from uuid import UUID, uuid4

from ddd.entity_interface import IEntity

from referentiel.value_objects.verse import Verse


@dataclass
class Metier(IEntity):
    external_id: str
    libelle: str
    description: str
    domaine_fonctionnel_code: str
    versants: List[Verse]
    offer_family_code: str  # not unique by metier, links an offer to some metiers
    activites: Optional[List[str]] = None
    conditions_particulieres: Optional[List[str]] = None
    id: UUID = field(default_factory=uuid4)
