"""Integration tests for ProcessUploadedCVUsecase with Django persistence."""

from datetime import datetime
from uuid import UUID

import pytest

from domain.entities.cv_metadata import CVMetadata
from domain.exceptions.cv_errors import InvalidPDFError, TextExtractionError
from infrastructure.django_apps.candidate.models.cv_metadata import CVMetadataModel
from infrastructure.exceptions.exceptions import ExternalApiError
from tests.utils.mock_api_response_factory import MockApiResponseFactory


@pytest.mark.django_db
async def test_execute_with_valid_pdf_saves_to_database(
    httpx_mock, request, pdf_content, extractor_config_integration
):
    """Test that valid PDF is processed and saved to real database."""
    mock_response = MockApiResponseFactory.create_ocr_api_response(
        experiences=[("Software Engineer", "Tech Corp")],
        skills=["Python", "Django"],
        description="5 years in Python development",
    )

    httpx_mock.add_response(
        method="POST",
        url=extractor_config_integration["api_url"],
        json=extractor_config_integration["response_wrapper"](mock_response),
        status_code=200,
    )

    usecase = request.getfixturevalue(extractor_config_integration["usecase_fixture"])
    filename = f"{extractor_config_integration['type']}_integration_test_cv.pdf"
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


@pytest.mark.django_db
async def test_execute_with_invalid_pdf_does_not_save_to_database(
    process_cv_usecase_integration,
):
    """Test that invalid PDF raises error and doesn't save to database."""
    pdf_content = b"This is not a PDF file"
    filename = "invalid.pdf"

    initial_count = await CVMetadataModel.objects.acount()

    with pytest.raises(InvalidPDFError) as exc_info:
        await process_cv_usecase_integration.execute(filename, pdf_content)

    assert exc_info.value.filename == filename
    final_count = await CVMetadataModel.objects.acount()
    assert initial_count == final_count


@pytest.mark.django_db
async def test_execute_with_api_failure_does_not_save_to_database(
    httpx_mock, request, pdf_content, extractor_config_integration
):
    """Test that API failure raises error and doesn't save to database."""
    # Mock multiple potential retry attempts for OpenAI
    for _ in range(extractor_config_integration["retry_count"]):
        httpx_mock.add_response(
            method="POST",
            url=extractor_config_integration["api_url"],
            json={"error": "API Error"},
            status_code=500,
        )

    filename = f"{extractor_config_integration['type']}_test.pdf"
    initial_count = await CVMetadataModel.objects.acount()

    with pytest.raises(ExternalApiError):
        usecase = request.getfixturevalue(
            extractor_config_integration["usecase_fixture"]
        )
        await usecase.execute(filename, pdf_content)

    final_count = await CVMetadataModel.objects.acount()
    assert initial_count == final_count


@pytest.mark.django_db
async def test_execute_with_empty_experiences_does_not_save_to_database(
    httpx_mock, request, pdf_content, extractor_config_integration
):
    """Test that empty experiences raises error and doesn't save to database."""
    mock_response = MockApiResponseFactory.create_empty_response()

    httpx_mock.add_response(
        method="POST",
        url=extractor_config_integration["api_url"],
        json=extractor_config_integration["response_wrapper"](mock_response),
        status_code=200,
    )

    filename = f"empty_experiences_{extractor_config_integration['type']}.pdf"
    initial_count = await CVMetadataModel.objects.acount()

    with pytest.raises(TextExtractionError):
        usecase = request.getfixturevalue(
            extractor_config_integration["usecase_fixture"]
        )
        await usecase.execute(filename, pdf_content)

    final_count = await CVMetadataModel.objects.acount()
    assert initial_count == final_count


@pytest.mark.django_db
async def test_multiple_cv_processing_creates_separate_records(
    httpx_mock, request, pdf_content, extractor_config_integration
):
    """Test that multiple CV processing creates separate database records."""
    mock_response = MockApiResponseFactory.create_ocr_api_response(
        experiences=[("Software Engineer", "Tech Corp")],
        skills=["Python", "Django"],
        description="5 years in Python development",
    )

    # First API call
    httpx_mock.add_response(
        method="POST",
        url=extractor_config_integration["api_url"],
        json=extractor_config_integration["response_wrapper"](mock_response),
        status_code=200,
    )

    initial_count = await CVMetadataModel.objects.acount()
    usecase = request.getfixturevalue(extractor_config_integration["usecase_fixture"])

    result1 = await usecase.execute(
        f"{extractor_config_integration['type']}_cv1.pdf", pdf_content
    )
    cv_id1 = UUID(result1)

    # Second API call
    httpx_mock.add_response(
        method="POST",
        url=extractor_config_integration["api_url"],
        json=extractor_config_integration["response_wrapper"](mock_response),
        status_code=200,
    )
    result2 = await usecase.execute(
        f"{extractor_config_integration['type']}_cv2.pdf", pdf_content
    )
    cv_id2 = UUID(result2)

    final_count = await CVMetadataModel.objects.acount()
    assert final_count == initial_count + 2

    assert cv_id1 != cv_id2

    cv1_model = await CVMetadataModel.objects.aget(id=cv_id1)
    cv2_model = await CVMetadataModel.objects.aget(id=cv_id2)

    assert cv1_model.filename == f"{extractor_config_integration['type']}_cv1.pdf"
    assert cv2_model.filename == f"{extractor_config_integration['type']}_cv2.pdf"
    assert cv1_model.extracted_text == mock_response
    assert cv2_model.extracted_text == mock_response
