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


class OrganismeRecruteurFactory:
    @staticmethod
    def create_entity(
        etapes: tuple[EtapeRecrutement, ...] | None = None,
    ) -> OrganismeRecruteur:
        return OrganismeRecruteur.build(entity_id=uuid4(), etapes=etapes)
