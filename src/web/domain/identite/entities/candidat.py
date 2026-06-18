from dataclasses import dataclass
from uuid import UUID

from ddd.aggregate_root import AggregateRoot, factory
from pydantic import EmailStr

from domain.identite.events.candidat_events import ProfilCandidatCree


@dataclass(kw_only=True)
class Candidat(AggregateRoot):
    _email: EmailStr
    _prenom: str
    _nom: str
    _resume: str

    @classmethod
    @factory(ProfilCandidatCree)
    def create(
        cls,
        email: EmailStr,
        prenom: str,
        nom: str,
        resume: str,
        user_id: UUID,
    ) -> "Candidat":
        return cls(
            entity_id=user_id,
            _email=email,
            _prenom=prenom,
            _nom=nom,
            _resume=resume,
        )

    @classmethod
    def build(
        cls,
        entity_id: UUID,
        email: EmailStr,
        prenom: str,
        nom: str,
        resume: str,
    ) -> "Candidat":
        return cls(
            entity_id=entity_id,
            _email=email,
            _prenom=prenom,
            _nom=nom,
            _resume=resume,
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
    def resume(self) -> str:
        return self._resume
