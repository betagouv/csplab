from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import UUID

from ddd.aggregate_root import AggregateRoot, factory, mutate

from domain.recruteur.entities.etape_recrutement import EtapeRecrutement
from domain.recruteur.errors.erreur_recrutement import CandidatureDejaPresente
from domain.recruteur.events.recrutement_events import (
    CandidatureRecue,
    EtapesAppliquees,
    RecrutementCree,
    ResponsableAjoute,
)
from domain.recruteur.value_objects.position_candidature import PositionCandidature


@dataclass(kw_only=True)
class Recrutement(AggregateRoot):
    _offre_id: UUID  # cross-BC FK → offer (ingestion BC), opaque
    _organisme_id: UUID  # intra-BC FK → OrganismeRecruteur
    _etapes: tuple[EtapeRecrutement, ...]
    _positions: tuple[PositionCandidature, ...]  # placement in the pipeline
    _responsables: tuple[UUID, ...]  # cross-BC FKs → HR users (identite BC)
    _derniere_activite_le: datetime

    @classmethod
    @factory(RecrutementCree)
    def create(
        cls,
        offre_id: UUID,
        organisme_id: UUID,
        etapes: tuple[EtapeRecrutement, ...],
    ) -> "Recrutement":
        return cls(
            _offre_id=offre_id,
            _organisme_id=organisme_id,
            _etapes=etapes,
            _positions=(),
            _responsables=(),
            _derniere_activite_le=datetime.now(tz=timezone.utc),
        )

    @classmethod
    def build(
        cls,
        entity_id: UUID,
        offre_id: UUID,
        organisme_id: UUID,
        etapes: tuple[EtapeRecrutement, ...],
        positions: tuple[PositionCandidature, ...],
        responsables: tuple[UUID, ...],
        derniere_activite_le: datetime,
    ) -> "Recrutement":
        return cls(
            entity_id=entity_id,
            _offre_id=offre_id,
            _organisme_id=organisme_id,
            _etapes=etapes,
            _positions=positions,
            _responsables=responsables,
            _derniere_activite_le=derniere_activite_le,
        )

    @property
    def offre_id(self) -> UUID:
        return self._offre_id

    @property
    def organisme_id(self) -> UUID:
        return self._organisme_id

    @property
    def etapes(self) -> tuple[EtapeRecrutement, ...]:
        return self._etapes

    @property
    def positions(self) -> tuple[PositionCandidature, ...]:
        return self._positions

    @property
    def responsables(self) -> tuple[UUID, ...]:
        return self._responsables

    @property
    def derniere_activite_le(self) -> datetime:
        return self._derniere_activite_le

    @mutate(EtapesAppliquees)
    def appliquer_etapes(self, etapes: tuple[EtapeRecrutement, ...]) -> None:
        self._etapes = etapes

    @mutate(ResponsableAjoute)
    def ajouter_responsable(self, agent_id: UUID) -> None:
        self._responsables = (*self._responsables, agent_id)

    @mutate(CandidatureRecue)
    def recevoir_candidature(self, candidature_id: UUID) -> None:
        existing_ids = {p.candidature_id for p in self._positions}
        if candidature_id in existing_ids:
            raise CandidatureDejaPresente(candidature_id=candidature_id)
        position = PositionCandidature(
            candidature_id=candidature_id,
            etape_id=self._etapes[0].entity_id,
            ordre=None,
        )
        self._positions = (position, *self._positions)
