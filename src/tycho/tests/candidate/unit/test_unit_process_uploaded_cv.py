"""Unit test cases for ProcessUploadedCVUsecase."""

import json
from datetime import datetime
from uuid import UUID

import pytest

from domain.exceptions.cv_errors import InvalidPDFError
from tests.utils.pdf_test_utils import create_large_pdf, create_minimal_valid_pdf

# Test constants
EXPECTED_EXPERIENCES_COUNT = 1
EXPECTED_SKILLS_COUNT = 2


@pytest.mark.asyncio
async def test_execute_with_valid_pdf_returns_cv_id_albert(
    httpx_mock, process_cv_usecase, candidate_container, mock_api_responses, pdf_content
):
    """Test that a valid PDF is processed successfully with Albert extractor."""
    httpx_mock.add_response(
        method="POST",
        url="https://albert.api.etalab.gouv.fr/v1/ocr-beta",
        json=mock_api_responses["albert"],
        status_code=200,
    )

    filename = "test_cv.pdf"
    result = await process_cv_usecase.execute(filename, pdf_content)

    assert isinstance(result, str)
    cv_id = UUID(result)

    cv_repo = candidate_container.postgres_cv_metadata_repository()
    assert cv_repo.count() == 1

    saved_cv = cv_repo.find_by_id(cv_id)
    assert saved_cv is not None
    assert saved_cv.filename == filename
    assert isinstance(saved_cv.extracted_text, dict)
    assert "experiences" in saved_cv.extracted_text
    assert "skills" in saved_cv.extracted_text
    assert len(saved_cv.extracted_text["experiences"]) == EXPECTED_EXPERIENCES_COUNT
    assert len(saved_cv.extracted_text["skills"]) == EXPECTED_SKILLS_COUNT
    assert isinstance(saved_cv.created_at, datetime)


@pytest.mark.asyncio
async def test_execute_with_valid_pdf_returns_cv_id_openai(
    httpx_mock,
    openai_process_cv_usecase,
    openai_candidate_container,
    mock_api_responses,
    pdf_content,
):
    """Test that a valid PDF is processed successfully with OpenAI extractor."""
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

    filename = "test_cv.pdf"
    result = await openai_process_cv_usecase.execute(filename, pdf_content)

    assert isinstance(result, str)
    cv_id = UUID(result)

    cv_repo = openai_candidate_container.postgres_cv_metadata_repository()
    assert cv_repo.count() == 1

    saved_cv = cv_repo.find_by_id(cv_id)
    assert saved_cv is not None
    assert saved_cv.filename == filename
    assert isinstance(saved_cv.extracted_text, dict)
    assert "experiences" in saved_cv.extracted_text
    assert "skills" in saved_cv.extracted_text
    assert len(saved_cv.extracted_text["experiences"]) == EXPECTED_EXPERIENCES_COUNT
    assert len(saved_cv.extracted_text["skills"]) == EXPECTED_SKILLS_COUNT
    assert isinstance(saved_cv.created_at, datetime)


@pytest.mark.asyncio
async def test_execute_with_invalid_pdf_raises_invalid_pdf_error_albert(
    process_cv_usecase, candidate_container
):
    """Test that invalid PDF content raises InvalidPDFError with Albert extractor."""
    pdf_content = b"This is not a PDF file"
    filename = "invalid.pdf"

    with pytest.raises(InvalidPDFError) as exc_info:
        await process_cv_usecase.execute(filename, pdf_content)

    assert exc_info.value.filename == filename
    cv_repo = candidate_container.postgres_cv_metadata_repository()
    assert cv_repo.count() == 0


@pytest.mark.asyncio
async def test_execute_with_invalid_pdf_raises_invalid_pdf_error_openai(
    openai_process_cv_usecase, openai_candidate_container
):
    """Test that invalid PDF content raises InvalidPDFError with OpenAI extractor."""
    pdf_content = b"This is not a PDF file"
    filename = "invalid.pdf"

    with pytest.raises(InvalidPDFError) as exc_info:
        await openai_process_cv_usecase.execute(filename, pdf_content)

    assert exc_info.value.filename == filename
    cv_repo = openai_candidate_container.postgres_cv_metadata_repository()
    assert cv_repo.count() == 0


@pytest.mark.asyncio
async def test_execute_with_empty_pdf_raises_invalid_pdf_error_albert(
    process_cv_usecase, candidate_container
):
    """Test that empty PDF content raises InvalidPDFError with Albert extractor."""
    pdf_content = b""
    filename = "empty.pdf"

    with pytest.raises(InvalidPDFError) as exc_info:
        await process_cv_usecase.execute(filename, pdf_content)

    assert exc_info.value.filename == filename
    cv_repo = candidate_container.postgres_cv_metadata_repository()
    assert cv_repo.count() == 0


@pytest.mark.asyncio
async def test_execute_with_empty_pdf_raises_invalid_pdf_error_openai(
    openai_process_cv_usecase, openai_candidate_container
):
    """Test that empty PDF content raises InvalidPDFError with OpenAI extractor."""
    pdf_content = b""
    filename = "empty.pdf"

    with pytest.raises(InvalidPDFError) as exc_info:
        await openai_process_cv_usecase.execute(filename, pdf_content)

    assert exc_info.value.filename == filename
    cv_repo = openai_candidate_container.postgres_cv_metadata_repository()
    assert cv_repo.count() == 0


def test_query_builder_extracts_keywords_correctly(candidate_container):
    """Test that query builder extracts keywords from CV structured data."""
    query_builder = candidate_container.query_builder()

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


def test_both_extractors_validate_pdf_consistently(
    candidate_container, openai_candidate_container
):
    """Test that both extractors validate PDFs consistently."""
    albert_extractor = candidate_container.pdf_text_extractor()
    openai_extractor = openai_candidate_container.pdf_text_extractor()

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


@pytest.mark.asyncio
async def test_both_extractors_process_same_pdf_consistently(
    httpx_mock,
    candidate_container,
    openai_candidate_container,
    mock_api_responses,
    pdf_content,
):
    """Test that both extractors process the same PDF consistently."""
    httpx_mock.add_response(
        method="POST",
        url="https://albert.api.etalab.gouv.fr/v1/ocr-beta",
        json=mock_api_responses["albert"],
        status_code=200,
    )

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

    # Test Albert extractor
    albert_usecase = candidate_container.process_uploaded_cv_usecase()
    filename = "test_cv.pdf"

    albert_result = await albert_usecase.execute(filename, pdf_content)
    albert_cv_repo = candidate_container.postgres_cv_metadata_repository()
    albert_saved_cv = albert_cv_repo.find_by_id(UUID(albert_result))

    # Test OpenAI extractor
    openai_usecase = openai_candidate_container.process_uploaded_cv_usecase()

    openai_result = await openai_usecase.execute(filename, pdf_content)
    openai_cv_repo = openai_candidate_container.postgres_cv_metadata_repository()
    openai_saved_cv = openai_cv_repo.find_by_id(UUID(openai_result))

    # Both should have the same structure
    assert isinstance(albert_saved_cv.extracted_text, dict)
    assert isinstance(openai_saved_cv.extracted_text, dict)
    assert "experiences" in albert_saved_cv.extracted_text
    assert "experiences" in openai_saved_cv.extracted_text
    assert "skills" in albert_saved_cv.extracted_text
    assert "skills" in openai_saved_cv.extracted_text
    assert (
        len(albert_saved_cv.extracted_text["experiences"]) == EXPECTED_EXPERIENCES_COUNT
    )
    assert (
        len(openai_saved_cv.extracted_text["experiences"]) == EXPECTED_EXPERIENCES_COUNT
    )
    assert len(albert_saved_cv.extracted_text["skills"]) == EXPECTED_SKILLS_COUNT
    assert len(openai_saved_cv.extracted_text["skills"]) == EXPECTED_SKILLS_COUNT

    # Both should have extracted the same experience data
    albert_exp = albert_saved_cv.extracted_text["experiences"][0]
    openai_exp = openai_saved_cv.extracted_text["experiences"][0]
    assert albert_exp["title"] == openai_exp["title"]
    assert albert_exp["company"] == openai_exp["company"]
    assert albert_exp["sector"] == openai_exp["sector"]
    assert albert_exp["description"] == openai_exp["description"]
