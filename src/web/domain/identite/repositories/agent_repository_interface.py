from typing import Protocol
from uuid import UUID

from domain.identite.entities.agent import Agent
from domain.identite.entities.utilisateurs import Utilisateur


class IAgentRepository(Protocol):
    def create(self, utilisateur: Utilisateur, agent: Agent) -> Agent: ...
    def get_by_email(self, email: str) -> Agent | None: ...
    def exists(self, agent_id: UUID) -> bool: ...
