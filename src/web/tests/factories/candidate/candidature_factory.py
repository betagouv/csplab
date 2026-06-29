from datetime import datetime
from typing import cast
from uuid import UUID

from faker import Faker

from domain.candidate.entities.candidature import Candidature
from domain.candidate.value_objects.statut_candidature import StatutCandidature
from infrastructure.django_apps.candidate.models.candidature import CandidatureModel
from tests.factories.identite.candidat_factory import CandidatFactory
from tests.factories.referentiel.offer_factory import OfferFactory

fake = Faker("fr_FR")


def make_documents() -> tuple[UUID, ...]:
    return (
        cast(UUID, fake.uuid4()),
        cast(UUID, fake.uuid4()),
    )


class CandidatureFactory:
    @staticmethod
    def build(
        entity_id: UUID | None = None,
        candidat_id: UUID | None = None,
        offre_id: UUID | None = None,
        statut: StatutCandidature | None = None,
        documents: tuple[UUID, ...] | None = None,
        soumise_le: datetime | None = None,
        mise_a_jour_le: datetime | None = None,
    ) -> "Candidature":
        entity_id = cast(UUID, fake.uuid4())
        candidat_id = candidat_id or cast(UUID, fake.uuid4())
        offre_id = offre_id or cast(UUID, fake.uuid4())
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

    @staticmethod
    def build_model(
        candidat_id: UUID | None = None,
        offre_id: UUID | None = None,
        statut: StatutCandidature | None = None,
        documents: tuple[UUID, ...] | None = None,
    ) -> CandidatureModel:
        if candidat_id is None:
            candidat_id = UUID(CandidatFactory.create_model().utilisateur_id)
        if offre_id is None:
            offre_id = OfferFactory.create_model().id

        candidature = CandidatureFactory.build(
            candidat_id=candidat_id,
            offre_id=offre_id,
            statut=statut,
            documents=documents,
        )
        model = CandidatureModel.from_entity(candidature)
        model.save()
        return model
