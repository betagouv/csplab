from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import UUID

from ddd.aggregate_root import AggregateRoot, factory, mutate

from domain.recruteur.entities.etape_recrutement import EtapeRecrutement
from domain.recruteur.errors.erreur_recrutement import CandidatureDejaPresente
from domain.recruteur.events.recrutement_events import (
    CandidatRecrute,
    CandidatureRecue,
    EtapesAppliquees,
    RecrutementCree,
    ResponsableAjoute,
)
from domain.recruteur.value_objects.position_candidature import PositionCandidature
from domain.recruteur.value_objects.recrutement_status import RecrutementStatus


@dataclass(kw_only=True)
class Recrutement(AggregateRoot):
    _offre_id: UUID  # cross-BC FK → offer (ingestion BC), opaque
    _organisme_id: UUID  # intra-BC FK → OrganismeRecruteur
    _etapes: tuple[EtapeRecrutement, ...]
    _status: RecrutementStatus
    _positions: tuple[PositionCandidature, ...]  # placement in the pipeline
    _responsables_ids: tuple[UUID, ...]  # cross-BC FKs → HR users (identite BC)
    _derniere_activite_le: datetime
    _candidat_recrute_id: UUID | None = None  # cross-BC FK → candidate

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
            _status=RecrutementStatus.ACTIF,
            _positions=(),
            _responsables_ids=(),
            _derniere_activite_le=datetime.now(tz=timezone.utc),
            _candidat_recrute_id=None,
        )

    @classmethod
    def build(
        cls,
        entity_id: UUID,
        offre_id: UUID,
        organisme_id: UUID,
        etapes: tuple[EtapeRecrutement, ...],
        status: RecrutementStatus,
        positions: tuple[PositionCandidature, ...],
        responsables_ids: tuple[UUID, ...],
        derniere_activite_le: datetime,
        candidat_recrute_id: UUID | None = None,
    ) -> "Recrutement":
        return cls(
            entity_id=entity_id,
            _offre_id=offre_id,
            _organisme_id=organisme_id,
            _etapes=etapes,
            _status=status,
            _positions=positions,
            _responsables_ids=responsables_ids,
            _derniere_activite_le=derniere_activite_le,
            _candidat_recrute_id=candidat_recrute_id,
        )

    @property
    def offre_id(self) -> UUID:
        return self._offre_id

    @property
    def status(self) -> RecrutementStatus:
        return self._status

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
    def responsables_ids(self) -> tuple[UUID, ...]:
        return self._responsables_ids

    @property
    def derniere_activite_le(self) -> datetime:
        return self._derniere_activite_le

    @property
    def candidat_recrute_id(self) -> UUID | None:
        return self._candidat_recrute_id

    @mutate(EtapesAppliquees)
    def appliquer_etapes(self, etapes: tuple[EtapeRecrutement, ...]) -> None:
        self._etapes = etapes
        self._derniere_activite_le = datetime.now(tz=timezone.utc)

    @mutate(ResponsableAjoute)
    def ajouter_responsable(self, agent_id: UUID) -> None:
        self._responsables_ids = (*self._responsables_ids, agent_id)
        self._derniere_activite_le = datetime.now(tz=timezone.utc)

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
        self._derniere_activite_le = datetime.now(tz=timezone.utc)

    @mutate(CandidatRecrute)
    def recruter_candidat(self, candidat_id: UUID) -> None:
        self._candidat_recrute_id = candidat_id
        self._status = RecrutementStatus.ARCHIVE
        self._derniere_activite_le = datetime.now(tz=timezone.utc)
