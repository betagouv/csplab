"""Integration tests for ProcessUploadedCVUsecase with Django persistence."""

from datetime import datetime
from uuid import UUID

import pytest
import responses
from django.test import TransactionTestCase
from pydantic import HttpUrl

from apps.candidate.config import AlbertConfig, CandidateConfig
from apps.candidate.containers import CandidateContainer
from apps.candidate.infrastructure.adapters.persistence.models.cv_metadata import (
    CVMetadataModel,
)
from apps.shared.infrastructure.exceptions import ExternalApiError
from domain.entities.cv_metadata import CVMetadata
from domain.exceptions.cv_errors import InvalidPDFError, TextExtractionError
from infrastructure.external_services.logger import LoggerService


class TestIntegrationProcessUploadedCVUsecase(TransactionTestCase):
    """Integration test cases for ProcessUploadedCVUsecase with Django persistence."""

    def setUp(self):
        """Set up container dependencies with real Django persistence."""
        self.container = CandidateContainer()

        albert_config = AlbertConfig(
            api_base_url=HttpUrl("https://albert.api.etalab.gouv.fr/"),
            api_key="test-api-key",
            model_name="albert-large",
            dpi=200,
        )
        candidate_config = CandidateConfig(albert_config)
        self.container.config.override(candidate_config)

        logger_service = LoggerService()
        self.container.logger_service.override(logger_service)

        self.usecase = self.container.process_uploaded_cv_usecase()

    @pytest.mark.django_db
    @responses.activate
    def test_execute_with_valid_pdf_saves_to_database(self):
        """Test that valid PDF is processed and saved to real database."""
        # Mock Albert API response
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

        pdf_content = b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n1 0 obj\n<<"
        "\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj"
        filename = "integration_test_cv.pdf"

        result = self.usecase.execute(filename, pdf_content)

        self.assertIsInstance(result, str)
        cv_id = UUID(result)

        cv_model = CVMetadataModel.objects.get(id=cv_id)
        self.assertEqual(cv_model.filename, filename)
        self.assertEqual(cv_model.extracted_text, mock_response)
        self.assertIn("software engineer", cv_model.search_query)
        self.assertIsInstance(cv_model.created_at, datetime)

        cv_entity = cv_model.to_entity()
        self.assertIsInstance(cv_entity, CVMetadata)
        self.assertEqual(cv_entity.id, cv_id)
        self.assertEqual(cv_entity.filename, filename)
        self.assertEqual(cv_entity.extracted_text, mock_response)

    @pytest.mark.django_db
    def test_execute_with_invalid_pdf_does_not_save_to_database(self):
        """Test that invalid PDF raises error and doesn't save to database."""
        pdf_content = b"This is not a PDF file"
        filename = "invalid.pdf"

        initial_count = CVMetadataModel.objects.count()

        with self.assertRaises(InvalidPDFError):
            self.usecase.execute(filename, pdf_content)

        final_count = CVMetadataModel.objects.count()
        self.assertEqual(initial_count, final_count)

    @pytest.mark.django_db
    @responses.activate
    def test_execute_with_albert_api_failure_does_not_save_to_database(self):
        """Test that Albert API failure raises error and doesn't save to database."""
        responses.add(
            responses.POST,
            "https://albert.api.etalab.gouv.fr/v1/ocr-beta",
            json={"error": "API Error"},
            status=500,
            content_type="application/json",
        )

        pdf_content = b"%PDF-1.4\nvalid content"
        filename = "test.pdf"

        initial_count = CVMetadataModel.objects.count()

        with self.assertRaises(ExternalApiError):
            self.usecase.execute(filename, pdf_content)

        final_count = CVMetadataModel.objects.count()
        self.assertEqual(initial_count, final_count)

    @pytest.mark.django_db
    @responses.activate
    def test_execute_with_empty_experiences_does_not_save_to_database(self):
        """Test that empty experiences raises error and doesn't save to database."""
        mock_response = {"experiences": []}

        responses.add(
            responses.POST,
            "https://albert.api.etalab.gouv.fr/v1/ocr-beta",
            json=mock_response,
            status=200,
            content_type="application/json",
        )

        pdf_content = b"%PDF-1.4\nvalid content"
        filename = "empty_experiences.pdf"

        initial_count = CVMetadataModel.objects.count()

        with self.assertRaises(TextExtractionError):
            self.usecase.execute(filename, pdf_content)

        final_count = CVMetadataModel.objects.count()
        self.assertEqual(initial_count, final_count)

    @pytest.mark.django_db
    @responses.activate
    def test_multiple_cv_processing_creates_separate_records(self):
        """Test that multiple CV processing creates separate database records."""
        mock_response = {
            "experiences": [
                {
                    "title": "Data Scientist",
                    "company": "AI Corp",
                    "sector": "AI",
                    "description": "3 years in machine learning",
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

        pdf_content = b"%PDF-1.4\nvalid content"

        initial_count = CVMetadataModel.objects.count()

        result1 = self.usecase.execute("cv1.pdf", pdf_content)
        cv_id1 = UUID(result1)

        responses.add(
            responses.POST,
            "https://albert.api.etalab.gouv.fr/v1/ocr-beta",
            json=mock_response,
            status=200,
            content_type="application/json",
        )
        result2 = self.usecase.execute("cv2.pdf", pdf_content)
        cv_id2 = UUID(result2)

        final_count = CVMetadataModel.objects.count()
        self.assertEqual(final_count, initial_count + 2)

        self.assertNotEqual(cv_id1, cv_id2)

        cv1_model = CVMetadataModel.objects.get(id=cv_id1)
        cv2_model = CVMetadataModel.objects.get(id=cv_id2)

        self.assertEqual(cv1_model.filename, "cv1.pdf")
        self.assertEqual(cv2_model.filename, "cv2.pdf")
        self.assertEqual(cv1_model.extracted_text, mock_response)
        self.assertEqual(cv2_model.extracted_text, mock_response)
