from dataclasses import dataclass
from uuid import UUID

from pydantic import EmailStr

from application.identite.context_services.organisme_permission_service import (
    can_execute,
)
from domain.identite.entities.agent import Agent
from domain.identite.entities.utilisateurs import Utilisateur
from domain.identite.errors.agent_errors import ProfilAgentExisteDeja
from domain.identite.errors.identite_errors import UtilisateurNexistePas
from domain.identite.repositories.agent_repository_interface import IAgentRepository
from domain.identite.repositories.utilisateur_repository_interface import (
    IUtilisateurRepository,
)
from domain.identite.value_objects.organisme_action import OrganismeAction


@dataclass
class CreateAgentInput:
    email: EmailStr
    organisme_id: UUID
    utilisateur: Utilisateur


class CreateAgentUsecase:
    def __init__(
        self,
        agent_repository: IAgentRepository,
        utilisateur_repository: IUtilisateurRepository,
    ):
        self.agent_repository = agent_repository
        self.utilisateur_repository = utilisateur_repository

    def execute(self, input_data: CreateAgentInput) -> Agent:
        can_execute(
            action=OrganismeAction.CREATE_AGENT,
            utilisateur=input_data.utilisateur,
            organisme_id=input_data.organisme_id,
        )

        existing = self.agent_repository.get_by_email(input_data.email)
        if existing is not None:
            raise ProfilAgentExisteDeja(input_data.email)

        try:
            agent_utilisateur = self.utilisateur_repository.get_by_email(
                input_data.email
            )
        except UtilisateurNexistePas:
            agent_utilisateur = self.utilisateur_repository.create(
                Utilisateur(email=input_data.email)
            )

        agent = Agent.create(
            email=input_data.email,
            user_id=agent_utilisateur.entity_id,
        )

        return self.agent_repository.create(agent_utilisateur, agent)
