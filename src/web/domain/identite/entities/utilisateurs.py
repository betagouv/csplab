from dataclasses import dataclass, field
from uuid import UUID, uuid4

from ddd.entity import Entity
from pydantic import EmailStr


@dataclass(kw_only=True)
class Utilisateur(Entity):
    email: EmailStr
    prenom: str
    nom: str
    entity_id: UUID = field(default_factory=uuid4)
