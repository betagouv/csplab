from domain.identite.entities.agent import Agent
from domain.identite.entities.utilisateurs import Utilisateur
from domain.identite.repositories.agent_repository_interface import IAgentRepository
from infrastructure.django_apps.users.models import ProfilAgentModel


class PostgresAgentRepository(IAgentRepository):
    def get_by_email(self, email: str) -> Agent | None:
        try:
            profil = ProfilAgentModel.objects.select_related("utilisateur").get(
                utilisateur__email=email
            )
            return profil.to_entity()
        except ProfilAgentModel.DoesNotExist:
            return None

    def create(self, utilisateur: Utilisateur, agent: Agent) -> Agent:
        ProfilAgentModel.from_entity(utilisateur, agent).save()
        return agent
