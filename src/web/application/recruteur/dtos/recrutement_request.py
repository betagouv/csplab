from dataclasses import dataclass
from uuid import UUID

from domain.identite.entities.utilisateurs import Utilisateur


@dataclass(kw_only=True)
class RecrutementRequest:
    organisme_id: UUID
    recrutement_id: UUID
    utilisateur: Utilisateur
