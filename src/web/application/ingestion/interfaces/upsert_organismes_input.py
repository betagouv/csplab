from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from referentiel.value_objects.localisation import Localisation
from referentiel.value_objects.siret import SIRET
from referentiel.value_objects.verse import Verse


@dataclass
class OrganismeUpsertData:
    nom: str
    versant: Verse
    siret: SIRET
    localisation: Localisation | None
    parent_id: UUID | None
    external_id: str
    referentiel: str
    millesime: str
    gestion_ats: bool | None = False
    date_creation: datetime | None = None
    date_derniere_activite: datetime | None = None
    entity_id: UUID | None = None


@dataclass
class UpsertOrganismesInput:
    organismes: list[OrganismeUpsertData]
