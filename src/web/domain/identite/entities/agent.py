from dataclasses import dataclass
from uuid import UUID

from ddd.aggregate_root import AggregateRoot, factory
from pydantic import EmailStr

from domain.identite.events.agent_events import ProfilAgentCree


@dataclass(kw_only=True)
class Agent(AggregateRoot):
    _email: EmailStr
    _prenom: str
    _nom: str
    _intitule_poste: str

    @classmethod
    @factory(ProfilAgentCree)
    def create(
        cls,
        email: EmailStr,
        prenom: str,
        nom: str,
        intitule_poste: str,
        user_id: UUID,
    ) -> "Agent":
        return cls(
            entity_id=user_id,
            _email=email,
            _prenom=prenom,
            _nom=nom,
            _intitule_poste=intitule_poste,
        )

    @classmethod
    def build(
        cls,
        entity_id: UUID,
        email: EmailStr,
        prenom: str,
        nom: str,
        intitule_poste: str,
    ) -> "Agent":
        return cls(
            entity_id=entity_id,
            _email=email,
            _prenom=prenom,
            _nom=nom,
            _intitule_poste=intitule_poste,
        )

    @property
    def email(self) -> EmailStr:
        return self._email

    @property
    def prenom(self) -> str:
        return self._prenom

    @property
    def nom(self) -> str:
        return self._nom

    @property
    def intitule_poste(self) -> str:
        return self._intitule_poste
