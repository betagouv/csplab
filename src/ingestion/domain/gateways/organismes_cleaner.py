from typing import Iterable, Mapping, Optional, Protocol
from uuid import UUID

from referentiel.entities.organisme import Organisme

from domain.entities.raw_organisme import RawOrganisme


class IOrganismesCleaner(Protocol):
    def clean(self, raw_organisme: RawOrganisme) -> Optional[Organisme]: ...

    def dedupe_by_siret(
        self,
        organismes: Iterable[Organisme],
        depths: Optional[Mapping[UUID, int]] = None,
    ) -> list[Organisme]: ...

    def dila_siret_query(self, raw_organisme: RawOrganisme) -> Optional[str]: ...

    def dila_ancestor_ids(self, raw_organisme: RawOrganisme) -> list[UUID]: ...
