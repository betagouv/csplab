"""Unit test cases for LoadDocuments usecase."""

import json
import unittest
from datetime import datetime
from pathlib import Path
from unittest.mock import Mock

from apps.ingestion.containers import IngestionContainer
from apps.ingestion.infrastructure.adapters.services.logger import LoggerService
from core.entities.document import Document, DocumentType


class TestUnitLoadDocumentsUsecase(unittest.TestCase):
    """Unit test cases for LoadDocuments usecase."""

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
        """Set up dependencies."""
        self.container = IngestionContainer()
        self.container.in_memory_mode.override("in_memory")

        logger_service = LoggerService()
        self.container.logger_service.override(logger_service)

        # Use container to create usecase with proper dependency injection
        self.usecase = self.container.load_documents_usecase()

    def tearDown(self):
        """Clean up after each test."""
        repository = self.container.document_repository()
        repository.clear()

    def test_execute_returns_zero_when_no_documents(self):
        """Test execute returns 0 when repository is empty."""
        result = self.usecase.execute(DocumentType.CORPS)
        self.assertEqual(result["created"], 0)
        self.assertEqual(result["updated"], 0)

    def test_execute_returns_correct_count_with_documents(self):
        """Test execute returns correct count when documents exist."""
        repository = self.container.document_repository()

        # preload data in repository
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

        repository.upsert_batch(documents)

        # now we execute usecase
        result = self.usecase.execute(DocumentType.CORPS)

        # in memory, same repo for fetch and persistence
        # Correction : fixture allégée contient 4 documents, pas 680
        self.assertEqual(result["updated"], 4)

    def test_execute_handles_repository_error(self):
        """Test execute handles repository errors properly."""
        mock_repo = Mock()
        mock_repo.fetch_by_type.side_effect = Exception("Database connection failed")
        self.container.document_repository.override(mock_repo)

        # Create new usecase with mocked repository
        usecase = self.container.load_documents_usecase()

        with self.assertRaises(Exception) as context:
            usecase.execute(DocumentType.CORPS)

        self.assertEqual(str(context.exception), "Database connection failed")

    def test_get_by_type_returns_documents_of_correct_type_only(self):
        """Test get_by_type returns only documents of the specified type."""
        repository = self.container.document_repository()

        documents = [
            Document(
                id=None,
                raw_data={"name": "Corps 1"},
                type=DocumentType.CORPS,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            ),
            Document(
                id=None,
                raw_data={"name": "Corps 2"},
                type=DocumentType.CORPS,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            ),
            Document(
                id=None,
                raw_data={"name": "Exam 1"},
                type=DocumentType.CONCOURS,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            ),
        ]

        repository.upsert_batch(documents)

        corps_docs = repository.fetch_by_type(DocumentType.CORPS)
        self.assertEqual(len(corps_docs), 2)

        for doc in corps_docs:
            self.assertEqual(doc.type, DocumentType.CORPS)

    def test_upsert_creates_new_document(self):
        """Test upsert creates a new document when it doesn't exist."""
        repository = self.container.document_repository()

        document = Document(
            id=None,
            raw_data={"name": "Test Document"},
            type=DocumentType.CORPS,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        result = repository.upsert(document)

        self.assertIsNotNone(result.id)
        self.assertEqual(result.raw_data, {"name": "Test Document"})
        self.assertEqual(result.type, DocumentType.CORPS)

    def test_upsert_batch_returns_correct_counts(self):
        """Test upsert_batch returns correct created/updated counts."""
        repository = self.container.document_repository()

        documents = [
            Document(
                id=None,
                raw_data={"name": "Doc 1"},
                type=DocumentType.CORPS,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            ),
            Document(
                id=None,
                raw_data={"name": "Doc 2"},
                type=DocumentType.CORPS,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            ),
        ]

        result = repository.upsert_batch(documents)

        self.assertEqual(result["created"], 2)
        self.assertEqual(result["updated"], 0)
