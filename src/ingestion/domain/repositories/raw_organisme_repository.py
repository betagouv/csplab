from datetime import datetime
from typing import Protocol

from domain.entities.raw_organisme import RawOrganisme


class IRawOrganismeRepository(Protocol):
    async def upsert_batch(self, organismes: list[RawOrganisme]) -> None: ...
    async def delete_missing(
        self, referentiel: str, loaded_before: datetime
    ) -> int: ...
