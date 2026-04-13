from dataclasses import dataclass, field
from typing import List
from uuid import UUID, uuid4

from domain.interfaces.entity_interface import IEntity
from domain.value_objects.competence import Competence


@dataclass
class Metier(IEntity):
    libelle: str
    description: str
    competences: List[Competence]
    domaine_fonctionnel: UUID
    activites: List[str]
    id: UUID = field(default_factory=uuid4)
