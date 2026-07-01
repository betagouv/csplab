from uuid import uuid4

from application.recruteur.usecases.update_organisme_steps import EtapeData
from domain.recruteur.entities.etape_recrutement import EtapeRecrutement
from domain.recruteur.entities.organisme_recruteur import OrganismeRecruteur
from domain.recruteur.value_objects.categorie_etapes_recrutement import (
    CategorieEtapeRecrutement,
)


class EtapeRecrutementFactory:
    @staticmethod
    def create_entity(
        categorie: CategorieEtapeRecrutement = CategorieEtapeRecrutement.EN_COURS,
        nom: str = "Entretien",
    ) -> EtapeRecrutement:
        return EtapeRecrutement.create(categorie=categorie, nom=nom)

    @staticmethod
    def create_entities(
        en_cours: tuple[EtapeRecrutement, ...] | None = None,
    ) -> tuple[EtapeRecrutement, ...]:
        etapes_en_cours = en_cours or (
            EtapeRecrutement.create(
                categorie=CategorieEtapeRecrutement.EN_COURS, nom="Présélection"
            ),
            EtapeRecrutement.create(
                categorie=CategorieEtapeRecrutement.EN_COURS, nom="Entretien"
            ),
            EtapeRecrutement.create(
                categorie=CategorieEtapeRecrutement.EN_COURS, nom="Proposition"
            ),
        )
        return (
            EtapeRecrutement.create(
                categorie=CategorieEtapeRecrutement.ENTREE,
                nom="Réception des candidatures",
            ),
            *etapes_en_cours,
            EtapeRecrutement.create(
                categorie=CategorieEtapeRecrutement.REFUS, nom="Refus"
            ),
            EtapeRecrutement.create(
                categorie=CategorieEtapeRecrutement.ACCEPTE, nom="Recrutement"
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


class OrganismeRecruteurFactory:
    @staticmethod
    def create_entity(
        etapes: tuple[EtapeRecrutement, ...] | None = None,
    ) -> OrganismeRecruteur:
        return OrganismeRecruteur.build(entity_id=uuid4(), etapes=etapes)
