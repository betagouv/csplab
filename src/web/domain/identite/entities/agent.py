from dataclasses import dataclass
from uuid import UUID, uuid4

from ddd.aggregate_root import AggregateRoot, factory
from pydantic import EmailStr

from domain.identite.events.agent_events import ProfilAgentCree


@dataclass(kw_only=True)
class Agent(AggregateRoot):
    _email: EmailStr
    _prenom: str
    _nom: str
    _matricule: str

    @classmethod
    @factory(ProfilAgentCree)
    def create(cls, event: ProfilAgentCree, entity_id: UUID | None = None) -> "Agent":
        return cls(
            entity_id=entity_id or uuid4(),
            _email=event.email,
            _prenom=event.prenom,
            _nom=event.nom,
            _matricule=event.matricule,
        )

    @classmethod
    def build(
        cls,
        entity_id: UUID,
        email: EmailStr,
        prenom: str,
        nom: str,
        matricule: str,
    ) -> "Agent":
        return cls(
            entity_id=entity_id,
            _email=email,
            _prenom=prenom,
            _nom=nom,
            _matricule=matricule,
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
    def matricule(self) -> str:
        return self._matricule
