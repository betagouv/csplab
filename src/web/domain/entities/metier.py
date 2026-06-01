from dataclasses import dataclass, field
from typing import List, Optional
from uuid import UUID, uuid4

from domain.ddd.entity_interface import IEntity
from domain.value_objects.verse import Verse


@dataclass
class Metier(IEntity):
    external_id: str
    libelle: str
    description: str
    domaine_fonctionnel_code: str
    versants: List[Verse]
    activites: Optional[List[str]] = None
    conditions_particulieres: Optional[List[str]] = None
    offer_family_code: Optional[str] = (
        None  # not unique by metier, but can be used to link an offer to some metiers
    )
    id: UUID = field(default_factory=uuid4)
