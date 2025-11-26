"""Integration tests for LoadDocuments usecase with external adapters."""

from unittest.mock import Mock, patch

import environ
import pytest
import responses
from django.test import TransactionTestCase
from rest_framework.test import APITestCase

from apps.ingestion.containers import IngestionContainer
from apps.ingestion.infrastructure.adapters.persistence.models.raw_document import (
    RawDocument,
)
from apps.ingestion.infrastructure.adapters.services.http_client import HttpClient
from apps.ingestion.infrastructure.adapters.services.logger import LoggerService
from apps.ingestion.infrastructure.exceptions import ExternalApiError
from apps.ingestion.tests.factories.ingres_factories import (
    IngresCorpsApiResponseFactory,
)
from core.entities.document import DocumentType


class TestIntegrationLoadDocumentsUsecase(TransactionTestCase):
    """Integration test cases for LoadDocuments usecase."""

    def setUp(self):
        """Set up container dependencies."""
        self.container = IngestionContainer()
        self.container.in_memory_mode.override("external")

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
        env = environ.Env()
        oauth_base_url = env.str("TYCHO_PISTE_OAUTH_BASE_URL")
        ingres_base_url = env.str("TYCHO_INGRES_BASE_URL")

        # Mock OAuth token endpoint
        responses.add(
            responses.POST,
            f"{oauth_base_url}/api/oauth/token",
            json={"access_token": "fake_token", "expires_in": 3600},
            status=200,
            content_type="application/json",
        )

        # Mock INGRES API endpoint with empty response
        responses.add(
            responses.GET,
            f"{ingres_base_url}/CORPS",
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
        env = environ.Env()
        oauth_base_url = env.str("TYCHO_PISTE_OAUTH_BASE_URL")
        ingres_base_url = env.str("TYCHO_INGRES_BASE_URL")

        # Mock OAuth token endpoint
        responses.add(
            responses.POST,
            f"{oauth_base_url}/api/oauth/token",
            json={"access_token": "fake_token", "expires_in": 3600},
            status=200,
            content_type="application/json",
        )

        # Mock INGRES API endpoint
        responses.add(
            responses.GET,
            f"{ingres_base_url}/CORPS",
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

    def test_domain_error_invalid_document_type(self):
        """Test Domain layer exception with invalid document type."""
        response = self.client.post(
            self.load_documents_url, {"type": "INVALID_TYPE"}, format="json"
        )

        self.assertEqual(response.status_code, 400)

    @patch(
        "apps.ingestion.infrastructure.adapters.external.piste_client.PisteClient._get_token"
    )
    def test_infrastructure_error_oauth_failure(self, mock_get_token):
        """Test Infrastructure layer exception with OAuth failure."""
        # Mock OAuth failure
        mock_get_token.side_effect = ExternalApiError(
            "OAuth authentication failed", status_code=401, api_name="PISTE"
        )

        response = self.client.post(
            self.load_documents_url, {"type": "CORPS"}, format="json"
        )

        self.assertEqual(response.status_code, 401)

    @responses.activate
    def test_infrastructure_error_ingres_api_failure(self):
        """Test Infrastructure layer exception with INGRES API failure."""
        env = environ.Env()
        oauth_base_url = env.str("TYCHO_PISTE_OAUTH_BASE_URL")
        ingres_base_url = env.str("TYCHO_INGRES_BASE_URL")

        # Mock successful OAuth
        responses.add(
            responses.POST,
            f"{oauth_base_url}/api/oauth/token",
            json={"access_token": "fake_token", "expires_in": 3600},
            status=200,
        )

        # Mock INGRES API failure
        responses.add(
            responses.GET,
            f"{ingres_base_url}/CORPS",
            json={"error": "Service unavailable"},
            status=503,
        )

        response = self.client.post(
            self.load_documents_url, {"type": "CORPS"}, format="json"
        )

        self.assertEqual(response.status_code, 503)

    @responses.activate
    def test_success_response_format(self):
        """Test successful API response format and content."""
        env = environ.Env()
        oauth_base_url = env.str("TYCHO_PISTE_OAUTH_BASE_URL")
        ingres_base_url = env.str("TYCHO_INGRES_BASE_URL")

        # Mock successful OAuth
        responses.add(
            responses.POST,
            f"{oauth_base_url}/api/oauth/token",
            json={"access_token": "fake_token", "expires_in": 3600},
            status=200,
        )

        # Mock successful INGRES API with documents
        api_response = IngresCorpsApiResponseFactory.build()
        api_data = [doc.model_dump(mode="json") for doc in api_response.documents]
        responses.add(
            responses.GET,
            f"{ingres_base_url}/CORPS",
            json={"items": api_data},
            status=200,
        )

        response = self.client.post(
            self.load_documents_url, {"type": "CORPS"}, format="json"
        )

        self.assertEqual(response.status_code, 200)
