from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import UUID

from ddd.aggregate_root import AggregateRoot, factory, mutate

from domain.recruteur.events.note_events import (
    NoteAjoutee,
    NoteEditee,
    NoteSupprimee,
)


@dataclass(kw_only=True)
class Note(AggregateRoot):
    _candidature_id: UUID
    _message: str
    _publie_par_id: UUID
    _publie_le: datetime
    _supprimee_le: datetime | None = None

    @classmethod
    @factory(NoteAjoutee)
    def create(
        cls,
        candidature_id: UUID,
        message: str,
        publie_par_id: UUID,
    ) -> "Note":
        now = datetime.now(tz=timezone.utc)
        return cls(
            _candidature_id=candidature_id,
            _message=message,
            _publie_par_id=publie_par_id,
            _publie_le=now,
        )

    @classmethod
    def build(
        cls,
        entity_id: UUID,
        candidature_id: UUID,
        message: str,
        publie_par_id: UUID,
        publie_le: datetime,
        supprimee_le: datetime | None = None,
    ) -> "Note":
        return cls(
            entity_id=entity_id,
            _candidature_id=candidature_id,
            _message=message,
            _publie_par_id=publie_par_id,
            _publie_le=publie_le,
            _supprimee_le=supprimee_le,
        )

    @property
    def candidature_id(self) -> UUID:
        return self._candidature_id

    @property
    def message(self) -> str:
        return self._message

    @property
    def publie_par_id(self) -> UUID:
        return self._publie_par_id

    @property
    def publie_le(self) -> datetime:
        return self._publie_le

    @property
    def supprimee_le(self) -> datetime | None:
        return self._supprimee_le

    @mutate(NoteEditee)
    def modifier(self, message: str) -> None:
        self._message = message

    @mutate(NoteSupprimee)
    def supprimer(self) -> None:
        now = datetime.now(tz=timezone.utc)
        self._supprimee_le = now
