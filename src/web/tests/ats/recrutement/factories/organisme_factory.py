from domain.recrutement.entities.organisme import Organisme
from domain.recrutement.value_objects.etapes_recrutement import (
    CategorieEtapeRecrutement,
    EtapeRecrutement,
    EtapesRecrutement,
)


def make_etape_recrutement(
    rang: int = 1,
    identifiant: str = "reception",
    categorie: CategorieEtapeRecrutement = CategorieEtapeRecrutement.RECEPTION,
    nom: str = "Réception des candidatures",
) -> EtapeRecrutement:
    return EtapeRecrutement(
        rang=rang, identifiant=identifiant, categorie=categorie, nom=nom
    )


def make_etapes_recrutement(
    etapes: tuple[EtapeRecrutement, ...] | None = None,
) -> EtapesRecrutement:
    if etapes is None:
        etapes = (
            make_etape_recrutement(
                rang=3,
                identifiant="entretien_telephone",
                categorie=CategorieEtapeRecrutement.EVALUATION,
                nom="Entretien par téléphone",
            ),
            make_etape_recrutement(
                rang=1,
                identifiant="publication",
                categorie=CategorieEtapeRecrutement.PUBLICATION,
                nom="Publication",
            ),
            make_etape_recrutement(
                rang=2,
                identifiant="reception",
                categorie=CategorieEtapeRecrutement.RECEPTION,
                nom="Réception",
            ),
            make_etape_recrutement(
                rang=6,
                identifiant="cloture",
                categorie=CategorieEtapeRecrutement.CLOTURE,
                nom="Clôture de l'offre",
            ),
            make_etape_recrutement(
                rang=4,
                identifiant="entretien_en_personne",
                categorie=CategorieEtapeRecrutement.RECEPTION,
                nom="Entretien en personne",
            ),
            make_etape_recrutement(
                rang=5,
                identifiant="selection",
                categorie=CategorieEtapeRecrutement.SELECTION,
                nom="Sélection finale",
            ),
        )
    return EtapesRecrutement(etapes=etapes)


class OrganismeFactory:
    @staticmethod
    def build(
        parametres: EtapesRecrutement | None = None,
    ) -> "Organisme":
        return Organisme.build(
            parametres=parametres or make_etapes_recrutement(),
        )
