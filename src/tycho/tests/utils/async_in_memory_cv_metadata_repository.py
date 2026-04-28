from typing import Dict, Optional
from uuid import UUID

from domain.entities.cv_metadata import CVMetadata
from domain.repositories.async_cv_metadata_repository_interface import (
    IAsyncCVMetadataRepository,
)


class AsyncInMemoryCVMetadataRepository(IAsyncCVMetadataRepository):
    def __init__(self):
        self._storage: Dict[UUID, CVMetadata] = {}

    async def save(self, cv_metadata: CVMetadata) -> CVMetadata:
        self._storage[cv_metadata.id] = cv_metadata
        return cv_metadata

    async def get_by_id(self, cv_id: UUID) -> Optional[CVMetadata]:
        return self._storage.get(cv_id)

    def count(self) -> int:
        return len(self._storage)

    def clear(self):
        self._storage.clear()
