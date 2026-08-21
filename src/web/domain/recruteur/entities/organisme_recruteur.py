from dataclasses import dataclass
from uuid import UUID

from ddd.aggregate_root import AggregateRoot, mutate

from domain.recruteur.entities.etape_recrutement import EtapeRecrutement
from domain.recruteur.events.organisme_events import (
    OrganismeEtapesInitialises,
    OrganismeEtapesMisesAJour,
)
from domain.recruteur.value_objects.processus_recrutement import ProcessusRecrutement


@dataclass(kw_only=True)
class OrganismeRecruteur(AggregateRoot):
    _etapes: tuple[EtapeRecrutement, ...] | None
    # _formulaire_candidature

    @classmethod
    def build(
        cls,
        entity_id: UUID,
        etapes: tuple[EtapeRecrutement, ...] | None,
    ) -> "OrganismeRecruteur":
        return cls(entity_id=entity_id, _etapes=etapes)

    @property
    def etapes(self) -> tuple[EtapeRecrutement, ...] | None:
        return self._etapes

    @mutate(OrganismeEtapesInitialises)
    def initialiser_etapes(self) -> None:
        # generate etapes from default recruit process
        etapes = tuple(
            EtapeRecrutement.create(nom=schema.nom, categorie=schema.categorie)
            for schema in ProcessusRecrutement().schemas
        )
        # mutate
        self._etapes = etapes

    @mutate(OrganismeEtapesMisesAJour)
    def mettre_a_jour_etapes(self, etapes: tuple[EtapeRecrutement, ...]) -> None:
        # check business rules
        ProcessusRecrutement(schemas=tuple(etape.schema for etape in etapes))
        # mutate
        self._etapes = etapes
