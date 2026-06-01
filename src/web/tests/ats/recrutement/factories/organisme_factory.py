from polyfactory.factories.dataclass_factory import DataclassFactory

from domain.recrutement.entities.organisme import Organisme
from domain.shared.value_objects.etapes_recrutement import (
    CategorieEtapeRecrutement,
    EtapeRecrutement,
    EtapesRecrutement,
)


class EtapeRecrutementFactory(DataclassFactory):
    __model__ = EtapeRecrutement


def make_etape_recrutement(
    identifiant: str = "reception",
    categorie: CategorieEtapeRecrutement = CategorieEtapeRecrutement.RECEPTION,
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


class OrganismeFactory:
    @staticmethod
    def build(
        parametres: EtapesRecrutement | None = None,
    ) -> "Organisme":
        return Organisme.build(
            parametres=parametres or make_etapes_recrutement(),
        )
