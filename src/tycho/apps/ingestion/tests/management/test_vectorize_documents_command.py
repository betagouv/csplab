"""Tests for vectorize_documents management command."""

import io
from unittest.mock import Mock, patch

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase

from core.entities.document import DocumentType


class TestVectorizeDocumentsCommand(TestCase):
    """Test cases for vectorize_documents management command."""

    @patch(
        "apps.ingestion.management.commands.vectorize_documents.get_ingestion_container"
    )
    def test_vectorize_documents_success(self, mock_get_container):
        """Test successful execution of vectorize_documents command."""
        # Mock the container, repository factory, repository and usecase
        mock_container = Mock()
        mock_repository_factory = Mock()
        mock_repository = Mock()
        mock_usecase = Mock()

        mock_container.repository_factory.return_value = mock_repository_factory
        mock_repository_factory.get_repository.return_value = mock_repository
        mock_container.vectorize_documents_usecase.return_value = mock_usecase
        mock_get_container.return_value = mock_container

        # Mock entities from repository
        mock_entities = [Mock(), Mock(), Mock()]
        mock_repository.get_all.return_value = mock_entities

        # Mock successful result
        mock_usecase.execute.return_value = {
            "processed": 3,
            "vectorized": 3,
            "errors": 0,
            "error_details": [],
        }

        # Capture stdout
        out = io.StringIO()

        # Execute command
        call_command("vectorize_documents", "--type=CORPS", stdout=out)

        # Verify repository factory was called with correct type
        mock_repository_factory.get_repository.assert_called_once_with(
            DocumentType.CORPS
        )

        # Verify repository get_all was called
        mock_repository.get_all.assert_called_once()

        # Verify usecase was called with entities
        mock_usecase.execute.assert_called_once_with(mock_entities)

        # Verify output
        output = out.getvalue()
        self.assertIn("Fetching all entities of type: CORPS", output)
        self.assertIn("Vectorizing 3 entities...", output)
        self.assertIn("✅ Completed: 3/3documents vectorized", output)

    @patch(
        "apps.ingestion.management.commands.vectorize_documents.get_ingestion_container"
    )
    def test_vectorize_documents_with_limit(self, mock_get_container):
        """Test vectorize_documents command with --limit argument."""
        # Mock the container, repository factory, repository and usecase
        mock_container = Mock()
        mock_repository_factory = Mock()
        mock_repository = Mock()
        mock_usecase = Mock()

        mock_container.repository_factory.return_value = mock_repository_factory
        mock_repository_factory.get_repository.return_value = mock_repository
        mock_container.vectorize_documents_usecase.return_value = mock_usecase
        mock_get_container.return_value = mock_container

        # Mock entities from repository (more than limit)
        mock_entities = [Mock() for _ in range(10)]
        mock_repository.get_all.return_value = mock_entities

        # Mock successful result
        mock_usecase.execute.return_value = {
            "processed": 5,
            "vectorized": 5,
            "errors": 0,
            "error_details": [],
        }

        # Capture stdout
        out = io.StringIO()

        # Execute command with limit
        call_command("vectorize_documents", "--type=CORPS", "--limit=5", stdout=out)

        # Verify usecase was called with limited entities
        mock_usecase.execute.assert_called_once_with(mock_entities[:5])

        # Verify output
        output = out.getvalue()
        self.assertIn("Fetching 5 entities of type: CORPS", output)
        self.assertIn("Vectorizing 5 entities...", output)

    @patch(
        "apps.ingestion.management.commands.vectorize_documents.get_ingestion_container"
    )
    def test_vectorize_documents_no_entities(self, mock_get_container):
        """Test vectorize_documents command when no entities are found."""
        # Mock the container, repository factory, repository
        mock_container = Mock()
        mock_repository_factory = Mock()
        mock_repository = Mock()

        mock_container.repository_factory.return_value = mock_repository_factory
        mock_repository_factory.get_repository.return_value = mock_repository
        mock_get_container.return_value = mock_container

        # Mock empty entities list
        mock_repository.get_all.return_value = []

        # Capture stdout
        out = io.StringIO()

        # Execute command
        call_command("vectorize_documents", "--type=CORPS", stdout=out)

        # Verify output shows warning
        output = out.getvalue()
        self.assertIn("No entities found for type: CORPS", output)

    @patch(
        "apps.ingestion.management.commands.vectorize_documents.get_ingestion_container"
    )
    def test_vectorize_documents_with_errors(self, mock_get_container):
        """Test vectorize_documents command with errors."""
        # Mock the container, repository factory, repository and usecase
        mock_container = Mock()
        mock_repository_factory = Mock()
        mock_repository = Mock()
        mock_usecase = Mock()

        mock_container.repository_factory.return_value = mock_repository_factory
        mock_repository_factory.get_repository.return_value = mock_repository
        mock_container.vectorize_documents_usecase.return_value = mock_usecase
        mock_get_container.return_value = mock_container

        # Mock entities from repository
        mock_entities = [Mock(), Mock()]
        mock_repository.get_all.return_value = mock_entities

        # Mock result with errors
        mock_usecase.execute.return_value = {
            "processed": 2,
            "vectorized": 1,
            "errors": 1,
            "error_details": [
                {"source_type": "Corps", "source_id": 123, "error": "Embedding failed"}
            ],
        }

        # Capture stdout
        out = io.StringIO()

        # Execute command
        call_command("vectorize_documents", "--type=CORPS", stdout=out)

        # Verify output includes warnings and error details
        output = out.getvalue()
        self.assertIn("✅ Completed: 1/2documents vectorized", output)
        self.assertIn("⚠️  1 errors occurred", output)
        self.assertIn("Error details:", output)
        self.assertIn("Corps 123:Embedding failed", output)

    def test_vectorize_documents_missing_type_argument(self):
        """Test vectorize_documents command fails without --type argument."""
        with self.assertRaises(SystemExit):
            call_command("vectorize_documents")

    def test_vectorize_documents_invalid_type_argument(self):
        """Test vectorize_documents command fails with invalid --type argument."""
        with self.assertRaises(SystemExit):
            call_command("vectorize_documents", "--type=INVALID")

    @patch(
        "apps.ingestion.management.commands.vectorize_documents.get_ingestion_container"
    )
    def test_vectorize_documents_usecase_exception(self, mock_get_container):
        """Test vectorize_documents command handles usecase exceptions."""
        # Mock the container, repository factory, repository and usecase
        mock_container = Mock()
        mock_repository_factory = Mock()
        mock_repository = Mock()
        mock_usecase = Mock()

        mock_container.repository_factory.return_value = mock_repository_factory
        mock_repository_factory.get_repository.return_value = mock_repository
        mock_container.vectorize_documents_usecase.return_value = mock_usecase
        mock_get_container.return_value = mock_container

        # Mock entities from repository
        mock_entities = [Mock()]
        mock_repository.get_all.return_value = mock_entities

        # Mock usecase to raise exception
        mock_usecase.execute.side_effect = Exception("Embedding service unavailable")

        # Execute command and expect CommandError
        with self.assertRaises(CommandError) as context:
            call_command("vectorize_documents", "--type=CORPS")

        self.assertIn(
            "Failed to vectorize documents: Embedding service unavailable",
            str(context.exception),
        )

    @patch(
        "apps.ingestion.management.commands.vectorize_documents.get_ingestion_container"
    )
    def test_vectorize_documents_container_exception(self, mock_get_container):
        """Test vectorize_documents command handles container exceptions."""
        # Mock container to raise exception
        mock_get_container.side_effect = Exception("Container initialization failed")

        # Execute command and expect CommandError
        with self.assertRaises(CommandError) as context:
            call_command("vectorize_documents", "--type=CORPS")

        self.assertIn(
            "Failed to vectorize documents: Container initialization failed",
            str(context.exception),
        )

    @patch(
        "apps.ingestion.management.commands.vectorize_documents.get_ingestion_container"
    )
    def test_vectorize_documents_repository_exception(self, mock_get_container):
        """Test vectorize_documents command handles repository exceptions."""
        # Mock the container, repository factory, repository
        mock_container = Mock()
        mock_repository_factory = Mock()
        mock_repository = Mock()

        mock_container.repository_factory.return_value = mock_repository_factory
        mock_repository_factory.get_repository.return_value = mock_repository
        mock_get_container.return_value = mock_container

        # Mock repository to raise exception
        mock_repository.get_all.side_effect = Exception("Database connection failed")

        # Execute command and expect CommandError
        with self.assertRaises(CommandError) as context:
            call_command("vectorize_documents", "--type=CORPS")

        self.assertIn(
            "Failed to vectorize documents: Database connection failed",
            str(context.exception),
        )
