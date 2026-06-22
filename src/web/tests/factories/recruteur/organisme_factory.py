from uuid import uuid4

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


def make_etapes_recrutement():
    etapes: tuple[EtapeRecrutement, ...]
    etapes = (
        EtapeRecrutement.create(
            categorie=CategorieEtapeRecrutement.ENTREE, nom="Réception des candidatures"
        ),
        EtapeRecrutement.create(
            categorie=CategorieEtapeRecrutement.EN_COURS,
            nom="Présélection",
        ),
        EtapeRecrutement.create(
            categorie=CategorieEtapeRecrutement.EN_COURS,
            nom="Entretien",
        ),
        EtapeRecrutement.create(
            categorie=CategorieEtapeRecrutement.EN_COURS,
            nom="Proposition",
        ),
        EtapeRecrutement.create(
            categorie=CategorieEtapeRecrutement.EN_COURS,
            nom="Refus",
        ),
        EtapeRecrutement.create(
            categorie=CategorieEtapeRecrutement.TERMINALE,
            nom="Recrutement",
        ),
    )
    return etapes


class OrganismeRecruteurFactory:
    @staticmethod
    def create_entity(
        etapes: tuple[EtapeRecrutement, ...] | None = None,
    ) -> OrganismeRecruteur:
        if etapes is None:
            etapes = make_etapes_recrutement()
        return OrganismeRecruteur.build(entity_id=uuid4(), etapes=etapes)
