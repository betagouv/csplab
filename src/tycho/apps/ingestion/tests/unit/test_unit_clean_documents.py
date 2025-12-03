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
        document_repository = self.container.document_repository()
        document_repository.clear()

        corps_repository = self.container.corps_repository()
        corps_repository.clear()

    def test_clean_documents_with_empty_repository(self):
        """Test cleaning when no documents exist returns zero statistics."""
        result = self.clean_documents_usecase.execute(DocumentType.CORPS)

        self.assertEqual(result["processed"], 0)
        self.assertEqual(result["cleaned"], 0)
        self.assertEqual(result["created"], 0)
        self.assertEqual(result["updated"], 0)
        self.assertEqual(result["errors"], 0)

    def test_clean_corps_documents_filters_non_fpe_data(self):
        """Test that non-FPE corps data is properly filtered out."""
        # Create mixed data: 1 valid FPE + 1 invalid FPT
        valid_corps_data = self.raw_corps_documents[0].copy()
        invalid_corps_data = self.raw_corps_documents[1].copy()
        invalid_corps_data["corpsOuPseudoCorps"]["caracteristiques"][
            "natureFonctionPublique"
        ]["libelleNatureFoncPub"] = "FPT"

        self._create_test_documents([valid_corps_data, invalid_corps_data])

        result = self.clean_documents_usecase.execute(DocumentType.CORPS)

        self.assertEqual(result["processed"], 2)
        self.assertEqual(result["cleaned"], 1)
        self.assertEqual(result["created"], 1)
        self.assertEqual(result["updated"], 0)
        self.assertEqual(result["errors"], 0)

    def test_clean_corps_documents_filters_non_civil_servants(self):
        """Test that non-civil servants are properly filtered out."""
        valid_corps_data = self.raw_corps_documents[0].copy()
        invalid_corps_data = self.raw_corps_documents[1].copy()
        invalid_corps_data["corpsOuPseudoCorps"]["caracteristiques"]["population"][
            "libellePopulation"
        ] = "Contractuel"

        self._create_test_documents([valid_corps_data, invalid_corps_data])

        result = self.clean_documents_usecase.execute(DocumentType.CORPS)

        self.assertEqual(result["processed"], 2)
        self.assertEqual(result["cleaned"], 1)
        self.assertEqual(result["created"], 1)
        self.assertEqual(result["updated"], 0)
        self.assertEqual(result["errors"], 0)

    def test_clean_corps_documents_filters_minarm_ministry(self):
        """Test that MINARM ministry is properly filtered out."""
        valid_corps_data = self.raw_corps_documents[0].copy()
        invalid_corps_data = self.raw_corps_documents[1].copy()
        invalid_corps_data["corpsOuPseudoCorps"][
            "ministereEtInstitutionDeLaRepublique"
        ][0]["libelleMinistere"] = "MINARM"

        self._create_test_documents([valid_corps_data, invalid_corps_data])

        result = self.clean_documents_usecase.execute(DocumentType.CORPS)

        self.assertEqual(result["processed"], 2)
        self.assertEqual(result["cleaned"], 1)
        self.assertEqual(result["created"], 1)
        self.assertEqual(result["updated"], 0)
        self.assertEqual(result["errors"], 0)

        # Verify that saved entity can be retrieved by ID
        corps_repository = self.container.corps_repository()
        expected_corps_id = int(self.raw_corps_documents[0]["identifiant"])
        saved_corps = corps_repository.find_by_id(expected_corps_id)

        self.assertIsNotNone(saved_corps)
        self.assertEqual(saved_corps.id, expected_corps_id)
        self.assertIsNotNone(saved_corps.label)
        self.assertIsNotNone(saved_corps.category)

    def test_clean_corps_documents_handles_empty_cleaned_entities(self):
        """Test that empty cleaned entities list is handled correctly."""
        # Create documents that will all be filtered out
        invalid_corps_data = self.raw_corps_documents[0].copy()
        invalid_corps_data["corpsOuPseudoCorps"]["caracteristiques"][
            "natureFonctionPublique"
        ]["libelleNatureFoncPub"] = "FPT"

        self._create_test_documents([invalid_corps_data])

        result = self.clean_documents_usecase.execute(DocumentType.CORPS)

        self.assertEqual(result["processed"], 1)
        self.assertEqual(result["cleaned"], 0)
        self.assertEqual(result["created"], 0)
        self.assertEqual(result["updated"], 0)
        self.assertEqual(result["errors"], 0)
