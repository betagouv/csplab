"""Integration tests for ProcessUploadedCVUsecase with Django persistence."""

import json
from datetime import datetime
from uuid import UUID

import pytest

from domain.entities.cv_metadata import CVMetadata
from infrastructure.django_apps.candidate.models.cv_metadata import CVMetadataModel
from infrastructure.exceptions.exceptions import ExternalApiError
from tests.utils.mock_api_response_factory import MockApiResponseFactory


@pytest.mark.parametrize(
    "container_name", ["albert_integration_container", "openai_integration_container"]
)
@pytest.mark.django_db
async def test_execute_with_valid_pdf_saves_to_database(
    httpx_mock, request, pdf_content, container_name
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

    usecase = container.process_uploaded_cv_usecase()
    filename = f"{extractor_type}_integration_test_cv.pdf"
    result = await usecase.execute(filename, pdf_content)

    assert isinstance(result, str)
    cv_id = UUID(result)

    cv_model = await CVMetadataModel.objects.aget(id=cv_id)
    assert cv_model.filename == filename
    assert cv_model.extracted_text == mock_response
    assert "software engineer" in cv_model.search_query
    assert isinstance(cv_model.created_at, datetime)

    cv_entity = cv_model.to_entity()
    assert isinstance(cv_entity, CVMetadata)
    assert cv_entity.id == cv_id
    assert cv_entity.filename == filename
    assert cv_entity.extracted_text == mock_response


@pytest.mark.parametrize(
    "container_name", ["albert_integration_container", "openai_integration_container"]
)
@pytest.mark.django_db
async def test_execute_with_api_failure_does_not_save_to_database(
    httpx_mock, request, pdf_content, container_name
):
    """Test that API failure raises error and doesn't save to database."""
    container = request.getfixturevalue(container_name)
    extractor_type = "albert" if "albert" in container_name else "openai"

    # Configuration spécifique selon l'extracteur
    if extractor_type == "albert":
        api_url = "https://albert.api.etalab.gouv.fr/v1/ocr-beta"
        retry_count = 1
    else:  # openai
        api_url = "https://openrouter.ai/api/v1/chat/completions"
        retry_count = 3

    # Mock multiple potential retry attempts
    for _ in range(retry_count):
        httpx_mock.add_response(
            method="POST",
            url=api_url,
            json={"error": "API Error"},
            status_code=500,
        )

    filename = f"{extractor_type}_test.pdf"
    initial_count = await CVMetadataModel.objects.acount()

    with pytest.raises(ExternalApiError):
        usecase = container.process_uploaded_cv_usecase()
        await usecase.execute(filename, pdf_content)

    final_count = await CVMetadataModel.objects.acount()
    assert initial_count == final_count
