from dataclasses import dataclass
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
