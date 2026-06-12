from dataclasses import dataclass

from pydantic import EmailStr

from domain.identite.entities.agent import Agent
from domain.identite.entities.utilisateurs import Utilisateur
from domain.identite.errors.agent_errors import ProfilAgentAlreadyExists
from domain.identite.errors.identite_errors import UtilisateurDoesNotExist
from domain.identite.events.agent_events import ProfilAgentCree
from domain.identite.repositories.agent_repository_interface import IAgentRepository
from domain.identite.repositories.utilisateur_repository_interface import (
    IUtilisateurRepository,
)


@dataclass
class CreateAgentInput:
    email: EmailStr
    prenom: str
    nom: str
    intitule_poste: str


class CreateAgentUsecase:
    def __init__(
        self,
        agent_repository: IAgentRepository,
        utilisateur_repository: IUtilisateurRepository,
    ):
        self.agent_repository = agent_repository
        self.utilisateur_repository = utilisateur_repository

    def execute(self, input_data: CreateAgentInput) -> Agent:
        existing = self.agent_repository.get_by_email(input_data.email)
        if existing is not None:
            raise ProfilAgentAlreadyExists(input_data.email)

        event = ProfilAgentCree(
            email=input_data.email,
            prenom=input_data.prenom,
            nom=input_data.nom,
            intitule_poste=input_data.intitule_poste,
        )

        try:
            utilisateur = self.utilisateur_repository.get_by_email(input_data.email)
            agent = Agent.create(event, entity_id=utilisateur.entity_id)
        except UtilisateurDoesNotExist:
            agent = Agent.create(event)
            utilisateur = self.utilisateur_repository.create(
                Utilisateur(
                    entity_id=agent.entity_id,
                    email=agent.email,
                    prenom=agent.prenom,
                    nom=agent.nom,
                )
            )

        return self.agent_repository.create(utilisateur, agent)
