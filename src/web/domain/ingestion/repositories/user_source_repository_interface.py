from typing import Protocol
from uuid import UUID

from domain.identite.entities.utilisateurs import Utilisateur


class IUserSourceRepository(Protocol):
    def get_allowed_source_ids(self, utilisateur: Utilisateur, source_ids: set[UUID]) -> set[UUID]: ...
