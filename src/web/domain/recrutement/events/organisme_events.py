from dataclasses import dataclass

from domain.ddd.domain_event import DomainEvent
from domain.shared.value_objects.etapes_recrutement import EtapesRecrutement


@dataclass(frozen=True)
class OrganismeParametresInitialises(DomainEvent):
    parametres: EtapesRecrutement


@dataclass(frozen=True)
class OrganismeParametresModifies(DomainEvent):
    parametres: EtapesRecrutement
