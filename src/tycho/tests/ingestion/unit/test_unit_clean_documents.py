"""Unit tests for CleanDocuments usecase.

IMPORTANT: Dependency Injection Override Timing
- Override timing is crucial with dependency-injector
- Always override BEFORE creating the usecase, not after
- Dependencies are resolved at creation time, not execution time
"""

import copy
import unittest
from datetime import datetime
from unittest.mock import Mock

from apps.ingestion.containers import IngestionContainer
from domain.entities.document import Document, DocumentType
from domain.exceptions.document_error import InvalidDocumentTypeError
from infrastructure.external_services.logger import LoggerService
from tests.fixtures.fixture_loader import load_fixture
from tests.utils.in_memory_concours_repository import InMemoryConcoursRepository
from tests.utils.in_memory_corps_repository import InMemoryCorpsRepository
from tests.utils.in_memory_document_repository import InMemoryDocumentRepository

REFERENCE_YEAR = 2024


class TestUnitCleanDocumentsUsecase(unittest.TestCase):
    """Unit tests for CleanDocuments usecase."""

    @classmethod
    def setUpClass(cls):
        """Load fixtures once for all tests."""
        cls.raw_corps_documents = load_fixture("corps_ingres_20251117.json")
        cls.raw_concours_documents = load_fixture("concours_greco_2025.json")

    def _create_isolated_container(self):
        """Create an isolated container for each test to avoid concurrency issues."""
        container = IngestionContainer()

        logger_service = LoggerService()
        container.logger_service.override(logger_service)

        in_memory_corps_repo = InMemoryCorpsRepository()
        container.corps_repository.override(in_memory_corps_repo)

        in_memory_concours_repo = InMemoryConcoursRepository()
        container.concours_repository.override(in_memory_concours_repo)

        in_memory_document_repo = InMemoryDocumentRepository()
        container.document_persister.override(in_memory_document_repo)

        return container

    def _create_test_documents(
        self, container, raw_data_list, doc_type=DocumentType.CORPS
    ):
        """Helper to create test documents and load them into repository."""
        repository = container.document_persister()
        documents = []

        for i, raw_data in enumerate(raw_data_list):
            document = Document(
                id=i + 1,
                external_id=f"test_{i + 1}",
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

    def test_clean_concours_documents_with_empty_repository(self):
        """Test cleaning CONCOURS when no documents exist returns zero statistics."""
        container = self._create_isolated_container()
        clean_documents_usecase = container.clean_documents_usecase()

        result = clean_documents_usecase.execute(DocumentType.CONCOURS)

        self.assertEqual(result["processed"], 0)
        self.assertEqual(result["cleaned"], 0)
        self.assertEqual(result["created"], 0)
        self.assertEqual(result["updated"], 0)
        self.assertEqual(result["errors"], 0)

    def test_clean_concours_documents_filters_invalid_status(self):
        """Test that CONCOURS with invalid status are filtered out."""
        container = self._create_isolated_container()
        clean_documents_usecase = container.clean_documents_usecase()

        valid_concours = [
            doc for doc in self.raw_concours_documents if doc["Statut"] == "VALIDE"
        ][:2]
        invalid_concours = [
            doc for doc in self.raw_concours_documents if doc["Statut"] == "INVALIDE"
        ][:1]

        test_data = valid_concours + invalid_concours
        self._create_test_documents(container, test_data, DocumentType.CONCOURS)

        result = clean_documents_usecase.execute(DocumentType.CONCOURS)

        self.assertEqual(result["processed"], 3)
        self.assertEqual(result["cleaned"], 2)

    def test_clean_concours_documents_filters_old_year(self):
        """Test that CONCOURS with year <= 2024 are filtered out."""
        container = self._create_isolated_container()
        clean_documents_usecase = container.clean_documents_usecase()
        new_concours = [
            doc
            for doc in self.raw_concours_documents
            if doc["Année de référence"] > REFERENCE_YEAR
        ][:2]
        old_concours = [
            doc
            for doc in self.raw_concours_documents
            if doc["Année de référence"] <= REFERENCE_YEAR
        ][:1]

        test_data = new_concours + old_concours
        self._create_test_documents(container, test_data, DocumentType.CONCOURS)

        result = clean_documents_usecase.execute(DocumentType.CONCOURS)

        self.assertEqual(result["processed"], 3)
        self.assertEqual(result["cleaned"], 2)

    def test_clean_concours_documents_filters_missing_required_fields(self):
        """Test that CONCOURS with missing required fields are filtered out."""
        container = self._create_isolated_container()
        clean_documents_usecase = container.clean_documents_usecase()

        valid_concours = copy.deepcopy(self.raw_concours_documents[0])
        invalid_concours = copy.deepcopy(self.raw_concours_documents[1])
        invalid_concours["N° NOR"] = None

        test_data = [valid_concours, invalid_concours]
        self._create_test_documents(container, test_data, DocumentType.CONCOURS)

        result = clean_documents_usecase.execute(DocumentType.CONCOURS)

        self.assertEqual(result["processed"], 2)
        self.assertEqual(result["cleaned"], 1)

    def test_clean_concours_documents_successful_processing(self):
        """Test successful CONCOURS processing with valid data."""
        container = self._create_isolated_container()
        clean_documents_usecase = container.clean_documents_usecase()

        valid_concours = [
            doc
            for doc in self.raw_concours_documents
            if doc["Statut"] == "VALIDE" and doc["Année de référence"] > REFERENCE_YEAR
        ][:2]

        self._create_test_documents(container, valid_concours, DocumentType.CONCOURS)

        result = clean_documents_usecase.execute(DocumentType.CONCOURS)

        self.assertEqual(result["processed"], 2)
        self.assertEqual(result["cleaned"], 2)
        self.assertEqual(result["created"], 2)
        self.assertEqual(result["updated"], 0)
        self.assertEqual(result["errors"], 0)

        concours_repository = container.concours_repository()
        saved_concours = concours_repository.get_all()
        self.assertEqual(len(saved_concours), 2)

    def test_clean_concours_documents_handles_processing_errors(self):
        """Test that CONCOURS processing errors are handled correctly."""
        container = self._create_isolated_container()

        valid_concours = [
            doc
            for doc in self.raw_concours_documents
            if doc["Statut"] == "VALIDE" and doc["Année de référence"] > REFERENCE_YEAR
        ][:2]
        self._create_test_documents(container, valid_concours, DocumentType.CONCOURS)

        mock_repository = Mock()
        mock_repository.upsert_batch.return_value = {
            "created": 0,
            "updated": 0,
            "errors": [
                {"entity_id": 1, "error": "Invalid NOR format"},
                {"entity_id": 2, "error": "Missing ministry mapping"},
            ],
        }

        container.concours_repository.override(mock_repository)
        clean_documents_usecase = container.clean_documents_usecase()

        result = clean_documents_usecase.execute(DocumentType.CONCOURS)

        self.assertEqual(result["processed"], 2)
        self.assertEqual(result["cleaned"], 2)
        self.assertEqual(result["created"], 0)
        self.assertEqual(result["updated"], 0)
        self.assertEqual(result["errors"], 2)
        self.assertEqual(len(result["error_details"]), 2)

    def test_execute_raises_error_for_unsupported_document_type(self):
        """Test that InvalidDocumentTypeError is raised."""
        container = self._create_isolated_container()

        grade_data = {"test": "data"}
        self._create_test_documents(container, [grade_data], DocumentType.GRADE)

        mock_cleaner = Mock()
        mock_cleaner.clean.return_value = [Mock()]  # Return fake entities
        container.document_cleaner.override(mock_cleaner)

        clean_documents_usecase = container.clean_documents_usecase()

        with self.assertRaises(InvalidDocumentTypeError) as context:
            clean_documents_usecase.execute(DocumentType.GRADE)

        self.assertIn("GRADE", str(context.exception))
