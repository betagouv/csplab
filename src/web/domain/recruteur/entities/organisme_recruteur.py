from dataclasses import dataclass
from uuid import UUID

from ddd.aggregate_root import AggregateRoot, mutate

from domain.recruteur.entities.etape_recrutement import EtapeRecrutement
from domain.recruteur.errors.erreur_recrutement import ConfigurationEtapesInvalide
from domain.recruteur.events.organisme_events import (
    OrganismeEtapesInitialises,
    OrganismeEtapesMisesAJour,
)
from domain.recruteur.value_objects.categorie_etapes_recrutement import (
    CategorieEtapeRecrutement,
)


@dataclass(kw_only=True)
class OrganismeRecruteur(AggregateRoot):
    _etapes: tuple[EtapeRecrutement, ...] | None
    # _formulaire_candidature
    # TODO : add candidature_id

    @classmethod
    def build(
        cls,
        entity_id: UUID,
        etapes: tuple[EtapeRecrutement, ...] | None = None,
    ) -> "OrganismeRecruteur":
        return cls(entity_id=entity_id, _etapes=etapes)

    @property
    def etapes(self) -> tuple[EtapeRecrutement, ...] | None:
        return self._etapes

    @mutate(OrganismeEtapesInitialises)
    def initialiser_etapes(self) -> None:
        self._etapes = (
            EtapeRecrutement.create(
                categorie=CategorieEtapeRecrutement.ENTREE,
                nom="Réception des candidatures",
            ),
            EtapeRecrutement.create(
                categorie=CategorieEtapeRecrutement.EN_COURS,
                nom="Présélection",
            ),
            EtapeRecrutement.create(
                categorie=CategorieEtapeRecrutement.EN_COURS,
                nom="Entretien",
            ),
            EtapeRecrutement.create(
                categorie=CategorieEtapeRecrutement.EN_COURS,
                nom="Proposition",
            ),
            EtapeRecrutement.create(
                categorie=CategorieEtapeRecrutement.REFUS,
                nom="Refus",
            ),
            EtapeRecrutement.create(
                categorie=CategorieEtapeRecrutement.ACCEPTE,
                nom="Recrutement",
            ),
        )

    @mutate(OrganismeEtapesMisesAJour)
    def mettre_a_jour_etapes(self, *, etapes: tuple[EtapeRecrutement, ...]) -> None:
        self._valider_configuration(etapes)
        self._etapes = etapes

    def _valider_configuration(self, etapes: tuple[EtapeRecrutement, ...]) -> None:
        categories = [e.categorie for e in etapes]

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
