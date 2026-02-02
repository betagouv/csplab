"""Integration tests for InitializeCVMetadataUsecase with Django."""

from uuid import UUID

import pytest

from application.candidate.usecases.initialize_cv_metadata import (
    InitializeCVMetadataUsecase,
)
from domain.value_objects.cv_processing_status import CVStatus
from infrastructure.django_apps.candidate.models.cv_metadata import CVMetadataModel
from infrastructure.repositories.candidate.postgres_cv_metadata_repository import (
    PostgresCVMetadataRepository,
)


@pytest.fixture
def cv_metadata_repository():
    """Create a PostgreSQL CV metadata repository for integration testing."""
    return PostgresCVMetadataRepository()


@pytest.fixture
def usecase(cv_metadata_repository):
    """Create InitializeCVMetadataUsecase with PostgreSQL repository."""
    return InitializeCVMetadataUsecase(cv_metadata_repository)


@pytest.mark.django_db
def test_execute_creates_cv_metadata_in_database(usecase):
    """Test that execute creates CV metadata in the database."""
    filename = "integration_test_cv.pdf"
    initial_count = CVMetadataModel.objects.count()

    cv_id = usecase.execute(filename)

    # Verify UUID is returned as string
    assert isinstance(cv_id, str)
    uuid_obj = UUID(cv_id)
    assert isinstance(uuid_obj, UUID)

    # Verify CV metadata was saved in database
    final_count = CVMetadataModel.objects.count()
    assert final_count == initial_count + 1

    # Verify the saved data
    cv_model = CVMetadataModel.objects.get(id=uuid_obj)
    assert cv_model.filename == filename
    assert cv_model.status == CVStatus.PENDING.value
    assert cv_model.extracted_text is None
    assert cv_model.search_query is None
    assert cv_model.created_at is not None
    assert cv_model.updated_at is not None

    # Test entity conversion
    cv_entity = cv_model.to_entity()
    assert cv_entity.filename == filename
    assert cv_entity.status == CVStatus.PENDING
