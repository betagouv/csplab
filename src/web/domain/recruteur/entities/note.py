from dataclasses import dataclass
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

    @classmethod
    @factory(NoteAjoutee)
    def create(
        cls,
        candidature_id: UUID,
        message: str,
        publie_par_id: UUID,
    ) -> "Note":
        return cls(
            _candidature_id=candidature_id,
            _message=message,
            _publie_par_id=publie_par_id,
        )

    @classmethod
    def build(
        cls,
        entity_id: UUID,
        candidature_id: UUID,
        message: str,
        publie_par_id: UUID,
    ) -> "Note":
        return cls(
            entity_id=entity_id,
            _candidature_id=candidature_id,
            _message=message,
            _publie_par_id=publie_par_id,
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

    @mutate(NoteEditee)
    def modifier(self, message: str) -> None:
        self._message = message

    @mutate(NoteSupprimee)
    def supprimer(self) -> None:
        pass
