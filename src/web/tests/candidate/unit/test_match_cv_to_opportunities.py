import pytest

from domain.exceptions.cv_errors import CVProcessingFailedError
from domain.value_objects.cv_processing_status import CVStatus
from tests.factories.cv_metadata_factory import CVMetadataFactory


def test_execute_with_failed_cv_raises_error(match_cv_to_opportunities_usecase):
    cv_metadata = CVMetadataFactory.create_entity(status=CVStatus.FAILED)

    cv_repo = match_cv_to_opportunities_usecase.cv_metadata_repository
    cv_repo.save(cv_metadata)

    with pytest.raises(CVProcessingFailedError) as exc_info:
        match_cv_to_opportunities_usecase.execute(cv_metadata, limit=10)

    assert exc_info.value.cv_id == str(cv_metadata.id)
