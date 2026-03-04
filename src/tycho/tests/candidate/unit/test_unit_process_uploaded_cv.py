"""Unit test cases for ProcessUploadedCVUsecase."""

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
    ["albert_candidate_container", "openai_candidate_container"],
)
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
        response_json = MockApiResponseFactory.create_albert_ocr_response(mock_response)
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
    ["albert_candidate_container", "openai_candidate_container"],
)
async def test_execute_cv_metadatas_not_found(request, pdf_content, container_name):
    """Test that CVNotFoundError is raised when CV metadata doesn't exist."""
    container = request.getfixturevalue(container_name)
    cv_id = UUID("00000000-0000-0000-0000-000000000000")  # UUID that doesn't exist

    usecase = container.process_uploaded_cv_usecase()
    with pytest.raises(CVNotFoundError):
        await usecase.execute(cv_id, pdf_content)


@pytest.mark.parametrize(
    "container_name",
    ["albert_candidate_container", "openai_candidate_container"],
)
async def test_execute_ocr_error(
    httpx_mock,
    request,
    pdf_content,
    container_name,
    cv_metadata_initial,
    test_app_config,
):
    """Test that API failure raises ExternalApiError and saves CV with FAILED."""
    container = request.getfixturevalue(container_name)
    extractor_type = "albert" if "albert" in container_name else "openai"

    if extractor_type == "albert":
        api_url = f"{test_app_config.albert_api_base_url}v1/ocr-beta"
    else:  # openai
        api_url = f"{test_app_config.openrouter_base_url}/chat/completions"

    # OpenAI can make multiple requests (retries), Albert makes only one
    num_requests = 3 if extractor_type == "openai" else 1
    for _ in range(num_requests):
        httpx_mock.add_response(
            method="POST",
            url=api_url,
            json={"error": "Internal server error"},
            status_code=500,
        )
    initial_cv, cv_id = cv_metadata_initial

    # Prepopulate the repository
    repo = container.async_cv_metadata_repository()
    await repo.save(initial_cv)

    usecase = container.process_uploaded_cv_usecase()

    with pytest.raises(ExternalApiError):
        await usecase.execute(cv_id, pdf_content)

    updated_cv = await repo.find_by_id(cv_id)
    assert updated_cv is not None
    assert updated_cv.status == CVStatus.FAILED


@pytest.mark.parametrize(
    "container_name",
    ["albert_candidate_container", "openai_candidate_container"],
)
async def test_execute_json_decode_error_with_details(
    httpx_mock,
    request,
    pdf_content,
    container_name,
    cv_metadata_initial,
    test_app_config,
):
    """Test that JSONDecodeError includes detailed error information."""
    container = request.getfixturevalue(container_name)
    extractor_type = "albert" if "albert" in container_name else "openai"

    # Mock invalid JSON response selon l'extracteur
    invalid_json_content = '{"experiences": [invalid json here'

    if extractor_type == "albert":
        api_url = f"{test_app_config.albert_api_base_url}v1/ocr-beta"
        response_json = (
            MockApiResponseFactory.create_albert_ocr_response_with_invalid_json(
                invalid_json_content
            )
        )
    else:  # openai
        api_url = f"{test_app_config.openrouter_base_url}/chat/completions"
        response_json = {"choices": [{"message": {"content": invalid_json_content}}]}

    expected_error_message = "Failed to parse JSON response."

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

    with pytest.raises(ExternalApiError) as exc_info:
        await usecase.execute(cv_id, pdf_content)

    # Verify the error message contains detailed JSON parsing information
    error_message = str(exc_info.value)
    assert expected_error_message in error_message


@pytest.mark.parametrize(
    "container_name",
    ["albert_candidate_container", "openai_candidate_container"],
)
async def test_execute_with_none_values_in_cv_data(
    httpx_mock,
    request,
    pdf_content,
    container_name,
    cv_metadata_initial,
    test_app_config,
):
    """Test that CV processing handles None values in company and description fields."""
    container = request.getfixturevalue(container_name)
    extractor_type = "albert" if "albert" in container_name else "openai"

    # Use the new fixture with None values
    mock_response = MockApiResponseFactory.create_ocr_response_with_none_values()

    # Configuration spécifique selon l'extracteur
    if extractor_type == "albert":
        api_url = f"{test_app_config.albert_api_base_url}v1/ocr-beta"
        response_json = MockApiResponseFactory.create_albert_ocr_response(mock_response)
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

    # This should not raise a ValidationError anymore
    result = await usecase.execute(cv_id, pdf_content)
    assert isinstance(result, CVMetadata)
    assert result.status == CVStatus.COMPLETED
