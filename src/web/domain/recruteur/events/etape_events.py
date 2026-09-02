from dataclasses import dataclass

from ddd.domain_event import DomainEvent

from domain.recruteur.value_objects.categorie_etapes_recrutement import (
    CategorieEtapeRecrutement,
)


@dataclass(frozen=True)
class EtapeAjoutee(DomainEvent):
    nom: str
    categorie: CategorieEtapeRecrutement


@dataclass(frozen=True)
class EtapeRenommee(DomainEvent):
    nom: str


@dataclass(frozen=True)
class EtapeReordonnee(DomainEvent):
    nouveau_rang: int


@dataclass(frozen=True)
class EtapeSupprimee(DomainEvent): ...
