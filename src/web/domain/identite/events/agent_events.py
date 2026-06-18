from dataclasses import dataclass
from uuid import UUID

from ddd.domain_event import DomainEvent
from pydantic import EmailStr


@dataclass(frozen=True)
class ProfilAgentCree(DomainEvent):
    email: EmailStr
    prenom: str
    nom: str
    intitule_poste: str
    user_id: UUID
