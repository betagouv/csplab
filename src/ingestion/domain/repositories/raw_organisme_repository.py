from datetime import datetime
from typing import Protocol
from uuid import UUID

from domain.entities.raw_organisme import RawOrganisme


class IRawOrganismeRepository(Protocol):
    async def upsert_batch(self, organismes: list[RawOrganisme]) -> None: ...
    async def delete_missing(
        self, referentiel: str, loaded_before: datetime
    ) -> int: ...
    async def find_uncleaned(
        self, referentiel: str, limit: int
    ) -> list[RawOrganisme]: ...
    async def mark_as_cleaned_batch(
        self, ids: list[UUID], cleaned_at: datetime
    ) -> None: ...
