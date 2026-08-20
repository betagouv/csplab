from dataclasses import replace
from uuid import UUID

from domain.identite.entities.utilisateurs import Utilisateur
from domain.identite.repositories.utilisateur_repository_interface import (
    IUtilisateurRepository,
)
from domain.identite.value_objects.organisme_role import OrganismeRole
from domain.recruteur.value_objects.roles import AgentOrganismeRole

STATIC_ORGANISMES = [
    OrganismeRole(
        organisme_uuid=UUID("00000000-0000-0000-0000-000000000000"),
        nom="Ministère de la Transition Écologique",
        role=AgentOrganismeRole.RESPONSABLE.value,
    )
]


class GetUtilisateurDetailUsecase:
    def __init__(self, utilisateur_repository: IUtilisateurRepository):
        self.utilisateur_repository = utilisateur_repository

    def execute(self, entity_id: UUID) -> Utilisateur:
        utilisateur = self.utilisateur_repository.get_by_entity_id(entity_id)
        return replace(utilisateur, organismes=STATIC_ORGANISMES)
