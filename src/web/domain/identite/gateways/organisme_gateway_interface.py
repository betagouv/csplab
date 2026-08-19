from dataclasses import dataclass
from datetime import date
from typing import Iterator, Protocol

from domain.identite.entities.organisme import Organisme


@dataclass(frozen=True)
class OrganismeImportResource:
    url: str
    millesime: date


class IOrganismeGateway(Protocol):
    def find_latest_resource(self) -> OrganismeImportResource: ...

    def stream_organismes(
        self, resource: OrganismeImportResource
    ) -> Iterator[Organisme]: ...
