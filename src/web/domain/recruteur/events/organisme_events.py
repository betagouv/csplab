from dataclasses import dataclass

from ddd.domain_event import DomainEvent


@dataclass(frozen=True)
class OrganismeEtapesInitialises(DomainEvent): ...
