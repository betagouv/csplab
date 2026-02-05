"""Test utilities for CV-related tests."""

from uuid import UUID

from domain.value_objects.cv_processing_status import CVStatus
from infrastructure.django_apps.candidate.models.cv_metadata import CVMetadataModel
from tests.factories.cv_metadata_factory import CVMetadataFactory


def create_cv_in_database(status: CVStatus = CVStatus.COMPLETED) -> UUID:
    """Create a CV with given status in database and return its UUID."""
    cv_metadata = CVMetadataFactory.build(status=status)
    CVMetadataModel.from_entity(cv_metadata).save()
    return cv_metadata.id
