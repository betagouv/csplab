"""Unit tests for CleanDocuments usecase.

IMPORTANT: Dependency Injection Override Timing
- Override timing is crucial with dependency-injector
- Always override BEFORE creating the usecase, not after
- Dependencies are resolved at creation time, not execution time
"""

import copy
import json
import unittest
from datetime import datetime
from pathlib import Path
from unittest.mock import Mock

from apps.ingestion.containers import IngestionContainer
from apps.ingestion.infrastructure.adapters.services.logger import LoggerService
from apps.ingestion.tests.utils.in_memory_corps_repository import (
    InMemoryCorpsRepository,
)
from apps.ingestion.tests.utils.in_memory_document_repository import (
    InMemoryDocumentRepository,
)
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

    def _create_isolated_container(self):
        """Create an isolated container for each test to avoid concurrency issues."""
        container = IngestionContainer()

        # Override with test dependencies
        logger_service = LoggerService()
        container.logger_service.override(logger_service)

        # Override with in-memory repositories for unit tests
        in_memory_corps_repo = InMemoryCorpsRepository()
        container.corps_repository.override(in_memory_corps_repo)

        in_memory_document_repo = InMemoryDocumentRepository()
        container.document_repository.override(in_memory_document_repo)

        return container

    def _create_test_documents(
        self, container, raw_data_list, doc_type=DocumentType.CORPS
    ):
        """Helper to create test documents and load them into repository."""
        repository = container.document_repository()
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

    def test_clean_documents_with_empty_repository(self):
        """Test cleaning when no documents exist returns zero statistics."""
        container = self._create_isolated_container()
        clean_documents_usecase = container.clean_documents_usecase()

        result = clean_documents_usecase.execute(DocumentType.CORPS)

        self.assertEqual(result["processed"], 0)
        self.assertEqual(result["cleaned"], 0)
        self.assertEqual(result["created"], 0)
        self.assertEqual(result["updated"], 0)
        self.assertEqual(result["errors"], 0)

    def test_clean_corps_documents_filters_non_fpe_data(self):
        """Test that non-FPE corps data is properly filtered out."""
        container = self._create_isolated_container()
        clean_documents_usecase = container.clean_documents_usecase()

        # Create mixed data: 1 valid FPE + 1 invalid FPT
        valid_corps_data = copy.deepcopy(self.raw_corps_documents[0])
        invalid_corps_data = copy.deepcopy(self.raw_corps_documents[1])
        invalid_corps_data["corpsOuPseudoCorps"]["caracteristiques"][
            "natureFonctionPublique"
        ]["libelleNatureFoncPub"] = "FPT"

        self._create_test_documents(container, [valid_corps_data, invalid_corps_data])

        result = clean_documents_usecase.execute(DocumentType.CORPS)

        self.assertEqual(result["processed"], 2)
        self.assertEqual(result["cleaned"], 1)
        self.assertEqual(result["created"], 1)
        self.assertEqual(result["updated"], 0)
        self.assertEqual(result["errors"], 0)

    def test_clean_corps_documents_filters_non_civil_servants(self):
        """Test that non-civil servants are properly filtered out."""
        container = self._create_isolated_container()
        clean_documents_usecase = container.clean_documents_usecase()

        valid_corps_data = copy.deepcopy(self.raw_corps_documents[0])
        invalid_corps_data = copy.deepcopy(self.raw_corps_documents[1])
        invalid_corps_data["corpsOuPseudoCorps"]["caracteristiques"]["population"][
            "libellePopulation"
        ] = "Contractuel"

        self._create_test_documents(container, [valid_corps_data, invalid_corps_data])

        result = clean_documents_usecase.execute(DocumentType.CORPS)

        self.assertEqual(result["processed"], 2)
        self.assertEqual(result["cleaned"], 1)
        self.assertEqual(result["created"], 1)
        self.assertEqual(result["updated"], 0)
        self.assertEqual(result["errors"], 0)

    def test_clean_corps_documents_filters_minarm_ministry(self):
        """Test that MINARM ministry is properly filtered out."""
        container = self._create_isolated_container()
        clean_documents_usecase = container.clean_documents_usecase()

        valid_corps_data = copy.deepcopy(self.raw_corps_documents[0])
        invalid_corps_data = copy.deepcopy(self.raw_corps_documents[1])
        invalid_corps_data["corpsOuPseudoCorps"][
            "ministereEtInstitutionDeLaRepublique"
        ][0]["libelleMinistere"] = "MINARM"

        self._create_test_documents(container, [valid_corps_data, invalid_corps_data])

        result = clean_documents_usecase.execute(DocumentType.CORPS)

        self.assertEqual(result["processed"], 2)
        self.assertEqual(result["cleaned"], 1)
        self.assertEqual(result["created"], 1)
        self.assertEqual(result["updated"], 0)
        self.assertEqual(result["errors"], 0)

        corps_repository = container.corps_repository()
        expected_corps_id = int(self.raw_corps_documents[0]["identifiant"])
        saved_corps = corps_repository.find_by_id(expected_corps_id)

        self.assertIsNotNone(saved_corps)
        self.assertEqual(saved_corps.id, expected_corps_id)
        self.assertIsNotNone(saved_corps.label)
        self.assertIsNotNone(saved_corps.category)

    def test_clean_corps_documents_handles_empty_cleaned_entities(self):
        """Test that empty cleaned entities list is handled correctly."""
        container = self._create_isolated_container()
        clean_documents_usecase = container.clean_documents_usecase()

        invalid_corps_data = copy.deepcopy(self.raw_corps_documents[0])
        invalid_corps_data["corpsOuPseudoCorps"]["caracteristiques"][
            "natureFonctionPublique"
        ]["libelleNatureFoncPub"] = "FPT"

        self._create_test_documents(container, [invalid_corps_data])

        result = clean_documents_usecase.execute(DocumentType.CORPS)

        self.assertEqual(result["processed"], 1)
        self.assertEqual(result["cleaned"], 0)
        self.assertEqual(result["created"], 0)
        self.assertEqual(result["updated"], 0)
        self.assertEqual(result["errors"], 0)

    def test_clean_documents_logs_save_errors_individually(self):
        """Test that save errors are logged individually with correct format."""
        container = self._create_isolated_container()

        valid_corps_data = copy.deepcopy(self.raw_corps_documents[:2])
        self._create_test_documents(container, valid_corps_data)

        # Mock the corps repository to return errors
        mock_repository = Mock()
        mock_repository.upsert_batch.return_value = {
            "created": 0,
            "updated": 0,
            "errors": [
                {"entity_id": 123, "error": "Database connection failed"},
                {"entity_id": 456, "error": "Validation error: invalid code"},
            ],
        }

        # Override BEFORE creating the usecase
        container.corps_repository.override(mock_repository)
        clean_documents_usecase = container.clean_documents_usecase()

        result = clean_documents_usecase.execute(DocumentType.CORPS)

        self.assertEqual(result["errors"], 2)
        self.assertEqual(len(result["error_details"]), 2)
        self.assertEqual(result["error_details"][0]["entity_id"], 123)
        self.assertEqual(result["error_details"][1]["entity_id"], 456)

    def test_clean_documents_with_successful_save_operations(self):
        """Test successful save operations with created and updated counts."""
        container = self._create_isolated_container()

        valid_corps_data = copy.deepcopy(self.raw_corps_documents[:2])
        self._create_test_documents(container, valid_corps_data)

        # Mock the corps repository to return success with mixed results
        mock_repository = Mock()
        mock_repository.upsert_batch.return_value = {
            "created": 1,
            "updated": 1,
            "errors": [],
        }

        # Override BEFORE creating the usecase
        container.corps_repository.override(mock_repository)
        clean_documents_usecase = container.clean_documents_usecase()

        result = clean_documents_usecase.execute(DocumentType.CORPS)

        self.assertEqual(result["processed"], 2)
        self.assertEqual(result["cleaned"], 2)
        self.assertEqual(result["created"], 1)
        self.assertEqual(result["updated"], 1)
        self.assertEqual(result["errors"], 0)
        self.assertEqual(result["error_details"], [])

    def test_clean_documents_logger_initialization(self):
        """Test that logger is properly initialized with correct name."""
        container = self._create_isolated_container()

        # Mock logger to verify it's called with correct parameters
        mock_logger_service = Mock()
        mock_logger = Mock()
        mock_logger_service.get_logger.return_value = mock_logger
        container.logger_service.override(mock_logger_service)

        container.clean_documents_usecase()

        # Verify logger was initialized with correct name
        mock_logger_service.get_logger.assert_called_with(
            "INGESTION::APPLICATION::CleanDocumentsUsecase::execute"
        )

    def test_clean_documents_logs_fetch_and_clean_operations(self):
        """Test that fetch and clean operations are properly logged."""
        container = self._create_isolated_container()

        # Mock logger to capture log calls
        mock_logger_service = Mock()
        mock_logger = Mock()
        mock_logger_service.get_logger.return_value = mock_logger
        container.logger_service.override(mock_logger_service)

        valid_corps_data = copy.deepcopy(self.raw_corps_documents[:1])
        self._create_test_documents(container, valid_corps_data)

        clean_documents_usecase = container.clean_documents_usecase()
        clean_documents_usecase.execute(DocumentType.CORPS)

        # Verify logging calls were made
        self.assertTrue(mock_logger.info.called)
        log_calls = [call.args[0] for call in mock_logger.info.call_args_list]

        # Check that fetch and clean operations were logged
        self.assertTrue(
            any("Fetched" in call and "raw documents" in call for call in log_calls)
        )
        self.assertTrue(
            any("Cleaned" in call and "entities" in call for call in log_calls)
        )
        self.assertTrue(any("Saved entities" in call for call in log_calls))

    def test_clean_documents_logs_detailed_errors(self):
        """Test that detailed error logging works correctly."""
        container = self._create_isolated_container()

        # Mock logger to capture error log calls
        mock_logger_service = Mock()
        mock_logger = Mock()
        mock_logger_service.get_logger.return_value = mock_logger
        container.logger_service.override(mock_logger_service)

        valid_corps_data = copy.deepcopy(self.raw_corps_documents[:1])
        self._create_test_documents(container, valid_corps_data)

        # Mock repository to return errors
        mock_repository = Mock()
        mock_repository.upsert_batch.return_value = {
            "created": 0,
            "updated": 0,
            "errors": [
                {"entity_id": 123, "error": "Database connection failed"},
                {"entity_id": 456, "error": "Validation error"},
            ],
        }

        container.corps_repository.override(mock_repository)
        clean_documents_usecase = container.clean_documents_usecase()

        clean_documents_usecase.execute(DocumentType.CORPS)

        # Verify error logging was called
        self.assertTrue(mock_logger.error.called)
        error_calls = [call.args[0] for call in mock_logger.error.call_args_list]

        # Check that detailed errors were logged
        self.assertTrue(
            any("Failed to save entity 123" in call for call in error_calls)
        )
        self.assertTrue(
            any("Failed to save entity 456" in call for call in error_calls)
        )
