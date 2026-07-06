from dataclasses import dataclass
from uuid import UUID

from ddd.domain_event import DomainEvent


@dataclass(frozen=True)
class NoteAjoutee(DomainEvent):
    candidature_id: UUID
    publie_par_id: UUID
    message: str


@dataclass(frozen=True)
class NoteEditee(DomainEvent):
    message: str


@dataclass(frozen=True)
class NoteSupprimee(DomainEvent):
    pass
