from dataclasses import dataclass, field
from uuid import UUID, uuid4

from pydantic import EmailStr

from domain.ddd.entity import Entity


@dataclass(kw_only=True)
class Utilisateur(Entity):
    email: EmailStr
    prenom: str
    nom: str
    entity_id: UUID = field(default_factory=uuid4)
