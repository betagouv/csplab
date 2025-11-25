"""Unit tests for CleanDocuments usecase."""

import json
import unittest
from datetime import datetime
from pathlib import Path

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
        # Setup container with in-memory mode
        self.container = IngestionContainer()
        self.container.in_memory_mode.override("in_memory")

        # Setup logger
        logger_service = LoggerService()
        self.container.logger_service.override(logger_service)

        # Pre-load raw documents into in-memory repository
        repository = self.container.document_repository()
        documents = []
        for doc in self.raw_corps_documents:
            document = Document(
                id=None,
                raw_data=doc,
                type=DocumentType.CORPS,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
            documents.append(document)

        # Load documents using LoadDocumentsUsecase
        repository.upsert_batch(documents)
        self.load_documents_usecase = self.container.load_documents_usecase()
        self.load_documents_usecase.execute(DocumentType.CORPS)
        self.clean_documents_usecase = self.container.clean_documents_usecase()

    def tearDown(self):
        """Clean up after each test."""
        repository = self.container.document_repository()
        repository.clear()

    def test_clean_documents(self):
        """Test that CleanDocumentsUsecase can be created with dependencies."""
        result = self.clean_documents_usecase.execute(DocumentType.CORPS)

        self.assertEqual(result["processed"], 4, "Should have processed 4 documents")
        self.assertEqual(result["cleaned"], 4, "Should have cleaned 4 documents")
