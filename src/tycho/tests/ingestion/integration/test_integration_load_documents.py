"""Integration tests for LoadDocuments usecase with external adapters."""

import pytest
import responses
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TransactionTestCase
from pydantic import HttpUrl
from rest_framework.test import APITestCase

from application.ingestion.interfaces.load_documents_input import LoadDocumentsInput
from application.ingestion.interfaces.load_operation_type import LoadOperationType
from domain.entities.document import DocumentType
from infrastructure.di.ingestion.ingestion_container import IngestionContainer
from infrastructure.di.shared.shared_container import SharedContainer
from infrastructure.django_apps.ingestion.models.raw_document import RawDocument
from infrastructure.external_gateways.configs.openai_config import (
    OpenAIConfig,
    OpenAIGatewayConfig,
)
from infrastructure.external_gateways.configs.piste_config import (
    PisteConfig,
    PisteGatewayConfig,
)
from infrastructure.external_gateways.http_client import HttpClient
from infrastructure.external_gateways.logger import LoggerService
from tests.factories.ingres_factories import IngresCorpsApiResponseFactory


class TestIntegrationLoadDocumentsUsecase(TransactionTestCase):
    """Integration test cases for LoadDocuments usecase."""

    def setUp(self):
        """Set up container dependencies."""
        # Create shared container and config
        self.shared_container = SharedContainer()
        self.openai_gateway_config = OpenAIGatewayConfig(
            openai_config=OpenAIConfig(
                api_key="fake-api-key",
                base_url=HttpUrl("https://fake-base-url.example.com"),
                model="fake-model",
            )
        )
        self.shared_container.config.override(self.openai_gateway_config)

        # Create ingestion container
        self.container = IngestionContainer()
        self.piste_gateway_config = PisteGatewayConfig(
            piste_config=PisteConfig(
                oauth_base_url=HttpUrl("https://fake-piste-oauth.example.com"),
                ingres_base_url=HttpUrl("https://fake-ingres-api.example.com/path"),
                client_id="fake-client-id",
                client_secret="fake-client-secret",  # noqa
            )
        )
        self.container.config.override(self.piste_gateway_config)
        self.container.shared_container.override(self.shared_container)

        logger_service = LoggerService()
        self.container.logger_service.override(logger_service)
        http_client = HttpClient()
        self.container.http_client.override(http_client)

        # Use container to create usecase with proper dependency injection
        self.usecase = self.container.load_documents_usecase()

    @pytest.mark.django_db
    @responses.activate
    def test_execute_returns_zero_when_no_documents(self):
        """Test execute returns 0 when repository is empty."""
        # Mock OAuth token endpoint
        responses.add(
            responses.POST,
            f"{self.piste_gateway_config.piste.oauth_base_url}api/oauth/token",
            json={"access_token": "fake_token", "expires_in": 3600},
            status=200,
            content_type="application/json",
        )

        # Mock INGRES API endpoint with empty response
        responses.add(
            responses.GET,
            f"{self.piste_gateway_config.piste.ingres_base_url}/CORPS",
            json={"items": []},
            status=200,
            content_type="application/json",
        )

        input_data = LoadDocumentsInput(
            operation_type=LoadOperationType.FETCH_FROM_API,
            kwargs={"document_type": DocumentType.CORPS},
        )
        result = self.usecase.execute(input_data)
        self.assertEqual(result["created"], 0)
        self.assertEqual(result["updated"], 0)

    @pytest.mark.django_db
    @responses.activate
    def test_execute_returns_correct_count_with_documents(self):
        """Test execute returns correct count when documents exist with mocked API."""
        api_response = IngresCorpsApiResponseFactory.build()
        api_data = [doc.model_dump(mode="json") for doc in api_response.documents]

        # Mock OAuth token endpoint
        responses.add(
            responses.POST,
            f"{self.piste_gateway_config.piste.oauth_base_url}api/oauth/token",
            json={"access_token": "fake_token", "expires_in": 3600},
            status=200,
            content_type="application/json",
        )

        # Mock INGRES API endpoint
        responses.add(
            responses.GET,
            f"{self.piste_gateway_config.piste.ingres_base_url}/CORPS",
            json={"items": api_data},
            status=200,
            content_type="application/json",
        )

        input_data = LoadDocumentsInput(
            operation_type=LoadOperationType.FETCH_FROM_API,
            kwargs={"document_type": DocumentType.CORPS},
        )
        result = self.usecase.execute(input_data)
        self.assertEqual(result["created"], 4)
        self.assertEqual(result["updated"], 0)

        # Verify documents are persisted in database
        saved_documents = RawDocument.objects.filter(
            document_type=DocumentType.CORPS.value
        )
        self.assertEqual(saved_documents.count(), 4)


class TestConcoursUploadView(APITestCase):
    """Integration tests for ConcoursUploadView."""

    def setUp(self):
        """Set up test environment."""
        self.concours_upload_url = "/ingestion/concours/upload/"

    def _create_valid_csv_content(self):
        """Create valid CSV content for testing."""
        return (
            "N° NOR;Ministère;Catégorie;Corps;"
            "Grade;Année de référence;Nb postes total\n"
            "INTB2400001C;Ministère de l'Intérieur;A;Attaché;Attaché;2024;10\n"
            "INTB2400002C;Ministère de l'Intérieur;B;Secrétaire;Secrétaire;2024;5\n"
        )

    def _create_invalid_csv_content(self):
        """Create invalid CSV content for testing."""
        return (
            "N° NOR;Ministère;Catégorie;Corps;Grade;"
            "Année de référence;Nb postes total\n"
            ";Ministère de l'Intérieur;A;Attaché;Attaché;2024;10\n"  # Missing NOR
            "INTB2400002C;;B;Secrétaire;Secrétaire;2024;5\n"  # Missing Ministère
        )

    def _create_csv_file(self, content, filename="test.csv"):
        """Create a temporary CSV file for testing."""
        return SimpleUploadedFile(
            filename, content.encode("utf-8"), content_type="text/csv"
        )

    def test_no_file_provided(self):
        """Test error when no file is provided."""
        response = self.client.post(self.concours_upload_url, {}, format="multipart")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["error"], "No file provided")

    def test_invalid_file_format(self):
        """Test error when file is not CSV."""
        txt_file = SimpleUploadedFile(
            "test.txt", b"not a csv file", content_type="text/plain"
        )

        response = self.client.post(
            self.concours_upload_url, {"file": txt_file}, format="multipart"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["error"], "File must be a CSV")

    def test_validation_errors(self):
        """Test handling of validation errors in CSV data."""
        invalid_csv = self._create_csv_file(self._create_invalid_csv_content())

        response = self.client.post(
            self.concours_upload_url, {"file": invalid_csv}, format="multipart"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["error"], "No valid rows found")
        self.assertIn("validation_errors", response.data)
        self.assertEqual(len(response.data["validation_errors"]), 2)

    def test_success_response(self):
        """Test successful CSV upload and processing."""
        valid_csv = self._create_csv_file(self._create_valid_csv_content())

        response = self.client.post(
            self.concours_upload_url, {"file": valid_csv}, format="multipart"
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["status"], "success")
        self.assertEqual(response.data["total_rows"], 2)
        self.assertEqual(response.data["valid_rows"], 2)
        self.assertEqual(response.data["invalid_rows"], 0)
        self.assertIn(
            "Successfully processed 2 valid concours records", response.data["message"]
        )
