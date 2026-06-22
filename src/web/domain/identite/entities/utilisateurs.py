from dataclasses import dataclass

from ddd.entity import Entity
from pydantic import EmailStr


@dataclass(kw_only=True)
class Utilisateur(Entity):
    email: EmailStr
    prenom: str
    nom: str
    is_superuser: bool = False
