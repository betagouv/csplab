from dataclasses import dataclass
from uuid import UUID

from pydantic import EmailStr

from domain.identite.entities.agent import Agent
from domain.identite.entities.utilisateurs import Utilisateur
from domain.identite.errors.agent_errors import ProfilAgentExisteDeja
from domain.identite.errors.identite_errors import UtilisateurNexistePas
from domain.identite.repositories.agent_repository_interface import IAgentRepository
from domain.identite.repositories.utilisateur_repository_interface import (
    IUtilisateurRepository,
)
from domain.identite.services.organisme_permission_service import (
    OrganismePermissionService,
)
from domain.identite.value_objects.organisme_action import OrganismeAction


@dataclass
class CreateAgentInput:
    email: EmailStr
    prenom: str
    nom: str
    intitule_poste: str
    organisme_id: UUID
    utilisateur: Utilisateur


class CreateAgentUsecase:
    def __init__(
        self,
        agent_repository: IAgentRepository,
        utilisateur_repository: IUtilisateurRepository,
        permission_service: OrganismePermissionService,
    ):
        self.agent_repository = agent_repository
        self.utilisateur_repository = utilisateur_repository
        self.permission_service = permission_service

    def can_execute(self, input_data: CreateAgentInput) -> None:
        self.permission_service.est_autorise(
            action=OrganismeAction.CREATE_AGENT,
            utilisateur=input_data.utilisateur,
            organisme_id=input_data.organisme_id,
        )

    def execute(self, input_data: CreateAgentInput) -> Agent:
        self.can_execute(input_data)

        existing = self.agent_repository.get_by_email(input_data.email)
        if existing is not None:
            raise ProfilAgentExisteDeja(input_data.email)

        try:
            agent_utilisateur = self.utilisateur_repository.get_by_email(
                input_data.email
            )
        except UtilisateurNexistePas:
            agent_utilisateur = self.utilisateur_repository.create(
                Utilisateur(
                    email=input_data.email,
                    prenom=input_data.prenom,
                    nom=input_data.nom,
                )
            )

        agent = Agent.create(
            email=input_data.email,
            prenom=input_data.prenom,
            nom=input_data.nom,
            intitule_poste=input_data.intitule_poste,
            user_id=agent_utilisateur.entity_id,
        )

        return self.agent_repository.create(agent_utilisateur, agent)
