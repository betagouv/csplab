"""Integration tests for ProcessUploadedCVUsecase with Django persistence."""

import json
from uuid import UUID

import pytest

from domain.entities.cv_metadata import CVMetadata
from domain.exceptions.cv_errors import CVNotFoundError
from domain.value_objects.cv_processing_status import CVStatus
from infrastructure.exceptions.exceptions import ExternalApiError
from tests.utils.mock_api_response_factory import MockApiResponseFactory


@pytest.mark.parametrize(
    "container_name",
    ["albert_integration_container", "openai_integration_container"],
)
@pytest.mark.django_db
async def test_execute_with_valid_pdf_updates_cv_metadatas(
    httpx_mock,
    request,
    pdf_content,
    container_name,
    cv_metadata_initial,
    test_app_config,
):
    """Test that valid PDF is processed and saved to real database."""
    container = request.getfixturevalue(container_name)
    extractor_type = "albert" if "albert" in container_name else "openai"

    mock_response = MockApiResponseFactory.create_ocr_api_response(
        experiences=[("Software Engineer", "Tech Corp")],
        skills=["Python", "Django"],
        description="5 years in Python development",
    )

    # Configuration spécifique selon l'extracteur
    if extractor_type == "albert":
        api_url = f"{test_app_config.albert_api_base_url}v1/ocr-beta"
        response_json = mock_response
    else:  # openai
        api_url = f"{test_app_config.openrouter_base_url}/chat/completions"
        response_json = {
            "choices": [{"message": {"content": json.dumps(mock_response)}}]
        }

    httpx_mock.add_response(
        method="POST",
        url=api_url,
        json=response_json,
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


@pytest.mark.parametrize(
    "container_name",
    ["albert_integration_container", "openai_integration_container"],
)
@pytest.mark.django_db
async def test_execute_cv_metadatas_not_found(request, pdf_content, container_name):
    """Test that CVNotFoundError is raised when CV metadata doesn't exist."""
    container = request.getfixturevalue(container_name)
    cv_id = UUID("00000000-0000-0000-0000-000000000000")  # UUID that doesn't exist

    usecase = container.process_uploaded_cv_usecase()
    with pytest.raises(CVNotFoundError):
        await usecase.execute(cv_id, pdf_content)


@pytest.mark.parametrize(
    "container_name", ["albert_integration_container", "openai_integration_container"]
)
@pytest.mark.django_db
async def test_execute_with_api_failure_saves_failed_status_to_database(
    httpx_mock,
    request,
    pdf_content,
    container_name,
    cv_metadata_initial,
    test_app_config,
):
    """Test that API failure raises error and saves CV with FAILED status to DB."""
    container = request.getfixturevalue(container_name)
    extractor_type = "albert" if "albert" in container_name else "openai"

    # Configuration spécifique selon l'extracteur
    if extractor_type == "albert":
        api_url = f"{test_app_config.albert_api_base_url}v1/ocr-beta"
        retry_count = 1
    else:  # openai
        api_url = f"{test_app_config.openrouter_base_url}/chat/completions"
        retry_count = 3

    # Mock multiple potential retry attempts
    for _ in range(retry_count):
        httpx_mock.add_response(
            method="POST",
            url=api_url,
            json={"error": "API Error"},
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
