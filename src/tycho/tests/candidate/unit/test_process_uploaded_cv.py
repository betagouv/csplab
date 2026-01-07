"""Unit test cases for ProcessUploadedCVUsecase."""

from datetime import datetime
from uuid import UUID

import pytest
import responses
from pydantic import HttpUrl

from domain.exceptions.cv_errors import InvalidPDFError
from domain.value_objects.pdf_extractor_type import PDFExtractorType
from infrastructure.di.candidate.candidate_container import CandidateContainer
from infrastructure.external_gateways.configs.albert_config import AlbertConfig
from infrastructure.external_gateways.configs.openai_config import OpenAIConfig
from infrastructure.external_gateways.configs.pdf_extractor_config import (
    PDFExtractorConfig,
)
from infrastructure.gateways.shared.logger import LoggerService
from tests.utils.in_memory_cv_metadata_repository import InMemoryCVMetadataRepository
from tests.utils.pdf_test_utils import create_large_pdf, create_minimal_valid_pdf


def _create_isolated_container(pdf_extractor_type=PDFExtractorType.ALBERT):
    """Create an isolated container."""
    container = CandidateContainer()

    logger_service = LoggerService()
    container.logger_service.override(logger_service)

    in_memory_cv_repo = InMemoryCVMetadataRepository()
    container.postgres_cv_metadata_repository.override(in_memory_cv_repo)

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


@responses.activate
def test_execute_with_valid_pdf_returns_cv_id_albert():
    """Test that a valid PDF is processed successfully with Albert extractor."""
    # Mock Albert API response - format that Albert actually returns
    mock_response = {
        "experiences": [
            {
                "title": "Software Engineer",
                "company": "Tech Corp",
                "sector": "Technology",
                "description": "5 years in Python development",
            }
        ]
    }

    responses.add(
        responses.POST,
        "https://albert.api.etalab.gouv.fr/v1/ocr-beta",
        json=mock_response,
        status=200,
        content_type="application/json",
    )

    container = _create_isolated_container(PDFExtractorType.ALBERT)
    usecase = container.process_uploaded_cv_usecase()

    pdf_content = create_minimal_valid_pdf()
    filename = "test_cv.pdf"

    result = usecase.execute(filename, pdf_content)

    assert isinstance(result, str)
    cv_id = UUID(result)

    cv_repo = container.postgres_cv_metadata_repository()
    assert cv_repo.count() == 1

    saved_cv = cv_repo.find_by_id(cv_id)
    assert saved_cv is not None
    assert saved_cv.filename == filename
    assert isinstance(saved_cv.extracted_text, dict)
    assert "experiences" in saved_cv.extracted_text
    assert len(saved_cv.extracted_text["experiences"]) == 1
    assert isinstance(saved_cv.created_at, datetime)


def test_execute_with_valid_pdf_returns_cv_id_openai(httpx_mock):
    """Test that a valid PDF is processed successfully with OpenAI extractor."""
    # Mock OpenAI API response using pytest-httpx
    mock_response = {
        "choices": [
            {
                "message": {
                    "content": (
                        '{"experiences": [{"title": "Software Engineer", '
                        '"company": "Tech Corp", "sector": "Technology", '
                        '"description": "5 years in Python development"}], '
                        '"skills": ["Python", "Django"]}'
                    )
                }
            }
        ]
    }

    httpx_mock.add_response(
        method="POST",
        url="https://openrouter.ai/api/v1/chat/completions",
        json=mock_response,
        status_code=200,
    )

    container = _create_isolated_container(PDFExtractorType.OPENAI)
    usecase = container.process_uploaded_cv_usecase()

    pdf_content = create_minimal_valid_pdf()
    filename = "test_cv.pdf"

    result = usecase.execute(filename, pdf_content)

    assert isinstance(result, str)
    cv_id = UUID(result)

    cv_repo = container.postgres_cv_metadata_repository()
    assert cv_repo.count() == 1

    saved_cv = cv_repo.find_by_id(cv_id)
    assert saved_cv is not None
    assert saved_cv.filename == filename
    assert isinstance(saved_cv.extracted_text, dict)
    assert "experiences" in saved_cv.extracted_text
    assert len(saved_cv.extracted_text["experiences"]) == 1
    assert isinstance(saved_cv.created_at, datetime)


def test_execute_with_invalid_pdf_raises_invalid_pdf_error_albert():
    """Test that invalid PDF content raises InvalidPDFError with Albert extractor."""
    container = _create_isolated_container(PDFExtractorType.ALBERT)
    usecase = container.process_uploaded_cv_usecase()

    pdf_content = b"This is not a PDF file"
    filename = "invalid.pdf"

    with pytest.raises(InvalidPDFError) as exc_info:
        usecase.execute(filename, pdf_content)

    assert exc_info.value.filename == filename
    cv_repo = container.postgres_cv_metadata_repository()
    assert cv_repo.count() == 0


def test_execute_with_invalid_pdf_raises_invalid_pdf_error_openai():
    """Test that invalid PDF content raises InvalidPDFError with OpenAI extractor."""
    container = _create_isolated_container(PDFExtractorType.OPENAI)
    usecase = container.process_uploaded_cv_usecase()

    pdf_content = b"This is not a PDF file"
    filename = "invalid.pdf"

    with pytest.raises(InvalidPDFError) as exc_info:
        usecase.execute(filename, pdf_content)

    assert exc_info.value.filename == filename
    cv_repo = container.postgres_cv_metadata_repository()
    assert cv_repo.count() == 0


def test_execute_with_empty_pdf_raises_invalid_pdf_error_albert():
    """Test that empty PDF content raises InvalidPDFError with Albert extractor."""
    container = _create_isolated_container(PDFExtractorType.ALBERT)
    usecase = container.process_uploaded_cv_usecase()

    pdf_content = b""
    filename = "empty.pdf"

    with pytest.raises(InvalidPDFError) as exc_info:
        usecase.execute(filename, pdf_content)

    assert exc_info.value.filename == filename
    cv_repo = container.postgres_cv_metadata_repository()
    assert cv_repo.count() == 0


def test_execute_with_empty_pdf_raises_invalid_pdf_error_openai():
    """Test that empty PDF content raises InvalidPDFError with OpenAI extractor."""
    container = _create_isolated_container(PDFExtractorType.OPENAI)
    usecase = container.process_uploaded_cv_usecase()

    pdf_content = b""
    filename = "empty.pdf"

    with pytest.raises(InvalidPDFError) as exc_info:
        usecase.execute(filename, pdf_content)

    assert exc_info.value.filename == filename
    cv_repo = container.postgres_cv_metadata_repository()
    assert cv_repo.count() == 0


def test_query_builder_extracts_keywords_correctly():
    """Test that query builder extracts keywords from CV structured data."""
    container = _create_isolated_container(PDFExtractorType.ALBERT)
    query_builder = container.query_builder()

    cv_data = {
        "experiences": [
            {
                "title": "Software Engineer",
                "company": "Tech Corp",
                "sector": "Technology",
                "description": "5 years experience",
            }
        ]
    }
    result = query_builder.build_query(cv_data)
    assert "software engineer" in result

    cv_data = {
        "experiences": [
            {
                "title": "Project Manager",
                "company": "Corp",
                "sector": "Business",
                "description": "Team lead",
            }
        ]
    }
    result = query_builder.build_query(cv_data)
    assert "project manager" in result

    cv_data = {"experiences": []}
    result = query_builder.build_query(cv_data)
    assert result == ""


def test_both_extractors_validate_pdf_consistently():
    """Test that both extractors validate PDFs consistently."""
    albert_container = _create_isolated_container(PDFExtractorType.ALBERT)
    openai_container = _create_isolated_container(PDFExtractorType.OPENAI)

    albert_extractor = albert_container.pdf_text_extractor()
    openai_extractor = openai_container.pdf_text_extractor()

    # Test cases
    valid_pdf = create_minimal_valid_pdf()
    invalid_pdf = b"Not a PDF"
    empty_pdf = b""
    large_pdf = create_large_pdf()

    # Both should validate consistently
    assert albert_extractor.validate_pdf(valid_pdf) == openai_extractor.validate_pdf(
        valid_pdf
    )
    assert albert_extractor.validate_pdf(invalid_pdf) == openai_extractor.validate_pdf(
        invalid_pdf
    )
    assert albert_extractor.validate_pdf(empty_pdf) == openai_extractor.validate_pdf(
        empty_pdf
    )
    assert albert_extractor.validate_pdf(large_pdf) == openai_extractor.validate_pdf(
        large_pdf
    )


@responses.activate
def test_both_extractors_process_same_pdf_consistently(httpx_mock):
    """Test that both extractors process the same PDF consistently."""
    # Mock Albert API response
    albert_mock_response = {
        "experiences": [
            {
                "title": "Data Scientist",
                "company": "AI Corp",
                "sector": "Technology",
                "description": "3 years in machine learning",
            }
        ]
    }

    responses.add(
        responses.POST,
        "https://albert.api.etalab.gouv.fr/v1/ocr-beta",
        json=albert_mock_response,
        status=200,
        content_type="application/json",
    )

    # Mock OpenAI API response
    openai_mock_response = {
        "choices": [
            {
                "message": {
                    "content": (
                        '{"experiences": [{"title": "Data Scientist", '
                        '"company": "AI Corp", "sector": "Technology", '
                        '"description": "3 years in machine learning"}], '
                        '"skills": ["Python", "Machine Learning"]}'
                    )
                }
            }
        ]
    }

    httpx_mock.add_response(
        method="POST",
        url="https://openrouter.ai/api/v1/chat/completions",
        json=openai_mock_response,
        status_code=200,
    )

    # Test Albert extractor
    albert_container = _create_isolated_container(PDFExtractorType.ALBERT)
    albert_usecase = albert_container.process_uploaded_cv_usecase()

    pdf_content = create_minimal_valid_pdf()
    filename = "test_cv.pdf"

    albert_result = albert_usecase.execute(filename, pdf_content)
    albert_cv_repo = albert_container.postgres_cv_metadata_repository()
    albert_saved_cv = albert_cv_repo.find_by_id(UUID(albert_result))

    # Test OpenAI extractor
    openai_container = _create_isolated_container(PDFExtractorType.OPENAI)
    openai_usecase = openai_container.process_uploaded_cv_usecase()

    openai_result = openai_usecase.execute(filename, pdf_content)
    openai_cv_repo = openai_container.postgres_cv_metadata_repository()
    openai_saved_cv = openai_cv_repo.find_by_id(UUID(openai_result))

    # Both should have the same structure
    assert isinstance(albert_saved_cv.extracted_text, dict)
    assert isinstance(openai_saved_cv.extracted_text, dict)
    assert "experiences" in albert_saved_cv.extracted_text
    assert "experiences" in openai_saved_cv.extracted_text
    assert len(albert_saved_cv.extracted_text["experiences"]) == 1
    assert len(openai_saved_cv.extracted_text["experiences"]) == 1

    # Both should have extracted the same experience data
    albert_exp = albert_saved_cv.extracted_text["experiences"][0]
    openai_exp = openai_saved_cv.extracted_text["experiences"][0]
    assert albert_exp["title"] == openai_exp["title"]
    assert albert_exp["company"] == openai_exp["company"]
    assert albert_exp["sector"] == openai_exp["sector"]
    assert albert_exp["description"] == openai_exp["description"]
