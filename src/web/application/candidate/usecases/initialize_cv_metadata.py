from datetime import datetime, timezone
from uuid import uuid4

from domain.candidate.entities.cv_metadata import CVMetadata
from domain.candidate.repositories.cv_metadata_repository_interface import (
    ICVMetadataRepository,
)
from domain.candidate.value_objects.cv_processing_status import CVStatus


class InitializeCVMetadataUsecase:
    def __init__(self, cv_metadata_repository: ICVMetadataRepository):
        self.cv_metadata_repository = cv_metadata_repository

    def execute(self, filename: str) -> str:

        now = datetime.now(timezone.utc)
        cv_metadata = CVMetadata(
            entity_id=uuid4(),
            filename=filename,
            status=CVStatus.PENDING,
            created_at=now,
            updated_at=now,
        )

        saved_cv = self.cv_metadata_repository.save(cv_metadata)
        return str(saved_cv.entity_id)
