from dataclasses import dataclass
from uuid import UUID

from ddd.entity import Entity

from domain.recruteur.value_objects.categorie_etapes_recrutement import (
    CategorieEtapeRecrutement,
)


@dataclass(kw_only=True)
class EtapeRecrutement(Entity):
    _categorie: CategorieEtapeRecrutement  # catégorie connue du système
    _nom: str  # label libre, personnalisé par l'organisme

    @classmethod
    def create(
        cls,
        categorie: CategorieEtapeRecrutement,
        nom: str,
    ) -> "EtapeRecrutement":
        return cls(_categorie=categorie, _nom=nom)

    @classmethod
    def build(
        cls,
        entity_id: UUID,
        categorie: CategorieEtapeRecrutement,
        nom: str,
    ) -> "EtapeRecrutement":
        return cls(entity_id=entity_id, _categorie=categorie, _nom=nom)

    @property
    def categorie(self) -> CategorieEtapeRecrutement:
        return self._categorie

    @property
    def nom(self) -> str:
        return self._nom
