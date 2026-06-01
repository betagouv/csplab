from dataclasses import dataclass

from domain.ddd.aggregate_root import AggregateRoot, mutate
from domain.recrutement.events.organisme_events import (
    OrganismeParametresInitialises,
    OrganismeParametresModifies,
)
from domain.shared.value_objects.etapes_recrutement import EtapesRecrutement


@dataclass(kw_only=True)
class Organisme(AggregateRoot):
    _parametres: EtapesRecrutement | None  # for now, only etapes_recrutement
    # but we can add more parameters later

    @classmethod
    def build(
        cls,
        parametres: EtapesRecrutement | None = None,
    ) -> "Organisme":
        return cls(
            _parametres=parametres,
        )

    @property
    def parametres(self) -> EtapesRecrutement | None:
        return self._parametres

    @mutate(OrganismeParametresInitialises)
    def initialiser_parametres(self, event: OrganismeParametresInitialises) -> None:
        self._parametres = event.parametres

    @mutate(OrganismeParametresModifies)
    def modifier_parametres(self, event: OrganismeParametresModifies) -> None:
        self._parametres = event.parametres
