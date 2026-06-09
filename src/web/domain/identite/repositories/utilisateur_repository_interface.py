from typing import Protocol

from domain.identite.entities.utilisateurs import Utilisateur


class IUtilisateurRepository(Protocol):
    def get_by_entity_id(self, entity_id) -> Utilisateur: ...
