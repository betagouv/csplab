"""Integration tests for ProcessUploadedCVUsecase with Django persistence."""

from datetime import datetime
from uuid import UUID

import pytest
from asgiref.sync import sync_to_async
from pydantic import HttpUrl

from domain.entities.cv_metadata import CVMetadata
from domain.exceptions.cv_errors import InvalidPDFError, TextExtractionError
from domain.value_objects.pdf_extractor_type import PDFExtractorType
from infrastructure.di.candidate.candidate_container import CandidateContainer
from infrastructure.django_apps.candidate.models.cv_metadata import CVMetadataModel
from infrastructure.exceptions.exceptions import ExternalApiError
from infrastructure.external_gateways.configs.albert_config import AlbertConfig
from infrastructure.external_gateways.configs.openai_config import OpenAIConfig
from infrastructure.external_gateways.configs.pdf_extractor_config import (
    PDFExtractorConfig,
)
from infrastructure.gateways.shared.logger import LoggerService
from tests.utils.pdf_test_utils import create_minimal_valid_pdf


def _create_integration_container(pdf_extractor_type=PDFExtractorType.ALBERT):
    """Create a container for integration tests with Django persistence."""
    container = CandidateContainer()

    logger_service = LoggerService()
    container.logger_service.override(logger_service)

    # Configure extractors for tests
    albert_config = AlbertConfig(
        api_base_url=HttpUrl("https://albert.api.etalab.gouv.fr"),
        api_key="test-albert-key",
        model_name="albert-large",
        dpi=200,
    )
    openai_config = OpenAIConfig(
        api_key="test-api-key",
        model="gpt-4o",
        base_url=HttpUrl("https://openrouter.ai/api/v1"),
    )
    pdf_config = PDFExtractorConfig(
        pdf_extractor_type=pdf_extractor_type,
        albert_config=albert_config,
        openai_config=openai_config,
    )
    container.config.override(pdf_config)

    return container


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_execute_with_valid_pdf_saves_to_database(httpx_mock):
    """Test that valid PDF is processed and saved to real database."""
    # Mock Albert API response with skills field
    mock_response = {
        "experiences": [
            {
                "title": "Software Engineer",
                "company": "Tech Corp",
                "sector": "Technology",
                "description": "5 years in Python development",
            }
        ],
        "skills": ["Python", "Django"],
    }

    httpx_mock.add_response(
        method="POST",
        url="https://albert.api.etalab.gouv.fr/v1/ocr-beta",
        json=mock_response,
        status_code=200,
    )

    container = _create_integration_container(PDFExtractorType.ALBERT)
    usecase = container.process_uploaded_cv_usecase()

    pdf_content = create_minimal_valid_pdf()
    filename = "integration_test_cv.pdf"

    result = await usecase.execute(filename, pdf_content)

    assert isinstance(result, str)
    cv_id = UUID(result)

    cv_model = await sync_to_async(CVMetadataModel.objects.get)(id=cv_id)
    assert cv_model.filename == filename
    assert cv_model.extracted_text == mock_response
    assert "software engineer" in cv_model.search_query
    assert isinstance(cv_model.created_at, datetime)

    cv_entity = cv_model.to_entity()
    assert isinstance(cv_entity, CVMetadata)
    assert cv_entity.id == cv_id
    assert cv_entity.filename == filename
    assert cv_entity.extracted_text == mock_response


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_execute_with_invalid_pdf_does_not_save_to_database():
    """Test that invalid PDF raises error and doesn't save to database."""
    container = _create_integration_container(PDFExtractorType.ALBERT)
    usecase = container.process_uploaded_cv_usecase()

    pdf_content = b"This is not a PDF file"
    filename = "invalid.pdf"

    initial_count = await sync_to_async(CVMetadataModel.objects.count)()

    with pytest.raises(InvalidPDFError) as exc_info:
        await usecase.execute(filename, pdf_content)

    assert exc_info.value.filename == filename
    final_count = await sync_to_async(CVMetadataModel.objects.count)()
    assert initial_count == final_count


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_execute_with_albert_api_failure_does_not_save_to_database(httpx_mock):
    """Test that Albert API failure raises error and doesn't save to database."""
    httpx_mock.add_response(
        method="POST",
        url="https://albert.api.etalab.gouv.fr/v1/ocr-beta",
        json={"error": "API Error"},
        status_code=500,
    )

    container = _create_integration_container(PDFExtractorType.ALBERT)
    usecase = container.process_uploaded_cv_usecase()

    pdf_content = create_minimal_valid_pdf()
    filename = "test.pdf"

    initial_count = await sync_to_async(CVMetadataModel.objects.count)()

    with pytest.raises(ExternalApiError):
        await usecase.execute(filename, pdf_content)

    final_count = await sync_to_async(CVMetadataModel.objects.count)()
    assert initial_count == final_count


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_execute_with_empty_experiences_does_not_save_to_database(httpx_mock):
    """Test that empty experiences raises error and doesn't save to database."""
    mock_response = {"experiences": [], "skills": []}

    httpx_mock.add_response(
        method="POST",
        url="https://albert.api.etalab.gouv.fr/v1/ocr-beta",
        json=mock_response,
        status_code=200,
    )

    container = _create_integration_container(PDFExtractorType.ALBERT)
    usecase = container.process_uploaded_cv_usecase()

    pdf_content = create_minimal_valid_pdf()
    filename = "empty_experiences.pdf"

    initial_count = await sync_to_async(CVMetadataModel.objects.count)()

    with pytest.raises(TextExtractionError):
        await usecase.execute(filename, pdf_content)

    final_count = await sync_to_async(CVMetadataModel.objects.count)()
    assert initial_count == final_count


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_multiple_cv_processing_creates_separate_records(httpx_mock):
    """Test that multiple CV processing creates separate database records."""
    mock_response = {
        "experiences": [
            {
                "title": "Data Scientist",
                "company": "AI Corp",
                "sector": "AI",
                "description": "3 years in machine learning",
            }
        ],
        "skills": ["Python", "Machine Learning"],
    }

    httpx_mock.add_response(
        method="POST",
        url="https://albert.api.etalab.gouv.fr/v1/ocr-beta",
        json=mock_response,
        status_code=200,
    )

    container = _create_integration_container(PDFExtractorType.ALBERT)
    usecase = container.process_uploaded_cv_usecase()

    pdf_content = create_minimal_valid_pdf()

    initial_count = await sync_to_async(CVMetadataModel.objects.count)()

    result1 = await usecase.execute("cv1.pdf", pdf_content)
    cv_id1 = UUID(result1)

    httpx_mock.add_response(
        method="POST",
        url="https://albert.api.etalab.gouv.fr/v1/ocr-beta",
        json=mock_response,
        status_code=200,
    )
    result2 = await usecase.execute("cv2.pdf", pdf_content)
    cv_id2 = UUID(result2)

    final_count = await sync_to_async(CVMetadataModel.objects.count)()
    assert final_count == initial_count + 2

    assert cv_id1 != cv_id2

    cv1_model = await sync_to_async(CVMetadataModel.objects.get)(id=cv_id1)
    cv2_model = await sync_to_async(CVMetadataModel.objects.get)(id=cv_id2)

    assert cv1_model.filename == "cv1.pdf"
    assert cv2_model.filename == "cv2.pdf"
    assert cv1_model.extracted_text == mock_response
    assert cv2_model.extracted_text == mock_response
