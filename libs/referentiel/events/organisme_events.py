from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from ddd.domain_event import DomainEvent

from referentiel.value_objects.localisation import Localisation
from referentiel.value_objects.siret import SIRET
from referentiel.value_objects.verse import Verse


@dataclass(frozen=True)
class _OrganismeEventPayload(DomainEvent):
    nom: str
    versant: Verse
    localisation: Localisation | None
    siret: SIRET
    parent_id: UUID | None
    external_id: str | None = None
    referentiel: str | None = None
    millesime: str | None = None
    gestion_ats: bool | None = False
    date_creation: datetime | None = None
    date_derniere_activite: datetime | None = None
    entity_id: UUID | None = None


@dataclass(frozen=True)
class OrganismeCree(_OrganismeEventPayload):
    pass


@dataclass(frozen=True)
class OrganismeModifie(DomainEvent):
    nom: str | None
    versant: Verse | None
    gestion_ats: bool | None


@dataclass(frozen=True)
class OrganismeRemplace(_OrganismeEventPayload):
    pass
