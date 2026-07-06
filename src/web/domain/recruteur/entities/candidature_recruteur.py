from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from ddd.aggregate_root import AggregateRoot


# todo when back for Kanban:
# CandidatureRecue: added in first step
# CandidatureTraitee: moved from step
# CandidaturePositionEnforced: maybe, waiting for UX
# CandidatureRefusee,
# CandidatureAcceptee
# for now: simple class to read data
@dataclass(kw_only=True)
class CandidatureRecruteur(AggregateRoot):
    _recrutement_id: UUID
    _candidat_id: UUID
    _etapes_id: UUID
    _derniere_activite_le: datetime

    @classmethod
    def build(
        cls,
        recrutement_id: UUID,
        candidat_id: UUID,
        etapes_id: UUID,
        derniere_activite_le: datetime,
    ) -> "CandidatureRecruteur":
        return cls(
            _recrutement_id=recrutement_id,
            _candidat_id=candidat_id,
            _etapes_id=etapes_id,
            _derniere_activite_le=derniere_activite_le,
        )

    @property
    def recrutement_id(self) -> UUID:
        return self._recrutement_id

    @property
    def candidat_id(self) -> UUID:
        return self._candidat_id

    @property
    def etapes_id(self) -> UUID:
        return self._etapes_id

    @property
    def derniere_activite_le(self) -> datetime:
        return self._derniere_activite_le
