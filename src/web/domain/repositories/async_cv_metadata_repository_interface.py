from typing import Optional, Protocol
from uuid import UUID

from domain.entities.cv_metadata import CVMetadata


class IAsyncCVMetadataRepository(Protocol):
    async def save(self, cv_metadata: CVMetadata) -> CVMetadata: ...

    async def get_by_id(self, cv_id: UUID) -> Optional[CVMetadata]: ...

    def count(self) -> int: ...
