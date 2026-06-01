from dataclasses import dataclass

from pydantic import EmailStr

from domain.interfaces.entity_interface import IEntity


@dataclass
class Utilisateur(IEntity):
    id: int
    email: EmailStr
    prenom: str
    nom: str
