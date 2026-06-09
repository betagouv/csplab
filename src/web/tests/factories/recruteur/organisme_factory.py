from polyfactory.factories.dataclass_factory import DataclassFactory

from domain.recruteur.entities.organisme import Organisme
from domain.recruteur.value_objects.etapes_recrutement import (
    CategorieEtapeRecrutement,
    EtapeRecrutement,
    EtapesRecrutement,
)


class EtapeRecrutementFactory(DataclassFactory):
    __model__ = EtapeRecrutement


def make_etape_recrutement(
    identifiant: str = "entree",
    categorie: CategorieEtapeRecrutement = CategorieEtapeRecrutement.INITIALE,
    nom: str = "Réception des candidatures",
) -> EtapeRecrutement:
    return EtapeRecrutement(identifiant=identifiant, categorie=categorie, nom=nom)


def make_etapes_recrutement(
    etapes: tuple[EtapeRecrutement, ...] | None = None,
    n: int = 6,
) -> EtapesRecrutement:
    if etapes is None:
        etapes = tuple(
            EtapeRecrutementFactory.build(identifiant=f"etape_{i}") for i in range(n)
        )
    return EtapesRecrutement(etapes=etapes)


class OrganismeFactory(DataclassFactory):
    __model__ = Organisme

    @classmethod
    def build(
        cls,
        parametres: EtapesRecrutement | None = None,
    ):
        if parametres is None:
            parametres = make_etapes_recrutement()
        return super().build(_parametres=parametres)
