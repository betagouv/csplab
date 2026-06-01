from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from domain.candidature.events.candidature_events import (
    CandidatureSoumise,
    DocumentsDeposes,
    DossierCandidatureCree,
)
from domain.candidature.exceptions import (
    CandidatureNePeutPasEtreSoumise,
    DossierCandidatureInvalide,
)
from domain.candidature.value_objects.statut_candidature import StatutCandidature
from domain.ddd.aggregate_root import AggregateRoot, factory, mutate
from domain.shared.value_objects.etapes_recrutement import (
    CategorieEtapeRecrutement,
    EtapeRecrutement,
)


@dataclass(kw_only=True)
class Candidature(AggregateRoot):
    _profil_candidat_id: UUID
    _offre_id: UUID
    _statut: StatutCandidature
    _etape_courante: EtapeRecrutement
    _documents: tuple[UUID, ...] | None = None
    _soumise_le: datetime | None = None
    _mise_a_jour_le: datetime | None = None

    @classmethod
    @factory(DossierCandidatureCree)
    def create(cls, event: DossierCandidatureCree) -> "Candidature":
        return cls(
            _profil_candidat_id=event.profil_candidat_id,
            _offre_id=event.offre_id,
            _statut=StatutCandidature.INITIAL,
            _etape_courante=event.etape_courante,
            _mise_a_jour_le=event.occurred_at,
        )

    @classmethod
    def build(
        cls,
        profil_candidat_id: UUID,
        offre_id: UUID,
        statut: StatutCandidature,
        etape_courante: EtapeRecrutement,
        documents: tuple[UUID, ...] | None = None,
        soumise_le: datetime | None = None,
        mise_a_jour_le: datetime | None = None,
    ) -> "Candidature":
        return cls(
            _profil_candidat_id=profil_candidat_id,
            _offre_id=offre_id,
            _statut=statut,
            _etape_courante=etape_courante,
            _documents=documents,
            _soumise_le=soumise_le,
            _mise_a_jour_le=mise_a_jour_le,
        )

    @property
    def profil_candidat_id(self) -> UUID:
        return self._profil_candidat_id

    @property
    def offre_id(self) -> UUID:
        return self._offre_id

    @property
    def statut(self) -> StatutCandidature:
        return self._statut

    @property
    def etape_courante(self) -> EtapeRecrutement | None:
        return self._etape_courante

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
    def deposer_documents(self, event: DocumentsDeposes) -> None:
        if len(event.documents) == 0:
            raise DossierCandidatureInvalide(
                ("Le dossier de candidature doit contenir au moins un document")
            )
        else:
            self._documents = event.documents
            self._mise_a_jour_le = event.occurred_at

    @mutate(CandidatureSoumise)
    def soumettre_candidature(self, event: CandidatureSoumise) -> None:
        if self._etape_courante.categorie == CategorieEtapeRecrutement.CLOTURE:
            raise CandidatureNePeutPasEtreSoumise("Le recrutement est clôturé")
        elif self._documents is None or len(self._documents) == 0:
            raise DossierCandidatureInvalide(
                (
                    "Le dossier de candidature doit contenir"
                    "au moins un document pour être soumis"
                )
            )
        else:
            self._statut = StatutCandidature.SOUMISE
            self._soumise_le = event.occurred_at
            self._mise_a_jour_le = event.occurred_at
