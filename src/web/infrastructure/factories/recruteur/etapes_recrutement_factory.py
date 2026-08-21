from typing import List
from uuid import UUID, uuid4

from application.recruteur.usecases.update_organisme_steps import EtapeData
from domain.recruteur.entities.etape_recrutement import EtapeRecrutement
from domain.recruteur.value_objects.categorie_etapes_recrutement import (
    CategorieEtapeRecrutement,
)


class EtapeRecrutementFactory:
    @staticmethod
    def create_entity(
        categorie: CategorieEtapeRecrutement = CategorieEtapeRecrutement.EN_COURS,
        nom: str = "Entretien",
        candidatures: List[UUID] | None = None,
    ) -> EtapeRecrutement:
        return EtapeRecrutement.build(
            entity_id=uuid4(),
            categorie=categorie,
            nom=nom,
            candidatures=candidatures,
        )

    @staticmethod
    def create_entity_batch(
        en_cours: tuple[EtapeRecrutement, ...] | None = None,
        candidatures: List[UUID] | None = None,
    ) -> tuple[EtapeRecrutement, ...]:
        etapes_en_cours = en_cours or (
            EtapeRecrutement.build(
                entity_id=uuid4(),
                categorie=CategorieEtapeRecrutement.EN_COURS,
                nom="Présélection",
            ),
            EtapeRecrutement.build(
                entity_id=uuid4(),
                categorie=CategorieEtapeRecrutement.EN_COURS,
                nom="Entretien",
                candidatures=candidatures,
            ),
            EtapeRecrutement.build(
                entity_id=uuid4(),
                categorie=CategorieEtapeRecrutement.EN_COURS,
                nom="Proposition",
            ),
        )
        return (
            EtapeRecrutement.build(
                entity_id=uuid4(),
                categorie=CategorieEtapeRecrutement.ENTREE,
                nom="Réception des candidatures",
            ),
            *etapes_en_cours,
            EtapeRecrutement.build(
                entity_id=uuid4(),
                categorie=CategorieEtapeRecrutement.REFUS,
                nom="Refus",
            ),
            EtapeRecrutement.build(
                entity_id=uuid4(),
                categorie=CategorieEtapeRecrutement.ACCEPTE,
                nom="Recrutement",
            ),
        )

    @staticmethod
    def to_etape_data_list(
        etapes: tuple[EtapeRecrutement, ...],
        en_cours: list[EtapeData] | None = None,
    ) -> list[EtapeData]:
        etapes_en_cours = en_cours or [
            EtapeData(
                etape_uuid=None,
                nom="Entretien RH",
                categorie=CategorieEtapeRecrutement.EN_COURS,
            ),
        ]
        return [
            EtapeData(
                etape_uuid=etapes[0].entity_id,
                nom=etapes[0].nom,
                categorie=etapes[0].categorie,
            ),
            *etapes_en_cours,
            EtapeData(
                etape_uuid=etapes[-2].entity_id,
                nom=etapes[-2].nom,
                categorie=etapes[-2].categorie,
            ),
            EtapeData(
                etape_uuid=etapes[-1].entity_id,
                nom=etapes[-1].nom,
                categorie=etapes[-1].categorie,
            ),
        ]
