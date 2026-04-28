from typing import Dict, Optional
from uuid import UUID

from domain.entities.cv_metadata import CVMetadata
from domain.repositories.cv_metadata_repository_interface import ICVMetadataRepository


class InMemoryCVMetadataRepository(ICVMetadataRepository):
    def __init__(self):
        self._storage: Dict[UUID, CVMetadata] = {}

    def save(self, cv_metadata: CVMetadata) -> CVMetadata:
        self._storage[cv_metadata.id] = cv_metadata
        return cv_metadata

    def get_by_id(self, cv_id: UUID) -> Optional[CVMetadata]:
        return self._storage.get(cv_id)

    def clear(self):
        self._storage.clear()

    def count(self) -> int:
        return len(self._storage)
