from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import UUID

from ddd.aggregate_root import AggregateRoot, factory, mutate, query

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
    _mis_a_jour_par_id: UUID
    _mis_a_jour_le: datetime
    _supprimee_par_id: UUID | None = None
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
            _mis_a_jour_par_id=publie_par_id,
            _mis_a_jour_le=now,
        )

    @classmethod
    def build(
        cls,
        entity_id: UUID,
        candidature_id: UUID,
        message: str,
        publie_par_id: UUID,
        publie_le: datetime,
        mis_a_jour_par_id: UUID,
        mis_a_jour_le: datetime,
        supprimee_par_id: UUID | None = None,
        supprimee_le: datetime | None = None,
    ) -> "Note":
        return cls(
            entity_id=entity_id,
            _candidature_id=candidature_id,
            _message=message,
            _publie_par_id=publie_par_id,
            _publie_le=publie_le,
            _mis_a_jour_par_id=mis_a_jour_par_id,
            _mis_a_jour_le=mis_a_jour_le,
            _supprimee_par_id=supprimee_par_id,
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
    def mis_a_jour_par_id(self) -> UUID:
        return self._mis_a_jour_par_id

    @property
    def mis_a_jour_le(self) -> datetime:
        return self._mis_a_jour_le

    @property
    def supprimee_par_id(self) -> UUID | None:
        return self._supprimee_par_id

    @property
    def supprimee_le(self) -> datetime | None:
        return self._supprimee_le

    @query
    def est_supprimee(self) -> bool:
        return self._supprimee_le is not None

    @mutate(NoteEditee)
    def modifier(self, message: str, mis_a_jour_par_id: UUID) -> None:
        self._message = message
        self._mis_a_jour_par_id = mis_a_jour_par_id
        self._mis_a_jour_le = datetime.now(tz=timezone.utc)

    @mutate(NoteSupprimee)
    def supprimer(self, supprime_par_id: UUID) -> None:
        now = datetime.now(tz=timezone.utc)
        self._supprimee_par_id = supprime_par_id
        self._supprimee_le = now
        self._mis_a_jour_par_id = supprime_par_id
        self._mis_a_jour_le = now  # TODO : check vs auto now in model
