from typing import Optional, Protocol
from uuid import UUID

from domain.entities.cv_metadata import CVMetadata


class ICVMetadataRepository(Protocol):
    def save(self, cv_metadata: CVMetadata) -> CVMetadata: ...

    def get_by_id(self, cv_id: UUID) -> Optional[CVMetadata]: ...
