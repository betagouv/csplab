from dataclasses import dataclass
from uuid import UUID, uuid4

from ddd.aggregate_root import AggregateRoot, factory
from pydantic import EmailStr, HttpUrl

from domain.identite.events.candidat_events import ProfilCandidatCree


@dataclass(kw_only=True)
class Candidat(AggregateRoot):
    _email: EmailStr
    _prenom: str
    _nom: str
    _resume: str
    _linkedin: HttpUrl

    @classmethod
    @factory(ProfilCandidatCree)
    def create(
        cls, event: ProfilCandidatCree, entity_id: UUID | None = None
    ) -> "Candidat":
        return cls(
            entity_id=entity_id or uuid4(),
            _email=event.email,
            _prenom=event.prenom,
            _nom=event.nom,
            _resume=event.resume,
            _linkedin=event.linkedin,
        )

    @classmethod
    def build(
        cls,
        entity_id: UUID,
        email: EmailStr,
        prenom: str,
        nom: str,
        resume: str,
        linkedin: HttpUrl,
    ) -> "Candidat":
        return cls(
            entity_id=entity_id,
            _email=email,
            _prenom=prenom,
            _nom=nom,
            _resume=resume,
            _linkedin=linkedin,
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

    @property
    def linkedin(self) -> HttpUrl:
        return self._linkedin
