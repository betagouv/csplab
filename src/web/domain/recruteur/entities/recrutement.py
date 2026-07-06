from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from ddd.aggregate_root import AggregateRoot

from domain.recruteur.entities.etape_recrutement import EtapeRecrutement
from domain.recruteur.value_objects.statut_recrutement import StatutRecrutement

# todo:
# RecrutementCree (with init steps)
# RecrutementClot
# ResponsableAjoute
# for now: simple class to read data

# todo: business rule:
# if candidat_recrute_id is not None, status must be ARCHIVE


@dataclass(kw_only=True)
class Recrutement(AggregateRoot):
    _offre_id: UUID
    _organisme_id: UUID
    _etapes: tuple[EtapeRecrutement, ...]
    _candidatures: tuple[UUID, ...]
    _responsables: tuple[UUID, ...]
    _status: StatutRecrutement
    _candidat_recrute_id: UUID | None = None
    _derniere_activite_le: datetime | None = None

    @classmethod
    def build(
        cls,
        offre_id: UUID,
        organisme_id: UUID,
        etapes: tuple[EtapeRecrutement, ...],
        candidatures: tuple[UUID, ...],
        responsables: tuple[UUID, ...],
        status: StatutRecrutement,
        candidat_recrute_id: UUID | None = None,
        derniere_activite_le: datetime | None = None,
    ) -> "Recrutement":
        return cls(
            _offre_id=offre_id,
            _organisme_id=organisme_id,
            _etapes=etapes,
            _candidatures=candidatures,
            _responsables=responsables,
            _status=status,
            _candidat_recrute_id=candidat_recrute_id,
            _derniere_activite_le=derniere_activite_le,
        )

    @property
    def offre_id(self) -> UUID:
        return self._offre_id

    @property
    def organisme_id(self) -> UUID:
        return self._organisme_id

    @property
    def status(self) -> StatutRecrutement:
        return self._status

    @property
    def etapes(self) -> tuple[EtapeRecrutement, ...]:
        return self._etapes

    @property
    def candidatures(self) -> tuple[UUID, ...]:
        return self._candidatures

    @property
    def responsables(self) -> tuple[UUID, ...]:
        return self._responsables

    @property
    def candidat_recrute_id(self) -> UUID | None:
        return self._candidat_recrute_id

    @property
    def derniere_activite_le(self) -> datetime | None:
        return self._derniere_activite_le
