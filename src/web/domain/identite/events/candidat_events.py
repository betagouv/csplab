from dataclasses import dataclass

from ddd.domain_event import DomainEvent
from pydantic import EmailStr, HttpUrl


@dataclass(frozen=True)
class ProfilCandidatCree(DomainEvent):
    email: EmailStr
    prenom: str
    nom: str
    resume: str
    linkedin: HttpUrl
