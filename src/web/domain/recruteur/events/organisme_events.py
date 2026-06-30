from dataclasses import dataclass

from ddd.domain_event import DomainEvent

from domain.recruteur.entities.etape_recrutement import EtapeRecrutement


@dataclass(frozen=True)
class OrganismeEtapesInitialises(DomainEvent): ...


@dataclass(frozen=True)
class OrganismeEtapesMisesAJour(DomainEvent):
    etapes: tuple[EtapeRecrutement, ...]
