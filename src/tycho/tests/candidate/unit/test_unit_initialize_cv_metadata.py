"""Unit tests for InitializeCVMetadataUsecase."""

from uuid import UUID

import pytest

from application.candidate.usecases.initialize_cv_metadata import (
    InitializeCVMetadataUsecase,
)
from domain.value_objects.cv_processing_status import CVStatus
from tests.utils.in_memory_cv_metadata_repository import InMemoryCVMetadataRepository


@pytest.fixture
def cv_metadata_repository():
    """Create an in-memory CV metadata repository for testing."""
    return InMemoryCVMetadataRepository()


@pytest.fixture
def usecase(cv_metadata_repository):
    """Create InitializeCVMetadataUsecase with in-memory repository."""
    return InitializeCVMetadataUsecase(cv_metadata_repository)


def test_execute_creates_cv_metadata_with_pending_status(
    usecase, cv_metadata_repository
):
    """Test that execute creates CV metadata with PENDING status."""
    filename = "test_cv.pdf"

    cv_id = usecase.execute(filename)

    # Verify UUID is returned as string
    assert isinstance(cv_id, str)
    uuid_obj = UUID(cv_id)  # Should not raise exception
    assert isinstance(uuid_obj, UUID)

    # Verify CV metadata was saved
    saved_cv = cv_metadata_repository.find_by_id(uuid_obj)
    assert saved_cv is not None
    assert saved_cv.filename == filename
    assert saved_cv.status == CVStatus.PENDING
    assert saved_cv.extracted_text is None
    assert saved_cv.search_query is None


def test_execute_creates_unique_ids(usecase, cv_metadata_repository):
    """Test that execute creates unique IDs for different calls."""
    filename1 = "cv1.pdf"
    filename2 = "cv2.pdf"
    expected_count = 2

    cv_id1 = usecase.execute(filename1)
    cv_id2 = usecase.execute(filename2)

    assert cv_id1 != cv_id2

    # Verify both CVs exist with correct data
    saved_cv1 = cv_metadata_repository.find_by_id(UUID(cv_id1))
    saved_cv2 = cv_metadata_repository.find_by_id(UUID(cv_id2))

    assert saved_cv1.filename == filename1
    assert saved_cv2.filename == filename2
    assert cv_metadata_repository.count() == expected_count


def test_execute_sets_timestamps(usecase, cv_metadata_repository):
    """Test that execute sets created_at and updated_at timestamps."""
    filename = "timestamped_cv.pdf"

    cv_id = usecase.execute(filename)

    saved_cv = cv_metadata_repository.find_by_id(UUID(cv_id))
    assert saved_cv.created_at is not None
    assert saved_cv.updated_at is not None
    # Both timestamps should be very close (same execution)
    time_diff = abs((saved_cv.updated_at - saved_cv.created_at).total_seconds())
    assert time_diff < 1.0  # Less than 1 second difference


def test_execute_with_empty_filename(usecase, cv_metadata_repository):
    """Test that execute works with empty filename."""
    filename = ""

    cv_id = usecase.execute(filename)

    saved_cv = cv_metadata_repository.find_by_id(UUID(cv_id))
    assert saved_cv.filename == ""
    assert saved_cv.status == CVStatus.PENDING
