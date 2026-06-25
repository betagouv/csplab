from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from ddd.aggregate_root import AggregateRoot


@dataclass(kw_only=True)
class CandidatureRecruteur(AggregateRoot):
    _candidat_id: UUID
    _offre_id: UUID
    _documents: tuple[UUID, ...] | None = None
    _soumise_le: datetime | None = None
    _mise_a_jour_le: datetime | None = None

    @classmethod
    def build(
        cls,
        candidat_id: UUID,
        offre_id: UUID,
        entity_id: UUID,
        documents: tuple[UUID, ...] | None = None,
        soumise_le: datetime | None = None,
        mise_a_jour_le: datetime | None = None,
    ) -> "CandidatureRecruteur":

        return cls(
            entity_id=entity_id,
            _candidat_id=candidat_id,
            _offre_id=offre_id,
            _documents=documents,
            _soumise_le=soumise_le,
            _mise_a_jour_le=mise_a_jour_le,
        )

    @property
    def candidat_id(self) -> UUID:
        return self._candidat_id

    @property
    def offre_id(self) -> UUID:
        return self._offre_id

    @property
    def documents(self) -> tuple[UUID, ...] | None:
        return self._documents

    @property
    def soumise_le(self) -> datetime | None:
        return self._soumise_le

    @property
    def mise_a_jour_le(self) -> datetime | None:
        return self._mise_a_jour_le
