from dataclasses import dataclass
from typing import List
from uuid import UUID

from ddd.aggregate_root import AggregateRoot, factory, mutate

from domain.recruteur.errors.recrutement_errors import SupressionEtapeImpossible
from domain.recruteur.events.etapes_events import (
    EtapeAjoutee,
    EtapeSupprimee,
)
from domain.recruteur.value_objects.categorie_etapes_recrutement import (
    CategorieEtapeRecrutement,
)


@dataclass(kw_only=True)
class EtapeRecrutement(AggregateRoot):
    _categorie: CategorieEtapeRecrutement  # catégorie connue du système
    _nom: str  # label libre, personnalisé par l'organisme
    _candidatures: List[UUID] | None

    @classmethod
    @factory(EtapeAjoutee)
    def create(
        cls, categorie: CategorieEtapeRecrutement, nom: str
    ) -> "EtapeRecrutement":
        return cls(_categorie=categorie, _nom=nom, _candidatures=None)

    @classmethod
    def build(
        cls,
        entity_id: UUID,
        categorie: CategorieEtapeRecrutement,
        nom: str,
        candidatures: List[UUID] | None = None,
    ) -> "EtapeRecrutement":
        return cls(
            entity_id=entity_id,
            _categorie=categorie,
            _nom=nom,
            _candidatures=candidatures,
        )

    @mutate(EtapeSupprimee)
    def delete(self) -> None:
        if self._candidatures is not None:
            raise SupressionEtapeImpossible(
                etape_id=self.entity_id, nombre_candidatures=len(self._candidatures)
            )

    @property
    def nom(self) -> str:
        return self._nom

    @property
    def categorie(self) -> CategorieEtapeRecrutement:
        return self._categorie

    @property
    def candidatures(self) -> List[UUID] | None:
        return self._candidatures
