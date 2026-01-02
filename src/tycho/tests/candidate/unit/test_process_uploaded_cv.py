"""Unit test cases for ProcessUploadedCVUsecase."""

import unittest
from datetime import datetime
from unittest.mock import Mock
from uuid import UUID

import responses
from pydantic import HttpUrl

from apps.candidate.config import AlbertConfig, CandidateConfig
from apps.candidate.containers import CandidateContainer
from domain.exceptions.cv_errors import (
    InvalidPDFError,
    TextExtractionError,
)
from infrastructure.external_services.logger import LoggerService
from tests.utils.in_memory_cv_metadata_repository import (
    InMemoryCVMetadataRepository,
)


class TestProcessUploadedCVUsecase(unittest.TestCase):
    """Unit test cases for ProcessUploadedCVUsecase."""

    def _create_isolated_container(self):
        """Create an isolated container for each test to avoid concurrency issues."""
        container = CandidateContainer()

        logger_service = LoggerService()
        container.logger_service.override(logger_service)

        in_memory_cv_repo = InMemoryCVMetadataRepository()
        container.cv_metadata_repository.override(in_memory_cv_repo)

        # Configure Albert for tests
        albert_config = AlbertConfig(
            api_base_url=HttpUrl("https://albert.api.etalab.gouv.fr"),
            api_key="test-api-key",
            model_name="albert-large",
            dpi=200,
        )
        candidate_config = CandidateConfig(albert_config)
        container.config.override(candidate_config)

        return container

    @responses.activate
    def test_execute_with_valid_pdf_returns_cv_id(self):
        """Test that a valid PDF is processed successfully and returns CV ID."""
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

        container = self._create_isolated_container()
        usecase = container.process_uploaded_cv_usecase()

        pdf_content = b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n1 0 obj\n<<"
        "\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj"
        filename = "test_cv.pdf"

        result = usecase.execute(filename, pdf_content)

        self.assertIsInstance(result, str)
        cv_id = UUID(result)

        cv_repo = container.cv_metadata_repository()
        self.assertEqual(cv_repo.count(), 1)

        saved_cv = cv_repo.find_by_id(cv_id)
        self.assertIsNotNone(saved_cv)
        self.assertEqual(saved_cv.filename, filename)
        self.assertIsInstance(saved_cv.extracted_text, dict)
        self.assertIn("experiences", saved_cv.extracted_text)
        self.assertEqual(len(saved_cv.extracted_text["experiences"]), 1)
        self.assertIsInstance(saved_cv.created_at, datetime)

    def test_execute_with_invalid_pdf_raises_invalid_pdf_error(self):
        """Test that invalid PDF content raises InvalidPDFError."""
        container = self._create_isolated_container()
        usecase = container.process_uploaded_cv_usecase()

        pdf_content = b"This is not a PDF file"
        filename = "invalid.pdf"

        with self.assertRaises(InvalidPDFError) as context:
            usecase.execute(filename, pdf_content)

        self.assertEqual(context.exception.filename, filename)
        cv_repo = container.cv_metadata_repository()
        self.assertEqual(cv_repo.count(), 0)

    def test_execute_with_empty_pdf_raises_invalid_pdf_error(self):
        """Test that empty PDF content raises InvalidPDFError."""
        container = self._create_isolated_container()
        usecase = container.process_uploaded_cv_usecase()

        pdf_content = b""
        filename = "empty.pdf"

        with self.assertRaises(InvalidPDFError) as context:
            usecase.execute(filename, pdf_content)

        self.assertEqual(context.exception.filename, filename)
        cv_repo = container.cv_metadata_repository()
        self.assertEqual(cv_repo.count(), 0)

    def test_execute_with_oversized_pdf_raises_invalid_pdf_error(self):
        """Test that oversized PDF raises InvalidPDFError."""
        container = self._create_isolated_container()
        usecase = container.process_uploaded_cv_usecase()

        large_content = b"%PDF-1.4\n" + b"x" * (6 * 1024 * 1024)  # 6MB
        filename = "large.pdf"

        with self.assertRaises(InvalidPDFError) as context:
            usecase.execute(filename, large_content)

        self.assertEqual(context.exception.filename, filename)
        cv_repo = container.cv_metadata_repository()
        self.assertEqual(cv_repo.count(), 0)

    def test_execute_with_empty_extracted_text_raises_text_extraction_error(self):
        """Test that empty extracted text raises TextExtractionError."""
        container = self._create_isolated_container()

        mock_extractor = Mock()
        mock_extractor.validate_pdf.return_value = True
        mock_extractor.extract_text.return_value = {
            "experiences": []
        }  # Empty structured content
        container.pdf_text_extractor.override(mock_extractor)

        usecase = container.process_uploaded_cv_usecase()

        pdf_content = b"%PDF-1.4\nvalid content"
        filename = "empty_text.pdf"

        with self.assertRaises(TextExtractionError) as context:
            usecase.execute(filename, pdf_content)

        self.assertEqual(context.exception.filename, filename)
        self.assertIn("No structured content found", context.exception.reason)
        cv_repo = container.cv_metadata_repository()
        self.assertEqual(cv_repo.count(), 0)

    def test_query_builder_extracts_keywords_correctly(self):
        """Test that query builder extracts keywords from CV structured data."""
        container = self._create_isolated_container()
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
        self.assertIn("software engineer", result)

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
        self.assertIn("project manager", result)

        cv_data = {"experiences": []}
        result = query_builder.build_query(cv_data)
        self.assertEqual(result, "")

    def test_pdf_text_extractor_validates_correctly(self):
        """Test that PDF text extractor validates PDF files correctly."""
        container = self._create_isolated_container()
        extractor = container.pdf_text_extractor()

        valid_pdf = b"%PDF-1.4\ncontent"
        self.assertTrue(extractor.validate_pdf(valid_pdf))

        invalid_pdf = b"Not a PDF"
        self.assertFalse(extractor.validate_pdf(invalid_pdf))

        self.assertFalse(extractor.validate_pdf(b""))

        large_pdf = b"%PDF-1.4\n" + b"x" * (6 * 1024 * 1024)  # 6MB
        self.assertFalse(extractor.validate_pdf(large_pdf))
