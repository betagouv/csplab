"""Use case for initializing CV metadata with pending status."""

from datetime import datetime
from uuid import uuid4

from domain.entities.cv_metadata import CVMetadata
from domain.repositories.cv_metadata_repository_interface import ICVMetadataRepository
from domain.value_objects.cv_processing_status import CVStatus


class InitializeCVMetadataUsecase:
    """Usecase for initializing CV metadata with filename and pending status."""

    def __init__(self, cv_metadata_repository: ICVMetadataRepository):
        """Initialize the use case with required dependencies.

        Args:
            cv_metadata_repository: Repository for CV metadata persistence
        """
        self._cv_metadata_repository = cv_metadata_repository

    def execute(self, filename: str) -> str:
        """Execute the initialization of CV metadata.

        Args:
            filename: Name of the CV file

        Returns:
            CV ID as string
        """
        now = datetime.now()
        cv_metadata = CVMetadata(
            id=uuid4(),
            filename=filename,
            status=CVStatus.PENDING,
            created_at=now,
            updated_at=now,
        )

        saved_cv = self._cv_metadata_repository.save(cv_metadata)
        return str(saved_cv.id)
