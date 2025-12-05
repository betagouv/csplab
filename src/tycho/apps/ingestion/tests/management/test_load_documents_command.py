"""Tests for load_documents management command."""

import io
from unittest.mock import Mock, patch

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase

from core.entities.document import DocumentType


class TestLoadDocumentsCommand(TestCase):
    """Test cases for load_documents management command."""

    @patch("apps.ingestion.management.commands.load_documents.get_ingestion_container")
    def test_load_documents_success(self, mock_get_container):
        """Test successful execution of load_documents command."""
        # Mock the container and usecase
        mock_container = Mock()
        mock_usecase = Mock()
        mock_container.load_documents_usecase.return_value = mock_usecase
        mock_get_container.return_value = mock_container

        # Mock successful result
        mock_usecase.execute.return_value = {"created": 15, "updated": 5, "errors": []}

        # Capture stdout
        out = io.StringIO()

        # Execute command
        call_command("load_documents", "--type=CORPS", stdout=out)

        # Verify usecase was called with correct type
        mock_usecase.execute.assert_called_once_with(DocumentType.CORPS)

        # Verify output
        output = out.getvalue()
        self.assertIn("Loading documents of type: CORPS", output)
        self.assertIn("✅ Load completed: 15 created, 5 updated", output)

    @patch("apps.ingestion.management.commands.load_documents.get_ingestion_container")
    def test_load_documents_with_errors(self, mock_get_container):
        """Test load_documents command with errors."""
        # Mock the container and usecase
        mock_container = Mock()
        mock_usecase = Mock()
        mock_container.load_documents_usecase.return_value = mock_usecase
        mock_get_container.return_value = mock_container

        # Mock result with errors
        mock_usecase.execute.return_value = {
            "created": 10,
            "updated": 3,
            "errors": [
                {"entity_id": 123, "error": "Network timeout"},
                {"entity_id": 456, "error": "Invalid data format"},
            ],
        }

        # Capture stdout
        out = io.StringIO()

        # Execute command
        call_command("load_documents", "--type=CORPS", stdout=out)

        # Verify output includes warnings
        output = out.getvalue()
        self.assertIn("✅ Load completed: 10 created, 3 updated", output)
        self.assertIn("⚠️  2 errors occurred", output)

    @patch("apps.ingestion.management.commands.load_documents.get_ingestion_container")
    def test_load_documents_no_errors(self, mock_get_container):
        """Test load_documents command with no errors."""
        # Mock the container and usecase
        mock_container = Mock()
        mock_usecase = Mock()
        mock_container.load_documents_usecase.return_value = mock_usecase
        mock_get_container.return_value = mock_container

        # Mock result with no errors
        mock_usecase.execute.return_value = {"created": 20, "updated": 0, "errors": []}

        # Capture stdout
        out = io.StringIO()

        # Execute command
        call_command("load_documents", "--type=CORPS", stdout=out)

        # Verify output does not include error warnings
        output = out.getvalue()
        self.assertIn("✅ Load completed: 20 created, 0 updated", output)
        self.assertNotIn("⚠️", output)

    def test_load_documents_missing_type_argument(self):
        """Test load_documents command fails without --type argument."""
        with self.assertRaises(SystemExit):
            call_command("load_documents")

    def test_load_documents_invalid_type_argument(self):
        """Test load_documents command fails with invalid --type argument."""
        with self.assertRaises(SystemExit):
            call_command("load_documents", "--type=INVALID")

    @patch("apps.ingestion.management.commands.load_documents.get_ingestion_container")
    def test_load_documents_usecase_exception(self, mock_get_container):
        """Test load_documents command handles usecase exceptions."""
        # Mock the container and usecase to raise exception
        mock_container = Mock()
        mock_usecase = Mock()
        mock_container.load_documents_usecase.return_value = mock_usecase
        mock_get_container.return_value = mock_container

        mock_usecase.execute.side_effect = Exception("API connection failed")

        # Execute command and expect CommandError
        with self.assertRaises(CommandError) as context:
            call_command("load_documents", "--type=CORPS")

        self.assertIn(
            "Failed to load documents: API connection failed",
            str(context.exception),
        )

    @patch("apps.ingestion.management.commands.load_documents.get_ingestion_container")
    def test_load_documents_container_exception(self, mock_get_container):
        """Test load_documents command handles container exceptions."""
        # Mock container to raise exception
        mock_get_container.side_effect = Exception("Container initialization failed")

        # Execute command and expect CommandError
        with self.assertRaises(CommandError) as context:
            call_command("load_documents", "--type=CORPS")

        self.assertIn(
            "Failed to load documents: Container initialization failed",
            str(context.exception),
        )
