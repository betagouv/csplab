from typing import Optional, Protocol

from domain.entities.organisme import Organisme
from domain.entities.raw_organisme import RawOrganisme


class IOrganismesCleaner(Protocol):
    def clean(self, raw_organisme: RawOrganisme) -> Optional[Organisme]: ...
