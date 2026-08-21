from dataclasses import dataclass

from domain.recruteur.value_objects.categorie_etapes_recrutement import (
    CategorieEtapeRecrutement,
)


@dataclass(frozen=True)
class SchemaEtapeRecrutement:
    nom: str
    categorie: CategorieEtapeRecrutement
