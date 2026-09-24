from datetime import datetime
from uuid import UUID, uuid4

from faker import Faker

from domain.candidate.entities.candidature import Candidature
from domain.candidate.value_objects.statut_candidature import StatutCandidature

fake = Faker("fr_FR")


def make_documents() -> tuple[UUID, ...]:
    return (
        uuid4(),
        uuid4(),
    )


class CandidatureFactory:
    @staticmethod
    def create_entity(
        entity_id: UUID | None = None,
        candidat_id: UUID | None = None,
        offre_id: UUID | None = None,
        statut: StatutCandidature | None = None,
        documents: tuple[UUID, ...] | None = None,
        soumise_le: datetime | None = None,
        mise_a_jour_le: datetime | None = None,
    ) -> "Candidature":
        entity_id = uuid4()
        candidat_id = candidat_id or uuid4()
        offre_id = offre_id or uuid4()
        statut = statut or StatutCandidature.INITIAL
        return Candidature.build(
            entity_id=entity_id,
            candidat_id=candidat_id,
            offre_id=offre_id,
            statut=statut,
            documents=documents,
            soumise_le=soumise_le,
            mise_a_jour_le=mise_a_jour_le,
        )
