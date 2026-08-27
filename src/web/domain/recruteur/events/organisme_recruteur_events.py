from dataclasses import dataclass

from ddd.domain_event import DomainEvent

from domain.recruteur.value_objects.etape_data import (
    EtapeData,
)


@dataclass(frozen=True)
class OrganismeEtapesInitialises(DomainEvent): ...


@dataclass(frozen=True)
class OrganismeEtapesMisesAJour(DomainEvent):
    etapes_data: tuple[EtapeData, ...]
