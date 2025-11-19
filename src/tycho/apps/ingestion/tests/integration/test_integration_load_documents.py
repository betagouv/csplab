"""Integration tests for LoadDocuments usecase with external adapters."""

from unittest.mock import Mock

import environ
import pytest
import responses
from django.test import TransactionTestCase

from apps.ingestion.application.usecases.load_documents import LoadDocumentsUsecase
from apps.ingestion.containers import IngestionContainer
from apps.ingestion.infrastructure.adapters.persistence.models.raw_document import (
    RawDocument,
)
from apps.ingestion.tests.factories.ingres_factories import (
    IngresCorpsApiResponseFactory,
)
from core.entities.document import DocumentType
from core.services.http_client import HttpClient
from core.services.logger import LoggerService


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
        self.usecase = LoadDocumentsUsecase(self.container)

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
            oauth_base_url + "/api/oauth/token",
            json={"access_token": "fake_token", "expires_in": 3600},
            status=200,
            content_type="application/json",
        )

        # Mock INGRES API endpoint with empty response
        responses.add(
            responses.GET,
            ingres_base_url + "/CORPS",
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
            oauth_base_url + "/api/oauth/token",
            json={"access_token": "fake_token", "expires_in": 3600},
            status=200,
            content_type="application/json",
        )

        # Mock INGRES API endpoint
        responses.add(
            responses.GET,
            ingres_base_url + "/CORPS",
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

        with self.assertRaises(Exception) as context:
            self.usecase.execute(DocumentType.CORPS)

        self.assertEqual(str(context.exception), "Ingres connection failed")

    # def test_get_by_type_returns_documents_of_correct_type_only(self):
    #     """Test get_by_type returns only documents of the specified type."""
    #     repository = self.container.document_repository()

    #     documents = [
    #         Document(
    #             id=None,
    #             raw_data={"name": "Corps 1"},
    #             type=DocumentType.CORPS,
    #             created_at=datetime.now(),
    #             updated_at=datetime.now(),
    #         ),
    #         Document(
    #             id=None,
    #             raw_data={"name": "Corps 2"},
    #             type=DocumentType.CORPS,
    #             created_at=datetime.now(),
    #             updated_at=datetime.now(),
    #         ),
    #         Document(
    #             id=None,
    #             raw_data={"name": "Exam 1"},
    #             type=DocumentType.CONCOURS,
    #             created_at=datetime.now(),
    #             updated_at=datetime.now(),
    #         ),
    #     ]

    #     repository.upsert_batch(documents)

    #     corps_docs = repository.fetch_by_type(DocumentType.CORPS)
    #     self.assertEqual(len(corps_docs), 2)

    #     for doc in corps_docs:
    #         self.assertEqual(doc.type, DocumentType.CORPS)

    # def test_upsert_creates_new_document(self):
    #     """Test upsert creates a new document when it doesn't exist."""
    #     repository = self.container.document_repository()

    #     document = Document(
    #         id=None,
    #         raw_data={"name": "Test Document"},
    #         type=DocumentType.CORPS,
    #         created_at=datetime.now(),
    #         updated_at=datetime.now(),
    #     )

    #     result = repository.upsert(document)

    #     self.assertIsNotNone(result.id)
    #     self.assertEqual(result.raw_data, {"name": "Test Document"})
    #     self.assertEqual(result.type, DocumentType.CORPS)

    # def test_upsert_batch_returns_correct_counts(self):
    #     """Test upsert_batch returns correct created/updated counts."""
    #     repository = self.container.document_repository()

    #     documents = [
    #         Document(
    #             id=None,
    #             raw_data={"name": "Doc 1"},
    #             type=DocumentType.CORPS,
    #             created_at=datetime.now(),
    #             updated_at=datetime.now(),
    #         ),
    #         Document(
    #             id=None,
    #             raw_data={"name": "Doc 2"},
    #             type=DocumentType.CORPS,
    #             created_at=datetime.now(),
    #             updated_at=datetime.now(),
    #         ),
    #     ]

    #     result = repository.upsert_batch(documents)

    #     self.assertEqual(result["created"], 2)
    #     self.assertEqual(result["updated"], 0)
