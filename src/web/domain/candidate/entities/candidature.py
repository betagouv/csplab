from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import UUID

from ddd.aggregate_root import AggregateRoot, factory, mutate

from domain.candidate.events.candidature_events import (
    CandidatureSoumise,
    DocumentsDeposes,
    DossierCandidatureInitialise,
)
from domain.candidate.exceptions.candidature_errors import (
    CandidatureDejaSoumise,
    DossierCandidatureInvalide,
)
from domain.candidate.value_objects.statut_candidature import StatutCandidature


@dataclass(kw_only=True)
class CandidatureCandidat(AggregateRoot):
    _candidat_id: UUID
    _offre_id: UUID
    _statut: StatutCandidature
    _documents: tuple[UUID, ...] | None = None
    _soumise_le: datetime | None = None
    _mise_a_jour_le: datetime | None = None

    @classmethod
    @factory(DossierCandidatureInitialise)
    def create(cls, offre_id: UUID, candidat_id: UUID) -> "CandidatureCandidat":
        return cls(
            _candidat_id=candidat_id,
            _offre_id=offre_id,
            _statut=StatutCandidature.INITIAL,
            _mise_a_jour_le=datetime.now(tz=timezone.utc),
        )

    @classmethod
    def build(
        cls,
        candidat_id: UUID,
        offre_id: UUID,
        statut: StatutCandidature,
        entity_id: UUID,
        documents: tuple[UUID, ...] | None = None,
        soumise_le: datetime | None = None,
        mise_a_jour_le: datetime | None = None,
    ) -> "CandidatureCandidat":

        return cls(
            entity_id=entity_id,
            _candidat_id=candidat_id,
            _offre_id=offre_id,
            _statut=statut,
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
    def statut(self) -> StatutCandidature:
        return self._statut

    @property
    def documents(self) -> tuple[UUID, ...] | None:
        return self._documents

    @property
    def soumise_le(self) -> datetime | None:
        return self._soumise_le

    @property
    def mise_a_jour_le(self) -> datetime | None:
        return self._mise_a_jour_le

    @mutate(DocumentsDeposes)
    def deposer_documents(self, documents: tuple[UUID, ...]) -> None:
        if len(documents) == 0:
            raise DossierCandidatureInvalide(
                "Le dossier de candidature doit contenir au moins un document"
            )
        self._documents = documents
        self._mise_a_jour_le = datetime.now(tz=timezone.utc)

    @mutate(CandidatureSoumise)
    def soumettre_candidature(self) -> None:
        if self._statut == StatutCandidature.SOUMISE:
            raise CandidatureDejaSoumise(self.candidat_id, self.offre_id)
        self._statut = StatutCandidature.SOUMISE
        now = datetime.now(tz=timezone.utc)
        self._soumise_le = now
        self._mise_a_jour_le = now
