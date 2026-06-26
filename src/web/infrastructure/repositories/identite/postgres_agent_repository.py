from uuid import UUID

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

    def get_by_ids(self, ids: list[UUID]) -> list[Agent]:
        profils = ProfilAgentModel.objects.select_related("utilisateur").filter(
            utilisateur__username__in=[str(id) for id in ids]
        )
        return [profil.to_entity() for profil in profils]

    def create(self, utilisateur: Utilisateur, agent: Agent) -> Agent:
        ProfilAgentModel.from_entity(utilisateur, agent).save()
        return agent
