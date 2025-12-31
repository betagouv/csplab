"""Unit test cases for LoadDocuments usecase.

IMPORTANT: Dependency Injection Override Timing
- Override timing is crucial with dependency-injector
- Always override BEFORE creating the usecase, not after
- Dependencies are resolved at creation time, not execution time
"""

import copy
import unittest
from datetime import datetime

from application.ingestion.interfaces.load_documents_input import (
    LoadDocumentsInput,
)
from application.ingestion.interfaces.load_operation_type import LoadOperationType
from application.ingestion.services import (
    load_documents_strategy_factory,
)
from apps.ingestion.containers import IngestionContainer
from apps.shared.infrastructure.adapters.external.logger import LoggerService
from domain.entities.document import Document, DocumentType
from tests.fixtures.fixture_loader import load_fixture
from tests.utils.in_memory_document_repository import (
    InMemoryDocumentRepository,
)


class TestUnitLoadDocumentsUsecase(unittest.TestCase):
    """Unit test cases for LoadDocuments usecase."""

    @classmethod
    def setUpClass(cls):
        """Load fixtures once for all tests."""
        cls.raw_corps_documents = load_fixture("corps_ingres_20251117.json")

    def _create_isolated_container(self):
        """Create an isolated container for each test to avoid concurrency issues."""
        container = IngestionContainer()

        # Override with test dependencies
        logger_service = LoggerService()
        container.logger_service.override(logger_service)

        # Override with in-memory repository for unit tests
        in_memory_document_repo = InMemoryDocumentRepository()
        container.document_repository.override(in_memory_document_repo)

        # Create real factory with the same in-memory repository as document_fetcher
        test_factory = load_documents_strategy_factory.LoadDocumentsStrategyFactory(
            document_fetcher=in_memory_document_repo
        )
        container.load_documents_strategy_factory.override(test_factory)

        return container

    def _create_test_documents(
        self, container, raw_data_list, doc_type=DocumentType.CORPS
    ):
        """Helper to create test documents and load them into repository."""
        repository = container.document_repository()
        documents = []

        for _, _raw_data in enumerate(raw_data_list):
            document = Document(
                id=None,
                external_id="test_doc",
                raw_data={"test": "data"},
                type=DocumentType.CORPS,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
            documents.append(document)

        repository.upsert_batch(documents)
        return documents

    def test_execute_returns_zero_when_no_documents(self):
        """Test execute returns 0 when repository is empty."""
        container = self._create_isolated_container()
        usecase = container.load_documents_usecase()

        input_data = LoadDocumentsInput(
            operation_type=LoadOperationType.FETCH_FROM_API,
            kwargs={"document_type": DocumentType.CORPS},
        )
        result = usecase.execute(input_data)
        self.assertEqual(result["created"], 0)
        self.assertEqual(result["updated"], 0)

    def test_execute_returns_correct_count_with_documents(self):
        """Test execute returns correct count when documents exist."""
        container = self._create_isolated_container()
        usecase = container.load_documents_usecase()

        raw_data = copy.deepcopy(self.raw_corps_documents)
        self._create_test_documents(container, raw_data)

        input_data = LoadDocumentsInput(
            operation_type=LoadOperationType.FETCH_FROM_API,
            kwargs={"document_type": DocumentType.CORPS},
        )
        result = usecase.execute(input_data)
        self.assertEqual(result["updated"], 4)

    def test_get_by_type_returns_documents_of_correct_type_only(self):
        """Test get_by_type returns only documents of the specified type."""
        container = self._create_isolated_container()
        repository = container.document_repository()

        documents = [
            Document(
                id=None,
                external_id="corps_1",
                raw_data={"name": "Corps 1"},
                type=DocumentType.CORPS,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            ),
            Document(
                id=None,
                external_id="corps_2",
                raw_data={"name": "Corps 2"},
                type=DocumentType.CORPS,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            ),
            Document(
                id=None,
                external_id="exam_1",
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

    def test_upsert_batch_creates_new_document(self):
        """Test upsert_batch creates a new document when it doesn't exist."""
        container = self._create_isolated_container()
        repository = container.document_repository()

        document = Document(
            id=None,
            external_id="test_document",
            raw_data={"name": "Test Document"},
            type=DocumentType.CORPS,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        result = repository.upsert_batch([document])

        self.assertEqual(result["created"], 1)
        self.assertEqual(result["updated"], 0)
        self.assertEqual(len(result["errors"]), 0)

        # Verify document was created
        docs = repository.fetch_by_type(DocumentType.CORPS)
        self.assertEqual(len(docs), 1)
        self.assertEqual(docs[0].raw_data, {"name": "Test Document"})

    def test_upsert_batch_returns_correct_counts(self):
        """Test upsert_batch returns correct created/updated counts."""
        container = self._create_isolated_container()
        repository = container.document_repository()

        documents = [
            Document(
                id=None,
                external_id="doc_1",
                raw_data={"name": "Doc 1"},
                type=DocumentType.CORPS,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            ),
            Document(
                id=None,
                external_id="doc_2",
                raw_data={"name": "Doc 2"},
                type=DocumentType.CORPS,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            ),
        ]

        result = repository.upsert_batch(documents)

        self.assertEqual(result["created"], 2)
        self.assertEqual(result["updated"], 0)

    def test_execute_returns_correct_count_with_documents_with_data_input(self):
        """Test execute returns correct count when documents exist with CSV upload."""
        container = self._create_isolated_container()
        usecase = container.load_documents_usecase()

        raw_data = copy.deepcopy(self.raw_corps_documents)
        documents = self._create_test_documents(container, raw_data)

        input_data = LoadDocumentsInput(
            operation_type=LoadOperationType.UPLOAD_FROM_CSV,
            kwargs={"documents": documents},
        )
        result = usecase.execute(input_data)
        self.assertEqual(result["created"], 4)
