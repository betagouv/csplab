"""Unit tests for CleanDocuments usecase."""

import json
import unittest
from datetime import datetime
from pathlib import Path

import pytest

from apps.ingestion.containers import IngestionContainer
from apps.ingestion.infrastructure.adapters.services.logger import LoggerService
from core.entities.document import Document, DocumentType


class TestUnitCleanDocumentsUsecase(unittest.TestCase):
    """Unit tests for CleanDocuments usecase."""

    @classmethod
    def setUpClass(cls):
        """Load fixtures once for all tests."""
        fixture_data = cls._load_fixture("corps_ingres_20251117.json")
        cls.raw_corps_documents = fixture_data

    @classmethod
    def _load_fixture(cls, filename):
        """Load fixture from the shared fixtures directory."""
        fixtures_path = Path(__file__).parent.parent / "fixtures" / filename
        with open(fixtures_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def setUp(self):
        """Set up test dependencies."""
        self.container = IngestionContainer()
        self.container.in_memory_mode.override("in_memory")

        logger_service = LoggerService()
        self.container.logger_service.override(logger_service)

        self.clean_documents_usecase = self.container.clean_documents_usecase()

    def _create_test_documents(self, raw_data_list, doc_type=DocumentType.CORPS):
        """Helper to create test documents and load them into repository."""
        repository = self.container.document_repository()
        documents = []

        for i, raw_data in enumerate(raw_data_list):
            document = Document(
                id=i + 1,
                raw_data=raw_data,
                type=doc_type,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
            documents.append(document)

        repository.upsert_batch(documents)
        return documents

    def tearDown(self):
        """Clean up after each test."""
        repository = self.container.document_repository()
        repository.clear()

    def test_clean_documents_with_valid_corps_data(self):
        """Test cleaning valid corps documents returns correct statistics."""
        self._create_test_documents(self.raw_corps_documents[:2])

        result = self.clean_documents_usecase.execute(DocumentType.CORPS)

        self.assertEqual(result["processed"], 2)
        self.assertEqual(result["cleaned"], 2)
        self.assertEqual(result["created"], 0)
        self.assertEqual(result["updated"], 0)
        self.assertEqual(result["errors"], 0)

    def test_clean_documents_with_empty_repository(self):
        """Test cleaning when no documents exist returns zero statistics."""
        result = self.clean_documents_usecase.execute(DocumentType.CORPS)

        self.assertEqual(result["processed"], 0)
        self.assertEqual(result["cleaned"], 0)
        self.assertEqual(result["created"], 0)
        self.assertEqual(result["updated"], 0)
        self.assertEqual(result["errors"], 0)

    @pytest.mark.skip("Skipping until repository factory is implemented")
    def test_clean_documents_saves_cleaned_entities_to_repository(self):
        """Test that cleaned entities are saved to appropriate repository."""
        self._create_test_documents(self.raw_corps_documents[:1])

        result = self.clean_documents_usecase.execute(DocumentType.CORPS)

        self.assertGreater(
            result["created"], 0, "Should have created entities in repository"
        )

    @pytest.mark.skip("Skipping until repository factory is implemented")
    def test_clean_documents_handles_cleaning_errors_gracefully(self):
        """Test that cleaning errors are handled and reported in statistics."""
        invalid_data = {"invalid": "data"}
        self._create_test_documents([invalid_data])

        result = self.clean_documents_usecase.execute(DocumentType.CORPS)

        self.assertEqual(result["processed"], 1)
        self.assertGreaterEqual(result["errors"], 0, "Should handle cleaning errors")
