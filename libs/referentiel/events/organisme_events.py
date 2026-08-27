from dataclasses import dataclass
from datetime import date
from uuid import UUID

from ddd.domain_event import DomainEvent

from referentiel.value_objects.localisation import Localisation
from referentiel.value_objects.siret import SIRET
from referentiel.value_objects.verse import Verse


@dataclass(frozen=True)
class OrganismeCree(DomainEvent):
    nom: str
    versant: Verse
    localisation: Localisation | None
    siret: SIRET
    parent_id: UUID | None
    external_id: str | None = None
    referentiel: str | None = None
    millesime: str | None = None
    gestion_ats: bool | None = False
    date_creation: date | None = None
    date_derniere_activite: date | None = None
