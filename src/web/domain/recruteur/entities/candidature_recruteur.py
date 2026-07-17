from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import UUID

from ddd.aggregate_root import AggregateRoot, mutate

from domain.recruteur.events.candidature_events import CandidatureRecue


# todo when back for Kanban:
# CandidatureTraitee: moved from step
# CandidaturePositionEnforced: maybe, waiting for UX
# CandidatureRefusee,
# CandidatureAcceptee
# for now: simple class to read data
@dataclass(kw_only=True)
class CandidatureRecruteur(AggregateRoot):
    _candidat_id: UUID
    _recrutement_id: UUID
    _etape_id: UUID
    _derniere_activite_le: datetime

    @classmethod
    def build(
        cls,
        entity_id: UUID,
        candidat_id: UUID,
        recrutement_id: UUID,
        etape_id: UUID,
        derniere_activite_le: datetime,
    ) -> "CandidatureRecruteur":
        return cls(
            entity_id=entity_id,
            _candidat_id=candidat_id,
            _recrutement_id=recrutement_id,
            _etape_id=etape_id,
            _derniere_activite_le=derniere_activite_le,
        )

    @mutate(CandidatureRecue)
    def recevoir_candidature(self, etape_id: UUID, candidat_id: UUID) -> None:
        self._etape_id = etape_id
        self._candidat_id = candidat_id
        self._derniere_activite_le = datetime.now(tz=timezone.utc)

    @property
    def candidat_id(self) -> UUID:
        return self._candidat_id

    @property
    def recrutement_id(self) -> UUID:
        return self._recrutement_id

    @property
    def etape_id(self) -> UUID:
        return self._etape_id

    @property
    def derniere_activite_le(self) -> datetime:
        return self._derniere_activite_le
