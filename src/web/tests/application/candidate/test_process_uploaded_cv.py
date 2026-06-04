from uuid import UUID

import pytest

from domain.candidate.entities.cv_metadata import CVMetadata
from domain.candidate.exceptions.cv_errors import CVNotFoundError
from domain.candidate.value_objects.cv_processing_status import CVStatus
from tests.factories.candidate.cv_metadata_factory import (
    CVMetadataFactory,
)


async def test_execute_with_valid_pdf_updates_cv_metadatas(
    process_uploaded_cv_usecase, pdf_content
):
    repo = process_uploaded_cv_usecase.async_cv_metadata_repository
    initial_cv = CVMetadataFactory.create_entity(status=CVStatus.PENDING)

    await repo.save(initial_cv)

    result = await process_uploaded_cv_usecase.execute(
        initial_cv.entity_id, pdf_content
    )
    assert isinstance(result, CVMetadata)
    assert result.status == CVStatus.COMPLETED


async def test_execute_cv_metadatas_not_found(process_uploaded_cv_usecase, pdf_content):
    cv_id = UUID("00000000-0000-0000-0000-000000000000")

    with pytest.raises(CVNotFoundError):
        await process_uploaded_cv_usecase.execute(cv_id, pdf_content)
