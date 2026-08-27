from dataclasses import dataclass
from datetime import datetime, timezone
from typing import List
from uuid import UUID

from ddd.aggregate_root import mutate
from referentiel.types import IBatchUpdate

from domain.recruteur.entities.candidature_recruteur import CandidatureRecruteur
from domain.recruteur.entities.etape_recrutement import EtapeRecrutement
from domain.recruteur.entities.organisme_recruteur import (
    OrganismeRecruteur,
)
from domain.recruteur.errors.recrutement_errors import (
    RecrutementCandidatureInexistante,
    RecrutementEtapeInexistante,
)
from domain.recruteur.events.recrutement_events import (
    EtapeCandidaturesChangees,
    RecrutementEtapesMisesAJour,
    RecrutementEtapesReinitialisees,
)
from domain.recruteur.value_objects.etape_data import EtapeData
from domain.recruteur.value_objects.statut_recrutement import StatutRecrutement


@dataclass(kw_only=True)
class Recrutement(OrganismeRecruteur):
    _offre_id: UUID
    _organisme_id: UUID
    _etapes: tuple[EtapeRecrutement, ...]
    _candidatures: tuple[UUID, ...]
    _agents: tuple[UUID, ...]
    _status: StatutRecrutement
    _candidat_recrute_id: UUID | None = None
    _derniere_activite_le: datetime

    @classmethod
    def build(  # type: ignore[override]
        cls,
        offre_id: UUID,
        organisme_id: UUID,
        etapes: tuple[EtapeRecrutement, ...],
        candidatures: tuple[UUID, ...],
        agents: tuple[UUID, ...],
        status: StatutRecrutement,
        derniere_activite_le: datetime,
        candidat_recrute_id: UUID | None = None,
    ) -> "Recrutement":
        return cls(
            entity_id=offre_id,
            _offre_id=offre_id,
            _organisme_id=organisme_id,
            _etapes=etapes,
            _candidatures=candidatures,
            _agents=agents,
            _status=status,
            _candidat_recrute_id=candidat_recrute_id,
            _derniere_activite_le=derniere_activite_le,
        )

    @mutate(EtapeCandidaturesChangees)
    def changer_etapes_candidatures(
        self, candidatures: List[CandidatureRecruteur], etape_cible_id: UUID
    ) -> IBatchUpdate[CandidatureRecruteur, RecrutementCandidatureInexistante]:
        if etape_cible_id not in [etape.entity_id for etape in self._etapes]:
            raise RecrutementEtapeInexistante(
                etape_id=etape_cible_id, recrutement_id=self.entity_id
            )
        successes: List[CandidatureRecruteur] = []
        failures: List[tuple[UUID, RecrutementCandidatureInexistante]] = []
        for candidature in candidatures:
            if candidature.recrutement_id != self.entity_id:
                failures.append(
                    (
                        candidature.entity_id,
                        RecrutementCandidatureInexistante(
                            candidature.entity_id,
                        ),
                    )
                )
            else:
                candidature.changer_etape(etape_id=etape_cible_id)
                for event in candidature.collect_events():
                    self.add_event(event)
                successes.append(candidature)
        # business rules about etapes order can be managed here
        self._derniere_activite_le = datetime.now(tz=timezone.utc)
        return {"successes": successes, "failures": failures}

    @mutate(RecrutementEtapesReinitialisees)
    def reinitialiser_etapes(
        self,
        etapes_organisme: tuple[EtapeRecrutement, ...],
    ):
        for step in self._etapes:
            step.delete()
            for event in step.collect_events():
                self.add_event(event)

        new_steps = []
        for step in etapes_organisme:
            new_step = EtapeRecrutement.create(nom=step.nom, categorie=step.categorie)
            new_steps.append(new_step)
            for event in new_step.collect_events():
                self.add_event(event)

        self._etapes = tuple(new_steps)
        self._derniere_activite_le = datetime.now(tz=timezone.utc)

    @mutate(RecrutementEtapesMisesAJour)
    def mettre_a_jour_etapes(
        self,
        etapes_data: tuple[EtapeData, ...],
    ):
        super()._validate(etapes_data)
        super()._apply(etapes_data)

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
    def agents(self) -> tuple[UUID, ...]:
        return self._agents

    @property
    def candidat_recrute_id(self) -> UUID | None:
        return self._candidat_recrute_id

    @property
    def derniere_activite_le(self) -> datetime:
        return self._derniere_activite_le
