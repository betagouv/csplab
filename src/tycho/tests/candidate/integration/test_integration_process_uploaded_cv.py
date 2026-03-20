"""Integration tests for ProcessUploadedCVUsecase with Django persistence."""

from uuid import UUID

import pytest

from domain.entities.cv_metadata import CVMetadata
from domain.exceptions.cv_errors import CVNotFoundError
from domain.value_objects.cv_processing_status import CVStatus
from infrastructure.exceptions.exceptions import ExternalApiError
from tests.utils.mock_api_response_factory import MockApiResponseFactory


@pytest.mark.django_db
async def test_execute_with_valid_pdf_updates_cv_metadatas(
    httpx_mock,
    albert_integration_container,
    pdf_content,
    cv_metadata_initial,
    test_app_config,
):
    container = albert_integration_container

    # Mock OCR service response
    ocr_response = MockApiResponseFactory.create_ocr_service_response()

    httpx_mock.add_response(
        method="POST",
        url=f"{test_app_config.ocr.base_url}extract-text",
        json=ocr_response,
        status_code=200,
    )

    # Mock Albert text formatter response
    albert_response = MockApiResponseFactory.create_albert_formatter_response()

    httpx_mock.add_response(
        method="POST",
        url=f"{test_app_config.albert.api_base_url}v1/chat/completions",
        json=albert_response,
        status_code=200,
    )

    # Unpack fixture data
    initial_cv, cv_id = cv_metadata_initial

    # Prepopulate the repository
    repo = container.async_cv_metadata_repository()
    await repo.save(initial_cv)

    usecase = container.process_uploaded_cv_usecase()

    result = await usecase.execute(cv_id, pdf_content)
    assert isinstance(result, CVMetadata)
    assert result.status == CVStatus.COMPLETED


@pytest.mark.django_db
async def test_execute_cv_metadatas_not_found(
    albert_integration_container, pdf_content
):
    container = albert_integration_container
    cv_id = UUID("00000000-0000-0000-0000-000000000000")  # UUID that doesn't exist

    usecase = container.process_uploaded_cv_usecase()
    with pytest.raises(CVNotFoundError):
        await usecase.execute(cv_id, pdf_content)


@pytest.mark.django_db
async def test_execute_with_api_failure_saves_failed_status_to_database(
    httpx_mock,
    albert_integration_container,
    pdf_content,
    cv_metadata_initial,
    test_app_config,
):
    container = albert_integration_container

    # Mock OCR service failure
    httpx_mock.add_response(
        method="POST",
        url=f"{test_app_config.ocr.base_url}extract-text",
        json={"error": "OCR Service Error"},
        status_code=500,
    )

    # Unpack fixture data
    initial_cv, cv_id = cv_metadata_initial

    # Prepopulate the repository with PENDING status
    repo = container.async_cv_metadata_repository()
    await repo.save(initial_cv)

    usecase = container.process_uploaded_cv_usecase()

    with pytest.raises(ExternalApiError):
        await usecase.execute(cv_id, pdf_content)

    # Verify that CV metadata was saved with FAILED status
    updated_cv = await repo.find_by_id(cv_id)
    assert updated_cv is not None
    assert updated_cv.status == CVStatus.FAILED
    assert updated_cv.updated_at > initial_cv.updated_at
