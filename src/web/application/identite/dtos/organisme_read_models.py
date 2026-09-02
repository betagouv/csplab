from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from referentiel.value_objects.siret import SIRET
from referentiel.value_objects.verse import Verse


@dataclass(frozen=True, kw_only=True)
class OrganismeReadModel:
    entity_id: UUID
    name: str
    siret: SIRET
    verse: Verse
    managed_ats: bool
    creation_date: datetime
    last_activity_date: datetime
    number_agents: int
    number_published_offers: int
