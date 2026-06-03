from dataclasses import dataclass
from uuid import UUID

from ddd.domain_event import DomainEvent
from referentiel.value_objects.localisation import Localisation
from referentiel.value_objects.verse import Verse

from domain.identite.value_objects.siret import SIRET


@dataclass(frozen=True)
class OrganismeCree(DomainEvent):
    nom: str
    versant: Verse
    localisation: Localisation | None
    siret: SIRET | None
    parent_id: UUID | None
