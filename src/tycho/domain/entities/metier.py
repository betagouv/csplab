from dataclasses import dataclass, field
from typing import List, Optional
from uuid import UUID, uuid4

from domain.interfaces.entity_interface import IEntity
from domain.value_objects.competence import Competence
from domain.value_objects.verse import Verse


@dataclass
class Metier(IEntity):
    libelle: str
    description: str
    domaine_fonctionnel: UUID
    versants: List[Verse]
    activites: Optional[List[str]] = None
    competences: Optional[List[Competence]] = None
    conditions_particulieres: Optional[str] = None
    id: UUID = field(default_factory=uuid4)
