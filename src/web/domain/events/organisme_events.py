from dataclasses import dataclass
from uuid import UUID

from domain.ddd.domain_event import DomainEvent
from domain.value_objects.localisation import Localisation
from domain.value_objects.siret import SIRET
from domain.value_objects.verse import Verse


@dataclass(frozen=True)
class OrganismeCree(DomainEvent):
    nom: str
    versant: Verse
    localisation: Localisation | None
    siret: SIRET | None
    parent_id: UUID | None
    config_recrutement: list[str]

@dataclass(frozen=True)
class ConfigRecrutementModifiee(DomainEvent):
    config: list[str]
