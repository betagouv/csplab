from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True, kw_only=True)
class AgentOrganismeReadModel:
    entity_id: UUID
    organisme_id: UUID
    nom: str
    prenom: str
    email: str
    poste: str
    role: str
    date_derniere_activite: datetime | None
    date_creation_compte: datetime
    date_revocation: datetime | None = None
