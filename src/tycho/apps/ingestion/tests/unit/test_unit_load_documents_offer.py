"""Unit test cases for LoadDocuments usecase with OFFER documents."""

import copy
import unittest
from datetime import datetime

from apps.ingestion.application.interfaces.load_documents_input import (
    LoadDocumentsInput,
)
from apps.ingestion.application.interfaces.load_operation_type import LoadOperationType
from apps.ingestion.containers import IngestionContainer
from apps.ingestion.infrastructure.adapters.services import (
    load_documents_strategy_factory,
)
from apps.ingestion.tests.utils.in_memory_document_repository import (
    InMemoryDocumentRepository,
)
from apps.shared.infrastructure.adapters.external.logger import LoggerService
from apps.shared.tests.fixtures.fixture_loader import load_fixture
from core.entities.document import Document, DocumentType


class TestUnitLoadDocumentsOfferUsecase(unittest.TestCase):
    """Unit test cases for LoadDocuments usecase with OFFER documents."""

    @classmethod
    def setUpClass(cls):
        """Load fixtures once for all tests."""
        cls.raw_offer_documents = load_fixture("offers_talentsoft_mock.json")

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

    def _create_test_offer_documents(self, container, raw_data_list):
        """Helper to create test OFFER documents and load them into repository."""
        repository = container.document_repository()
        documents = []

        for i, raw_data in enumerate(raw_data_list):
            document = Document(
                id=None,
                external_id=raw_data.get("id", f"test_offer_{i}"),
                raw_data=raw_data,
                type=DocumentType.OFFER,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
            documents.append(document)

        repository.upsert_batch(documents)
        return documents

    def test_execute_returns_zero_when_no_offer_documents(self):
        """Test execute returns 0 when repository has no OFFER documents."""
        container = self._create_isolated_container()
        usecase = container.load_documents_usecase()

        input_data = LoadDocumentsInput(
            operation_type=LoadOperationType.FETCH_FROM_API,
            kwargs={"document_type": DocumentType.OFFER},
        )
        result = usecase.execute(input_data)
        self.assertEqual(result["created"], 0)
        self.assertEqual(result["updated"], 0)

    def test_execute_returns_correct_count_with_offer_documents(self):
        """Test execute returns correct count when OFFER documents exist."""
        container = self._create_isolated_container()
        usecase = container.load_documents_usecase()

        raw_data = copy.deepcopy(self.raw_offer_documents)
        self._create_test_offer_documents(container, raw_data)

        input_data = LoadDocumentsInput(
            operation_type=LoadOperationType.FETCH_FROM_API,
            kwargs={"document_type": DocumentType.OFFER},
        )
        result = usecase.execute(input_data)
        self.assertEqual(result["updated"], 3)

    def test_get_by_type_returns_offer_documents_only(self):
        """Test get_by_type returns only OFFER documents."""
        container = self._create_isolated_container()
        repository = container.document_repository()

        documents = [
            Document(
                id=None,
                external_id="OFFER_001",
                raw_data={"title": "Développeur Full Stack", "category": "A"},
                type=DocumentType.OFFER,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            ),
            Document(
                id=None,
                external_id="OFFER_002",
                raw_data={"title": "Data Scientist", "category": "A"},
                type=DocumentType.OFFER,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            ),
            Document(
                id=None,
                external_id="CORPS_001",
                raw_data={"name": "Corps 1"},
                type=DocumentType.CORPS,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            ),
        ]

        repository.upsert_batch(documents)

        offer_docs = repository.fetch_by_type(DocumentType.OFFER)
        self.assertEqual(len(offer_docs), 2)

        for doc in offer_docs:
            self.assertEqual(doc.type, DocumentType.OFFER)

    def test_upsert_batch_creates_new_offer_document(self):
        """Test upsert_batch creates a new OFFER document when it doesn't exist."""
        container = self._create_isolated_container()
        repository = container.document_repository()

        document = Document(
            id=None,
            external_id="OFFER_NEW",
            raw_data={
                "id": "OFFER_NEW",
                "verse": "FPE",
                "title": "Nouveau poste",
                "profile": "Profil test",
                "category": "A",
            },
            type=DocumentType.OFFER,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        result = repository.upsert_batch([document])

        self.assertEqual(result["created"], 1)
        self.assertEqual(result["updated"], 0)
        self.assertEqual(len(result["errors"]), 0)

        # Verify document was created
        docs = repository.fetch_by_type(DocumentType.OFFER)
        self.assertEqual(len(docs), 1)
        self.assertEqual(docs[0].raw_data["title"], "Nouveau poste")

    def test_upsert_batch_returns_correct_counts_for_offers(self):
        """Test upsert_batch returns correct created/updated counts for OFFER."""
        container = self._create_isolated_container()
        repository = container.document_repository()

        documents = [
            Document(
                id=None,
                external_id="OFFER_001",
                raw_data={
                    "id": "OFFER_001",
                    "title": "Développeur",
                    "category": "A",
                },
                type=DocumentType.OFFER,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            ),
            Document(
                id=None,
                external_id="OFFER_002",
                raw_data={
                    "id": "OFFER_002",
                    "title": "Analyste",
                    "category": "A",
                },
                type=DocumentType.OFFER,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            ),
        ]

        result = repository.upsert_batch(documents)

        self.assertEqual(result["created"], 2)
        self.assertEqual(result["updated"], 0)

    def test_fetch_from_api_strategy_with_offer_type(self):
        """Test FetchFromApiStrategy specifically with OFFER document type."""
        container = self._create_isolated_container()
        strategy_factory = container.load_documents_strategy_factory()

        # Pre-populate repository with OFFER documents
        raw_data = copy.deepcopy(self.raw_offer_documents)
        self._create_test_offer_documents(container, raw_data)

        strategy = strategy_factory.create(LoadOperationType.FETCH_FROM_API)
        documents = strategy.load_documents(document_type=DocumentType.OFFER)

        self.assertEqual(len(documents), 3)
        for doc in documents:
            self.assertEqual(doc.type, DocumentType.OFFER)
            self.assertIn("title", doc.raw_data)
            self.assertIn("category", doc.raw_data)

    def test_offer_document_structure_validation(self):
        """Test that OFFER documents have expected structure."""
        container = self._create_isolated_container()
        repository = container.document_repository()

        # Test with fixture data structure
        raw_data = copy.deepcopy(self.raw_offer_documents)
        self._create_test_offer_documents(container, raw_data)

        stored_docs = repository.fetch_by_type(DocumentType.OFFER)

        for doc in stored_docs:
            # Verify required fields are present
            self.assertIn("id", doc.raw_data)
            self.assertIn("verse", doc.raw_data)
            self.assertIn("title", doc.raw_data)
            self.assertIn("profile", doc.raw_data)
            self.assertIn("category", doc.raw_data)

            # Verify verse values are valid
            self.assertIn(doc.raw_data["verse"], ["FPE", "FPT"])
