from dataclasses import dataclass, field

from domain.recruteur.errors.organisme_recruteur_errors import (
    ConfigurationEtapesInvalide,
)
from domain.recruteur.value_objects.categorie_etapes_recrutement import (
    CategorieEtapeRecrutement,
)
from domain.recruteur.value_objects.schema_etape_recrutement import (
    SchemaEtapeRecrutement,
)


def generate_default() -> tuple[SchemaEtapeRecrutement, ...]:
    return (
        SchemaEtapeRecrutement(
            categorie=CategorieEtapeRecrutement.ENTREE,
            nom="Réception des candidatures",
        ),
        SchemaEtapeRecrutement(
            categorie=CategorieEtapeRecrutement.EN_COURS,
            nom="Présélection",
        ),
        SchemaEtapeRecrutement(
            categorie=CategorieEtapeRecrutement.EN_COURS,
            nom="Entretien",
        ),
        SchemaEtapeRecrutement(
            categorie=CategorieEtapeRecrutement.EN_COURS,
            nom="Proposition",
        ),
        SchemaEtapeRecrutement(
            categorie=CategorieEtapeRecrutement.REFUS,
            nom="Refus",
        ),
        SchemaEtapeRecrutement(
            categorie=CategorieEtapeRecrutement.ACCEPTE,
            nom="Recrutement",
        ),
    )


@dataclass(frozen=True)
class ProcessusRecrutement:
    schemas: tuple[SchemaEtapeRecrutement, ...] = field(
        default_factory=generate_default
    )

    def __post_init__(self):
        self._validate()

    def _validate(self) -> None:
        categories = [e.categorie for e in self.schemas]
        # add that etapes as a whole is a set of schemas (schema = nom x categorie)
        if not categories or categories[0] != CategorieEtapeRecrutement.ENTREE:
            raise ConfigurationEtapesInvalide(
                "La première étape doit être de catégorie ENTREE"
            )
        elif categories[-1] != CategorieEtapeRecrutement.ACCEPTE:
            raise ConfigurationEtapesInvalide(
                "La dernière étape doit être de catégorie ACCEPTE"
            )
        elif categories[-2] != CategorieEtapeRecrutement.REFUS:
            raise ConfigurationEtapesInvalide(
                "L'avant-dernière étape doit être de catégorie REFUS"
            )

        milieu = categories[1:-2]
        if not milieu:
            raise ConfigurationEtapesInvalide(
                "Il doit y avoir au moins une étape EN_COURS"
            )
        if any(c != CategorieEtapeRecrutement.EN_COURS for c in milieu):
            raise ConfigurationEtapesInvalide(
                "Seules les étapes EN_COURS peuvent être placées entre ENTREE et REFUS"
            )

        # each schema (nom, categorie) must be unique
        couples = {(e.nom, e.categorie) for e in self.schemas}
        if len(couples) != len(self.schemas):
            raise ConfigurationEtapesInvalide(
                "Chaque couple (nom, catégorie) doit être unique"
            )
