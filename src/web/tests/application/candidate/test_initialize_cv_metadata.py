from uuid import UUID

from domain.candidate.value_objects.cv_processing_status import CVStatus


def test_execute_creates_cv_metadata_with_pending_status(
    initialize_cv_metadata_usecase,
):
    filename = "test_cv.pdf"

    cv_id = initialize_cv_metadata_usecase.execute(filename)
    cv_metadata_repository = initialize_cv_metadata_usecase.cv_metadata_repository

    # Verify UUID is returned as string
    assert isinstance(cv_id, str)
    uuid_obj = UUID(cv_id)  # Should not raise exception
    assert isinstance(uuid_obj, UUID)

    # Verify CV metadata was saved
    saved_cv = cv_metadata_repository.get_by_id(uuid_obj)
    assert saved_cv is not None
    assert saved_cv.filename == filename
    assert saved_cv.status == CVStatus.PENDING
    assert saved_cv.extracted_text is None
    assert saved_cv.search_query is None


def test_execute_creates_unique_ids(initialize_cv_metadata_usecase):
    filename1 = "cv1.pdf"
    filename2 = "cv2.pdf"
    expected_count = 2

    cv_id1 = initialize_cv_metadata_usecase.execute(filename1)
    cv_id2 = initialize_cv_metadata_usecase.execute(filename2)

    cv_metadata_repository = initialize_cv_metadata_usecase.cv_metadata_repository

    assert cv_id1 != cv_id2

    # Verify both CVs exist with correct data
    saved_cv1 = cv_metadata_repository.get_by_id(UUID(cv_id1))
    saved_cv2 = cv_metadata_repository.get_by_id(UUID(cv_id2))

    assert saved_cv1.filename == filename1
    assert saved_cv2.filename == filename2
    assert cv_metadata_repository.count() == expected_count


def test_execute_sets_timestamps(initialize_cv_metadata_usecase):
    filename = "timestamped_cv.pdf"

    cv_id = initialize_cv_metadata_usecase.execute(filename)
    cv_metadata_repository = initialize_cv_metadata_usecase.cv_metadata_repository

    saved_cv = cv_metadata_repository.get_by_id(UUID(cv_id))
    assert saved_cv.created_at is not None
    assert saved_cv.updated_at is not None
    # Both timestamps should be very close (same execution)
    time_diff = abs((saved_cv.updated_at - saved_cv.created_at).total_seconds())
    assert time_diff < 1.0  # Less than 1 second difference


def test_execute_with_empty_filename(initialize_cv_metadata_usecase):
    filename = ""

    cv_id = initialize_cv_metadata_usecase.execute(filename)
    cv_metadata_repository = initialize_cv_metadata_usecase.cv_metadata_repository

    saved_cv = cv_metadata_repository.get_by_id(UUID(cv_id))
    assert saved_cv.filename == ""
    assert saved_cv.status == CVStatus.PENDING
