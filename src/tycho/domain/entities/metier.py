from dataclasses import dataclass, field
from typing import Dict, List, Optional
from uuid import UUID, uuid4

from domain.interfaces.entity_interface import IEntity
from domain.value_objects.competence import Competence
from domain.value_objects.verse import Verse


@dataclass
class Metier(IEntity):
    libelle: str
    description: str
    competences: List[Competence]
    domaine_fonctionnel: UUID
    activites: List[str]
    versant: List[Verse]
    competences_par_versant: Optional[Dict[Verse, Optional[str]]] = None
    id: UUID = field(default_factory=uuid4)
