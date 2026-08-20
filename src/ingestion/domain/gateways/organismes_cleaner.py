from typing import Optional, Protocol

from referentiel.entities.organisme import Organisme

from domain.entities.raw_organisme import RawOrganisme


class IOrganismesCleaner(Protocol):
    def clean(self, raw_organisme: RawOrganisme) -> Optional[Organisme]: ...
