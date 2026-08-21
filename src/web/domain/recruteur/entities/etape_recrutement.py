from dataclasses import dataclass
from uuid import UUID

from ddd.aggregate_root import AggregateRoot, factory, mutate

from domain.recruteur.events.etapes_events import (
    EtapeAjoutee,
    EtapeRenommee,
    EtapeReordonnee,
    EtapeSupprimee,
)
from domain.recruteur.value_objects.categorie_etapes_recrutement import (
    CategorieEtapeRecrutement,
)
from domain.recruteur.value_objects.schema_etape_recrutement import (
    SchemaEtapeRecrutement,
)


@dataclass(kw_only=True)
class EtapeRecrutement(AggregateRoot):
    _categorie: CategorieEtapeRecrutement  # catégorie connue du système
    _nom: str  # label libre, personnalisé par l'organisme

    @classmethod
    @factory(EtapeAjoutee)
    def create(
        cls, categorie: CategorieEtapeRecrutement, nom: str
    ) -> "EtapeRecrutement":
        return cls(_categorie=categorie, _nom=nom)

    @classmethod
    def build(
        cls, entity_id: UUID, categorie: CategorieEtapeRecrutement, nom: str
    ) -> "EtapeRecrutement":
        return cls(
            entity_id=entity_id,
            _categorie=categorie,
            _nom=nom,
        )

    @mutate(EtapeRenommee)
    def renommer(self, nom: str) -> None:
        self._nom = nom

    @mutate(EtapeReordonnee)
    def changer_rang(self, rang: int) -> None: ...

    @mutate(EtapeSupprimee)
    def delete(self) -> None: ...

    @property
    def nom(self) -> str:
        return self._nom

    @property
    def categorie(self) -> CategorieEtapeRecrutement:
        return self._categorie

    @property
    def schema(self) -> SchemaEtapeRecrutement:
        return SchemaEtapeRecrutement(nom=self._nom, categorie=self._categorie)
