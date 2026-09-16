from uuid import UUID

from domain.identite.entities.agent import Agent
from domain.identite.entities.utilisateurs import Utilisateur
from domain.identite.repositories.agent_repository_interface import IAgentRepository
from domain.identite.value_objects.email import normalize_email
from infrastructure.django_apps.users.models import ProfilAgentModel


class PostgresAgentRepository(IAgentRepository):
    def get_by_email(self, email: str) -> Agent | None:
        try:
            profil = ProfilAgentModel.objects.select_related("utilisateur").get(
                utilisateur__email=normalize_email(email)
            )
            return profil.to_entity()
        except ProfilAgentModel.DoesNotExist:
            return None

    def exists(self, agent_id: UUID) -> bool:
        return ProfilAgentModel.objects.filter(utilisateur__username=agent_id).exists()

    def create(self, utilisateur: Utilisateur, agent: Agent) -> Agent:
        ProfilAgentModel.from_entity(utilisateur, agent).save()
        return agent
