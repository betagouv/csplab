"""Polyfactory for CVMetadata entity."""

from datetime import UTC, datetime
from uuid import uuid4

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
