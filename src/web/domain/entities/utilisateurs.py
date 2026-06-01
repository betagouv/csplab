from dataclasses import dataclass, field
from uuid import UUID, uuid4

from pydantic import EmailStr

from domain.interfaces.entity_interface import IUserEntity


@dataclass
class Utilisateur(IUserEntity):
    email: EmailStr
    prenom: str
    nom: str
    entity_id: UUID = field(default_factory=uuid4)
