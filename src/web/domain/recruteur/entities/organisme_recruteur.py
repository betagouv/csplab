from dataclasses import dataclass
from uuid import UUID

from ddd.aggregate_root import AggregateRoot, mutate

from domain.recruteur.entities.etape_recrutement import EtapeRecrutement
from domain.recruteur.events.organisme_events import OrganismeEtapesInitialises
from domain.recruteur.value_objects.categorie_etapes_recrutement import (
    CategorieEtapeRecrutement,
)


@dataclass(kw_only=True)
class OrganismeRecruteur(AggregateRoot):
    _etapes: tuple[EtapeRecrutement, ...] | None
    # _formulaire_candidature

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
                categorie=CategorieEtapeRecrutement.EN_COURS,
                nom="Refus",
            ),
            EtapeRecrutement.create(
                categorie=CategorieEtapeRecrutement.TERMINALE,
                nom="Recrutement",
            ),
        )
