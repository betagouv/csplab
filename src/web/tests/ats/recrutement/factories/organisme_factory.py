import random

from polyfactory.factories.dataclass_factory import DataclassFactory

from domain.recrutement.entities.organisme import Organisme
from domain.recrutement.value_objects.etapes_recrutement import (
    CategorieEtapeRecrutement,
    EtapeRecrutement,
    EtapesRecrutement,
)


class EtapeRecrutementFactory(DataclassFactory):
    __model__ = EtapeRecrutement

    @classmethod
    def rang(cls) -> int:
        return cls.__random__.randint(1, 999)


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
    n: int = 6,
) -> EtapesRecrutement:
    if etapes is None:
        rangs = random.sample(range(1, n * 10 + 1), n)
        etapes = tuple(
            EtapeRecrutementFactory.build(
                rang=rangs[i],
                identifiant=f"etape_{i}",
            )
            for i in range(n)
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
