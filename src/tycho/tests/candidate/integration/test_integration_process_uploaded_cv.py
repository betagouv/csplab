"""Integration tests for ProcessUploadedCVUsecase with Django persistence."""

import json
from datetime import datetime
from uuid import UUID

import pytest
from asgiref.sync import sync_to_async

from domain.entities.cv_metadata import CVMetadata
from domain.exceptions.cv_errors import InvalidPDFError, TextExtractionError
from infrastructure.django_apps.candidate.models.cv_metadata import CVMetadataModel
from infrastructure.exceptions.exceptions import ExternalApiError


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_execute_with_valid_pdf_saves_to_database(
    httpx_mock, process_cv_usecase_integration, mock_api_responses, pdf_content
):
    """Test that valid PDF is processed and saved to real database."""
    httpx_mock.add_response(
        method="POST",
        url="https://albert.api.etalab.gouv.fr/v1/ocr-beta",
        json=mock_api_responses["albert"],
        status_code=200,
    )

    filename = "integration_test_cv.pdf"
    result = await process_cv_usecase_integration.execute(filename, pdf_content)

    assert isinstance(result, str)
    cv_id = UUID(result)

    cv_model = await sync_to_async(CVMetadataModel.objects.get)(id=cv_id)
    assert cv_model.filename == filename
    assert cv_model.extracted_text == mock_api_responses["albert"]
    assert "software engineer" in cv_model.search_query
    assert isinstance(cv_model.created_at, datetime)

    cv_entity = cv_model.to_entity()
    assert isinstance(cv_entity, CVMetadata)
    assert cv_entity.id == cv_id
    assert cv_entity.filename == filename
    assert cv_entity.extracted_text == mock_api_responses["albert"]


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_execute_with_invalid_pdf_does_not_save_to_database(
    process_cv_usecase_integration,
):
    """Test that invalid PDF raises error and doesn't save to database."""
    pdf_content = b"This is not a PDF file"
    filename = "invalid.pdf"

    initial_count = await sync_to_async(CVMetadataModel.objects.count)()

    with pytest.raises(InvalidPDFError) as exc_info:
        await process_cv_usecase_integration.execute(filename, pdf_content)

    assert exc_info.value.filename == filename
    final_count = await sync_to_async(CVMetadataModel.objects.count)()
    assert initial_count == final_count


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_execute_with_albert_api_failure_does_not_save_to_database(
    httpx_mock, process_cv_usecase_integration, pdf_content
):
    """Test that Albert API failure raises error and doesn't save to database."""
    httpx_mock.add_response(
        method="POST",
        url="https://albert.api.etalab.gouv.fr/v1/ocr-beta",
        json={"error": "API Error"},
        status_code=500,
    )

    filename = "test.pdf"
    initial_count = await sync_to_async(CVMetadataModel.objects.count)()

    with pytest.raises(ExternalApiError):
        await process_cv_usecase_integration.execute(filename, pdf_content)

    final_count = await sync_to_async(CVMetadataModel.objects.count)()
    assert initial_count == final_count


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_execute_with_empty_experiences_does_not_save_to_database(
    httpx_mock, process_cv_usecase_integration, pdf_content
):
    """Test that empty experiences raises error and doesn't save to database."""
    mock_response = {"experiences": [], "skills": []}

    httpx_mock.add_response(
        method="POST",
        url="https://albert.api.etalab.gouv.fr/v1/ocr-beta",
        json=mock_response,
        status_code=200,
    )

    filename = "empty_experiences.pdf"
    initial_count = await sync_to_async(CVMetadataModel.objects.count)()

    with pytest.raises(TextExtractionError):
        await process_cv_usecase_integration.execute(filename, pdf_content)

    final_count = await sync_to_async(CVMetadataModel.objects.count)()
    assert initial_count == final_count


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_multiple_cv_processing_creates_separate_records(
    httpx_mock, process_cv_usecase_integration, pdf_content, mock_api_responses
):
    """Test that multiple CV processing creates separate database records."""
    httpx_mock.add_response(
        method="POST",
        url="https://albert.api.etalab.gouv.fr/v1/ocr-beta",
        json=mock_api_responses["albert"],
        status_code=200,
    )

    initial_count = await sync_to_async(CVMetadataModel.objects.count)()

    result1 = await process_cv_usecase_integration.execute("cv1.pdf", pdf_content)
    cv_id1 = UUID(result1)

    httpx_mock.add_response(
        method="POST",
        url="https://albert.api.etalab.gouv.fr/v1/ocr-beta",
        json=mock_api_responses["albert"],
        status_code=200,
    )
    result2 = await process_cv_usecase_integration.execute("cv2.pdf", pdf_content)
    cv_id2 = UUID(result2)

    final_count = await sync_to_async(CVMetadataModel.objects.count)()
    assert final_count == initial_count + 2

    assert cv_id1 != cv_id2

    cv1_model = await sync_to_async(CVMetadataModel.objects.get)(id=cv_id1)
    cv2_model = await sync_to_async(CVMetadataModel.objects.get)(id=cv_id2)

    assert cv1_model.filename == "cv1.pdf"
    assert cv2_model.filename == "cv2.pdf"
    assert cv1_model.extracted_text == mock_api_responses["albert"]
    assert cv2_model.extracted_text == mock_api_responses["albert"]


# Tests with OpenAI PDF Extractor
@pytest.mark.asyncio
@pytest.mark.django_db
async def test_execute_with_valid_pdf_saves_to_database_openai(
    httpx_mock, openai_process_cv_usecase_integration, mock_api_responses, pdf_content
):
    """Test that valid PDF is processed and saved to real database using OpenAI."""
    httpx_mock.add_response(
        method="POST",
        url="https://openrouter.ai/api/v1/chat/completions",
        json={
            "choices": [
                {"message": {"content": json.dumps(mock_api_responses["openai"])}}
            ]
        },
        status_code=200,
    )

    filename = "openai_integration_test_cv.pdf"
    result = await openai_process_cv_usecase_integration.execute(filename, pdf_content)

    assert isinstance(result, str)
    cv_id = UUID(result)

    cv_model = await sync_to_async(CVMetadataModel.objects.get)(id=cv_id)
    assert cv_model.filename == filename
    assert cv_model.extracted_text == mock_api_responses["openai"]
    assert "software engineer" in cv_model.search_query
    assert isinstance(cv_model.created_at, datetime)

    cv_entity = cv_model.to_entity()
    assert isinstance(cv_entity, CVMetadata)
    assert cv_entity.id == cv_id
    assert cv_entity.filename == filename
    assert cv_entity.extracted_text == mock_api_responses["openai"]


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_execute_with_openai_api_failure_does_not_save_to_database(
    httpx_mock, openai_process_cv_usecase_integration, pdf_content
):
    """Test that OpenAI API failure raises error and doesn't save to database."""
    # Mock multiple potential retry attempts
    for _ in range(3):
        httpx_mock.add_response(
            method="POST",
            url="https://openrouter.ai/api/v1/chat/completions",
            json={"error": "API Error"},
            status_code=500,
        )

    filename = "openai_test.pdf"
    initial_count = await sync_to_async(CVMetadataModel.objects.count)()

    # OpenAI extractor raises ExternalApiError for HTTP errors with status codes
    with pytest.raises(ExternalApiError):
        await openai_process_cv_usecase_integration.execute(filename, pdf_content)

    final_count = await sync_to_async(CVMetadataModel.objects.count)()
    assert initial_count == final_count


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_execute_with_empty_experiences_does_not_save_to_db_openai(
    httpx_mock, openai_process_cv_usecase_integration, pdf_content
):
    """Test that empty experiences raises error and doesn't save to database."""
    mock_response = {"experiences": [], "skills": []}

    httpx_mock.add_response(
        method="POST",
        url="https://openrouter.ai/api/v1/chat/completions",
        json={"choices": [{"message": {"content": json.dumps(mock_response)}}]},
        status_code=200,
    )

    filename = "empty_experiences_openai.pdf"
    initial_count = await sync_to_async(CVMetadataModel.objects.count)()

    with pytest.raises(TextExtractionError):
        await openai_process_cv_usecase_integration.execute(filename, pdf_content)

    final_count = await sync_to_async(CVMetadataModel.objects.count)()
    assert initial_count == final_count


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_multiple_cv_processing_creates_separate_records_openai(
    httpx_mock, openai_process_cv_usecase_integration, pdf_content, mock_api_responses
):
    """Test that multiple CV processing creates separate DB records."""
    # First API call
    httpx_mock.add_response(
        method="POST",
        url="https://openrouter.ai/api/v1/chat/completions",
        json={
            "choices": [
                {"message": {"content": json.dumps(mock_api_responses["openai"])}}
            ]
        },
        status_code=200,
    )

    initial_count = await sync_to_async(CVMetadataModel.objects.count)()

    result1 = await openai_process_cv_usecase_integration.execute(
        "openai_cv1.pdf", pdf_content
    )
    cv_id1 = UUID(result1)

    # Second API call
    httpx_mock.add_response(
        method="POST",
        url="https://openrouter.ai/api/v1/chat/completions",
        json={
            "choices": [
                {"message": {"content": json.dumps(mock_api_responses["openai"])}}
            ]
        },
        status_code=200,
    )
    result2 = await openai_process_cv_usecase_integration.execute(
        "openai_cv2.pdf", pdf_content
    )
    cv_id2 = UUID(result2)

    final_count = await sync_to_async(CVMetadataModel.objects.count)()
    assert final_count == initial_count + 2

    assert cv_id1 != cv_id2

    cv1_model = await sync_to_async(CVMetadataModel.objects.get)(id=cv_id1)
    cv2_model = await sync_to_async(CVMetadataModel.objects.get)(id=cv_id2)

    assert cv1_model.filename == "openai_cv1.pdf"
    assert cv2_model.filename == "openai_cv2.pdf"
    assert cv1_model.extracted_text == mock_api_responses["openai"]
    assert cv2_model.extracted_text == mock_api_responses["openai"]
