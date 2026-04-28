"""Polyfactory for CVMetadata entity."""

from datetime import UTC, datetime, timezone
from uuid import UUID, uuid4

from polyfactory.factories import DataclassFactory

from domain.entities.cv_metadata import CVMetadata
from domain.value_objects.cv_processing_status import CVStatus


class CVMetadataFactory(DataclassFactory[CVMetadata]):
    """Factory for generating CVMetadata test instances."""

    __model__ = CVMetadata

    @classmethod
    def id(cls):
        """Generate unique UUID."""
        return uuid4()

    @classmethod
    def filename(cls):
        """Generate filename."""
        return "cv_test.pdf"

    @classmethod
    def status(cls):
        """Default to PENDING status."""
        return CVStatus.PENDING

    @classmethod
    def created_at(cls):
        """Generate creation timestamp."""
        return datetime.now(tz=UTC)

    @classmethod
    def updated_at(cls):
        """Generate update timestamp."""
        return datetime.now(tz=UTC)

    @classmethod
    def extracted_text(cls):
        """Default to None."""
        return None

    @classmethod
    def search_query(cls):
        """Default to None."""
        return None


def create_cv_metadata_initial():
    cv_id = UUID("00000000-0000-0000-0000-000000000001")
    now = datetime.now(timezone.utc)
    return CVMetadata(
        id=cv_id,
        filename="test_cv.pdf",
        status=CVStatus.PENDING,
        created_at=now,
        updated_at=now,
    ), cv_id


def create_cv_metadata_completed():
    cv_metadata, cv_id = create_cv_metadata_initial()
    cv_metadata.status = CVStatus.COMPLETED
    cv_metadata.search_query = "Python developer with Django experience"
    cv_metadata.extracted_text = {
        "experiences": ["Software Engineer"],
        "skills": ["Python", "Django"],
    }
    return cv_metadata, cv_id
