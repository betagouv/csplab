"""Integration tests for LoadDocuments usecase with external adapters."""

import os
from unittest.mock import Mock, patch

import pytest
import responses
from django.test import TransactionTestCase
from pydantic import HttpUrl
from rest_framework.test import APITestCase

from apps.ingestion.application.exceptions import LoadDocumentsError
from apps.ingestion.config import IngestionConfig, PisteConfig
from apps.ingestion.containers import IngestionContainer
from apps.ingestion.infrastructure.adapters.external.http_client import HttpClient
from apps.ingestion.infrastructure.adapters.persistence.models.raw_document import (
    RawDocument,
)
from apps.ingestion.tests.factories.ingres_factories import (
    IngresCorpsApiResponseFactory,
)
from apps.shared.config import OpenAIConfig, SharedConfig
from apps.shared.containers import SharedContainer
from apps.shared.infrastructure.adapters.external.logger import LoggerService
from core.entities.document import DocumentType


class TestIntegrationLoadDocumentsUsecase(TransactionTestCase):
    """Integration test cases for LoadDocuments usecase."""

    def setUp(self):
        """Set up container dependencies."""
        # Create shared container and config
        self.shared_container = SharedContainer()
        self.shared_config = SharedConfig(
            openai_config=OpenAIConfig(
                api_key="fake-api-key",
                base_url=HttpUrl("https://fake-base-url.example.com"),
                model="fake-model",
            )
        )
        self.shared_container.config.override(self.shared_config)

        # Create ingestion container
        self.container = IngestionContainer()
        self.ingestion_config = IngestionConfig(
            piste_config=PisteConfig(
                oauth_base_url=HttpUrl("https://fake-piste-oauth.example.com"),
                ingres_base_url=HttpUrl("https://fake-ingres-api.example.com/path"),
                client_id="fake-client-id",
                client_secret="fake-client-secret",  # noqa
            )
        )
        self.container.config.override(self.ingestion_config)
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
            f"{self.ingestion_config.piste.oauth_base_url}api/oauth/token",
            json={"access_token": "fake_token", "expires_in": 3600},
            status=200,
            content_type="application/json",
        )

        # Mock INGRES API endpoint with empty response
        responses.add(
            responses.GET,
            f"{self.ingestion_config.piste.ingres_base_url}/CORPS",
            json={"items": []},
            status=200,
            content_type="application/json",
        )

        result = self.usecase.execute(DocumentType.CORPS)
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
            f"{self.ingestion_config.piste.oauth_base_url}api/oauth/token",
            json={"access_token": "fake_token", "expires_in": 3600},
            status=200,
            content_type="application/json",
        )

        # Mock INGRES API endpoint
        responses.add(
            responses.GET,
            f"{self.ingestion_config.piste.ingres_base_url}/CORPS",
            json={"items": api_data},
            status=200,
            content_type="application/json",
        )

        result = self.usecase.execute(DocumentType.CORPS)
        self.assertEqual(result["created"], 4)
        self.assertEqual(result["updated"], 0)

        # Verify documents are persisted in database
        saved_documents = RawDocument.objects.filter(
            document_type=DocumentType.CORPS.value
        )
        self.assertEqual(saved_documents.count(), 4)

    @pytest.mark.django_db
    def test_execute_handles_repository_error(self):
        """Test execute handles repository errors properly."""
        mock_repo = Mock()
        mock_repo.fetch_by_type.side_effect = Exception("Ingres connection failed")
        self.container.document_repository.override(mock_repo)

        # Create new usecase with mocked repository
        usecase = self.container.load_documents_usecase()

        with self.assertRaises(Exception) as context:
            usecase.execute(DocumentType.CORPS)

        self.assertEqual(str(context.exception), "Ingres connection failed")


class TestIntegrationExceptions(APITestCase):
    """Integration tests for the exception system across all layers."""

    def setUp(self):
        """Set up test environment."""
        self.load_documents_url = "/ingestion/load/"
        self.config = IngestionConfig(
            piste_config=PisteConfig(
                oauth_base_url=HttpUrl("https://fake-piste-oauth.example.com"),
                ingres_base_url=HttpUrl("https://fake-ingres-api.example.com/path"),
                client_id="fake-client-id",
                client_secret="fake-client-secret",  # noqa
            )
        )

    @patch.dict(
        os.environ,
        {
            "TYCHO_PISTE_OAUTH_BASE_URL": "https://fake-piste-oauth.example.com",
            "TYCHO_INGRES_BASE_URL": "https://fake-ingres-api.example.com/path",
            "TYCHO_INGRES_CLIENT_ID": "fake-client-id",
            "TYCHO_INGRES_CLIENT_SECRET": "fake-client-secret",
        },
    )
    def test_domain_error_invalid_document_type(self):
        """Test Domain layer exception with invalid document type."""
        response = self.client.post(
            self.load_documents_url, {"type": "INVALID_TYPE"}, format="json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["status"], "error")
        self.assertEqual(
            response.data["type"],
            "DomainError::DocumentError::InvalidDocumentTypeError",
        )
        self.assertIn("Invalid document type: INVALID_TYPE", response.data["message"])

    @patch.dict(
        os.environ,
        {
            "TYCHO_PISTE_OAUTH_BASE_URL": "https://fake-piste-oauth.example.com",
            "TYCHO_INGRES_BASE_URL": "https://fake-ingres-api.example.com/path",
            "TYCHO_INGRES_CLIENT_ID": "fake-client-id",
            "TYCHO_INGRES_CLIENT_SECRET": "fake-client-secret",
        },
    )
    @responses.activate
    def test_infrastructure_error_ingres_api_failure(self):
        """Test Infrastructure layer exception with INGRES API failure."""
        # Mock successful OAuth
        responses.add(
            responses.POST,
            f"{self.config.piste.oauth_base_url}api/oauth/token",
            json={"access_token": "fake_token", "expires_in": 3600},
            status=200,
        )

        # Mock INGRES API failure
        responses.add(
            responses.GET,
            f"{self.config.piste.ingres_base_url}/CORPS",
            json={"error": "Service unavailable"},
            status=503,
        )

        response = self.client.post(
            self.load_documents_url, {"type": "CORPS"}, format="json"
        )

        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.data["status"], "error")
        self.assertEqual(response.data["type"], "InfrastructureError::ExternalApiError")

    @patch.dict(
        os.environ,
        {
            "TYCHO_PISTE_OAUTH_BASE_URL": "https://fake-piste-oauth.example.com",
            "TYCHO_INGRES_BASE_URL": "https://fake-ingres-api.example.com/path",
            "TYCHO_INGRES_CLIENT_ID": "fake-client-id",
            "TYCHO_INGRES_CLIENT_SECRET": "fake-client-secret",
        },
    )
    @patch(
        "apps.ingestion.application.usecases.load_documents.LoadDocumentsUsecase.execute"
    )
    def test_application_error_usecase_failure(self, mock_execute):
        """Test Application layer exception with use case failure."""
        # Mock use case failure
        mock_execute.side_effect = LoadDocumentsError(
            "Failed to orchestrate document loading", status_code=500
        )

        response = self.client.post(
            self.load_documents_url, {"type": "CORPS"}, format="json"
        )

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.data["status"], "error")
        self.assertEqual(response.data["type"], "ApplicationError::LoadDocumentsError")

    @patch.dict(
        os.environ,
        {
            "TYCHO_PISTE_OAUTH_BASE_URL": "https://fake-piste-oauth.example.com",
            "TYCHO_INGRES_BASE_URL": "https://fake-ingres-api.example.com/path",
            "TYCHO_INGRES_CLIENT_ID": "fake-client-id",
            "TYCHO_INGRES_CLIENT_SECRET": "fake-client-secret",
        },
    )
    @responses.activate
    def test_success_response_format(self):
        """Test successful API response format and content."""
        # Mock successful OAuth
        responses.add(
            responses.POST,
            f"{self.config.piste.oauth_base_url}api/oauth/token",
            json={"access_token": "fake_token", "expires_in": 3600},
            status=200,
        )

        # Mock successful INGRES API with documents
        api_response = IngresCorpsApiResponseFactory.build()
        api_data = [doc.model_dump(mode="json") for doc in api_response.documents]
        responses.add(
            responses.GET,
            f"{self.config.piste.ingres_base_url}/CORPS",
            json={"items": api_data},
            status=200,
        )

        response = self.client.post(
            self.load_documents_url, {"type": "CORPS"}, format="json"
        )

        # Test success response format (covers lines 45-48 in views.py)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["status"], "success")
        self.assertEqual(response.data["document_type"], "CORPS")
        self.assertEqual(response.data["created"], 4)
        self.assertEqual(response.data["updated"], 0)
        self.assertEqual(response.data["message"], "4 documents created, 0 updated")
