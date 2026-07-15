from datetime import datetime
from typing import cast
from uuid import UUID

from faker import Faker

from domain.candidate.entities.candidature import Candidature
from domain.candidate.value_objects.statut_candidature import StatutCandidature
from domain.recruteur.value_objects.categorie_etapes_recrutement import (
    CategorieEtapeRecrutement,
)
from infrastructure.django_apps.candidate.models.candidature import CandidatureModel
from infrastructure.django_apps.recruteur.models.etape import EtapeModel
from infrastructure.django_apps.recruteur.models.recrutement import RecrutementModel
from infrastructure.mappers.candidature_mapper import CandidatureMapper
from tests.factories.identite.candidat_factory import CandidatFactory
from tests.factories.recruteur.recrutement_factory import RecrutementFactory
from tests.factories.referentiel.offer_factory import OfferFactory

fake = Faker("fr_FR")


def make_documents() -> tuple[UUID, ...]:
    return (
        cast(UUID, fake.uuid4()),
        cast(UUID, fake.uuid4()),
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
    def create_model(
        candidat_id: UUID | None = None,
        offre_id: UUID | None = None,
        statut: StatutCandidature | None = None,
        documents: tuple[UUID, ...] | None = None,
        etape: EtapeModel | None = None,
    ) -> CandidatureModel:
        if candidat_id is None:
            candidat_id = UUID(CandidatFactory.create_model().utilisateur_id)
        if offre_id is None:
            offre_id = OfferFactory.create_model().id

        candidature = CandidatureFactory.create_entity(
            candidat_id=candidat_id,
            offre_id=offre_id,
            statut=statut,
            documents=documents,
        )

        if etape is None:
            # Réutiliser un recrutement existant ou en créer un
            recrutement = RecrutementModel.objects.filter(  # type: ignore[attr-defined]
                offre_id=offre_id
            ).first()
            if recrutement is None:
                recrutement = RecrutementFactory.create_model(offre_id=offre_id)

            first_etape = EtapeModel.objects.filter(  # type: ignore[attr-defined]
                recrutement_id=offre_id,
                categorie=CategorieEtapeRecrutement.ENTREE.value,
            ).first()
            etape_id = (
                first_etape.id if first_etape else UUID(recrutement.ordre_etapes[0])
            )  # type: ignore[attr-defined]
        else:
            etape_id = etape.id

        model = CandidatureMapper().from_domain(candidature, etape_id=etape_id)
        model.save()
        return model
