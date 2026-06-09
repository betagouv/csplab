from datetime import datetime
from typing import cast
from uuid import UUID

from faker import Faker

from domain.candidate.entities.candidature import Candidature
from domain.candidate.value_objects.statut_candidature import StatutCandidature

fake = Faker("fr_FR")


def make_documents() -> tuple[UUID, ...]:
    return (
        cast(UUID, fake.uuid4()),
        cast(UUID, fake.uuid4()),
    )


class CandidatureFactory:
    @staticmethod
    def build(
        profil_candidat_id: UUID | None = None,
        offre_id: UUID | None = None,
        statut: StatutCandidature | None = None,
        documents: tuple[UUID, ...] | None = None,
        soumise_le: datetime | None = None,
        mise_a_jour_le: datetime | None = None,
    ) -> "Candidature":
        profil_candidat_id = profil_candidat_id or cast(UUID, fake.uuid4())
        offre_id = offre_id or cast(UUID, fake.uuid4())
        statut = statut or StatutCandidature.INITIAL

        return Candidature.build(
            profil_candidat_id=profil_candidat_id,
            offre_id=offre_id,
            statut=statut,
            documents=documents,
            soumise_le=soumise_le,
            mise_a_jour_le=mise_a_jour_le,
        )
