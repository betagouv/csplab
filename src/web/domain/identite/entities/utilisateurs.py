from dataclasses import dataclass, field

from ddd.entity import Entity
from pydantic import EmailStr

from domain.identite.value_objects.organisme_role import OrganismeRole


@dataclass(kw_only=True)
class Utilisateur(Entity):
    email: EmailStr
    prenom: str
    nom: str
    is_superuser: bool = False
    organisme_roles: list[OrganismeRole] = field(default_factory=list)
