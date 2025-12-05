"""Tests for clean_documents management command."""

import io
from unittest.mock import Mock, patch

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase

from core.entities.document import DocumentType


class TestCleanDocumentsCommand(TestCase):
    """Test cases for clean_documents management command."""

    @patch("apps.ingestion.management.commands.clean_documents.get_ingestion_container")
    def test_clean_documents_success(self, mock_get_container):
        """Test successful execution of clean_documents command."""
        # Mock the container and usecase
        mock_container = Mock()
        mock_usecase = Mock()
        mock_container.clean_documents_usecase.return_value = mock_usecase
        mock_get_container.return_value = mock_container

        # Mock successful result
        mock_usecase.execute.return_value = {
            "processed": 10,
            "cleaned": 8,
            "created": 5,
            "updated": 3,
            "errors": 0,
            "error_details": [],
        }

        # Capture stdout
        out = io.StringIO()

        # Execute command
        call_command("clean_documents", "--type=CORPS", stdout=out)

        # Verify usecase was called with correct type
        mock_usecase.execute.assert_called_once_with(DocumentType.CORPS)

        # Verify output
        output = out.getvalue()
        self.assertIn("Cleaning documents of type: CORPS", output)
        self.assertIn("✅ Clean completed: 8/10documents cleaned", output)

    @patch("apps.ingestion.management.commands.clean_documents.get_ingestion_container")
    def test_clean_documents_with_errors(self, mock_get_container):
        """Test clean_documents command with errors."""
        # Mock the container and usecase
        mock_container = Mock()
        mock_usecase = Mock()
        mock_container.clean_documents_usecase.return_value = mock_usecase
        mock_get_container.return_value = mock_container

        # Mock result with errors
        mock_usecase.execute.return_value = {
            "processed": 5,
            "cleaned": 3,
            "created": 2,
            "updated": 1,
            "errors": 2,
            "error_details": [
                {"entity_id": 123, "error": "Database error"},
                {"entity_id": 456, "error": "Validation error"},
            ],
        }

        # Capture stdout
        out = io.StringIO()

        # Execute command
        call_command("clean_documents", "--type=CORPS", stdout=out)

        # Verify output includes warnings and error details
        output = out.getvalue()
        self.assertIn("⚠️  2 errors occurred", output)
        self.assertIn("Error details:", output)
        self.assertIn("Entity 123: Database error", output)
        self.assertIn("Entity 456: Validation error", output)

    def test_clean_documents_missing_type_argument(self):
        """Test clean_documents command fails without --type argument."""
        with self.assertRaises(SystemExit):
            call_command("clean_documents")

    def test_clean_documents_invalid_type_argument(self):
        """Test clean_documents command fails with invalid --type argument."""
        with self.assertRaises(SystemExit):
            call_command("clean_documents", "--type=INVALID")

    @patch("apps.ingestion.management.commands.clean_documents.get_ingestion_container")
    def test_clean_documents_usecase_exception(self, mock_get_container):
        """Test clean_documents command handles usecase exceptions."""
        # Mock the container and usecase to raise exception
        mock_container = Mock()
        mock_usecase = Mock()
        mock_container.clean_documents_usecase.return_value = mock_usecase
        mock_get_container.return_value = mock_container

        mock_usecase.execute.side_effect = Exception("Database connection failed")

        # Execute command and expect CommandError
        with self.assertRaises(CommandError) as context:
            call_command("clean_documents", "--type=CORPS")

        self.assertIn(
            "Failed to clean documents: Database connection failed",
            str(context.exception),
        )

    @patch("apps.ingestion.management.commands.clean_documents.get_ingestion_container")
    def test_clean_documents_container_exception(self, mock_get_container):
        """Test clean_documents command handles container exceptions."""
        # Mock container to raise exception
        mock_get_container.side_effect = Exception("Container initialization failed")

        # Execute command and expect CommandError
        with self.assertRaises(CommandError) as context:
            call_command("clean_documents", "--type=CORPS")

        self.assertIn(
            "Failed to clean documents: Container initialization failed",
            str(context.exception),
        )
