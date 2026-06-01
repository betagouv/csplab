from datetime import datetime
from uuid import UUID

from domain.candidature.entities.candidature import Candidature
from domain.candidature.value_objects.statut_candidature import StatutCandidature
from domain.shared.value_objects.etapes_recrutement import (
    EtapeRecrutement,
)
from tests.ats.shared.factories.shared_factories import make_etapes_recrutement


def make_documents() -> tuple[UUID, ...]:
    return (
        UUID("00000000-0000-0000-0000-000000000003"),
        UUID("00000000-0000-0000-0000-000000000004"),
    )


class CandidatureFactory:
    @staticmethod
    def build(
        profil_candidat_id: UUID | None = None,
        offre_id: UUID | None = None,
        statut: StatutCandidature | None = None,
        etape_courante: EtapeRecrutement | None = None,
        documents: tuple[UUID, ...] | None = None,
        soumise_le: datetime | None = None,
        mise_a_jour_le: datetime | None = None,
    ) -> "Candidature":
        etape_courante = etape_courante or make_etapes_recrutement().ordonnees()[0]
        profil_candidat_id = profil_candidat_id or UUID(
            "00000000-0000-0000-0000-000000000001"
        )
        offre_id = offre_id or UUID("00000000-0000-0000-0000-000000000002")
        statut = statut or StatutCandidature.INITIAL

        return Candidature.build(
            profil_candidat_id=profil_candidat_id,
            offre_id=offre_id,
            statut=statut,
            etape_courante=etape_courante,
            documents=documents,
            soumise_le=soumise_le,
            mise_a_jour_le=mise_a_jour_le,
        )
