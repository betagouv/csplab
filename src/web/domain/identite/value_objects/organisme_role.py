from dataclasses import dataclass
from uuid import UUID


@dataclass
class OrganismeRole:
    organisme_uuid: UUID
    nom: str
    role: str
