"""Unit test cases for ProcessUploadedCVUsecase."""

import json
from uuid import UUID

import pytest

from domain.entities.cv_metadata import CVMetadata
from domain.exceptions.cv_errors import CVNotFoundError, TextExtractionError
from domain.value_objects.cv_processing_status import CVStatus
from tests.utils.mock_api_response_factory import MockApiResponseFactory


@pytest.mark.parametrize(
    "container_name",
    ["albert_candidate_container", "openai_candidate_container"],
)
async def test_execute_with_valid_pdf_updates_cv_metadatas(
    httpx_mock, request, pdf_content, container_name, cv_metadata_initial
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
        api_url = "https://albert.api.etalab.gouv.fr/v1/ocr-beta"
        response_json = mock_response
    else:  # openai
        api_url = "https://openrouter.ai/api/v1/chat/completions"
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
    httpx_mock, request, pdf_content, container_name, cv_metadata_initial
):
    """Test that valid PDF is processed and saved to real database."""
    container = request.getfixturevalue(container_name)
    extractor_type = "albert" if "albert" in container_name else "openai"

    mock_response = MockApiResponseFactory.create_ocr_api_response(
        experiences=[],
        skills=[],
        description="",
    )

    # Configuration spécifique selon l'extracteur
    if extractor_type == "albert":
        api_url = "https://albert.api.etalab.gouv.fr/v1/ocr-beta"
        response_json = mock_response
    else:  # openai
        api_url = "https://openrouter.ai/api/v1/chat/completions"
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

    with pytest.raises(TextExtractionError):
        await usecase.execute(cv_id, pdf_content)
