"""Unit test cases for LoadDocuments usecase.

IMPORTANT: Dependency Injection Override Timing
- Override timing is crucial with dependency-injector
- Always override BEFORE creating the usecase, not after
- Dependencies are resolved at creation time, not execution time
"""

import copy
from datetime import datetime

import pytest

from application.ingestion.interfaces.load_documents_input import LoadDocumentsInput
from application.ingestion.interfaces.load_operation_type import LoadOperationType
from domain.entities.document import Document, DocumentType
from infrastructure.di.ingestion.ingestion_container import IngestionContainer
from infrastructure.gateways.ingestion import load_documents_strategy_factory
from infrastructure.gateways.shared.logger import LoggerService
from tests.fixtures.fixture_loader import load_fixture
from tests.utils.in_memory_document_repository import InMemoryDocumentRepository


@pytest.fixture(scope="session", name="raw_corps_documents")
def raw_corps_documents_fixture():
    """Load fixture data once for all tests."""
    return load_fixture("corps_ingres_20251117.json")


@pytest.fixture(name="container")
def container_fixture():
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


@pytest.fixture(name="usecase")
def usecase_fixture(container):
    """Create the load documents usecase."""
    return container.load_documents_usecase()


@pytest.fixture(name="repository")
def repository_fixture(container):
    """Get the document repository from the container."""
    return container.document_repository()


@pytest.fixture(name="corps_document")
def corps_document_fixture():
    """Create a single corps document for testing."""
    return Document(
        id=None,
        external_id="test_corps_doc",
        raw_data={"name": "Test Document"},
        type=DocumentType.CORPS,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )


@pytest.fixture(name="corps_documents")
def corps_documents_fixture():
    """Create multiple corps documents for batch testing."""
    return [
        Document(
            id=None,
            external_id="corps_1",
            raw_data={"name": "Corps 1", "description": "First corps"},
            type=DocumentType.CORPS,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        ),
        Document(
            id=None,
            external_id="corps_2",
            raw_data={"name": "Corps 2", "description": "Second corps"},
            type=DocumentType.CORPS,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        ),
    ]


@pytest.fixture(name="concours_documents")
def concours_documents_fixture():
    """Create sample concours documents."""
    return [
        Document(
            id=None,
            external_id="exam_1",
            raw_data={"name": "Exam 1"},
            type=DocumentType.CONCOURS,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        ),
    ]


def create_test_documents(container, raw_data_list, doc_type=DocumentType.CORPS):
    """Helper to create test documents and load them into repository."""
    repository = container.document_repository()

    documents = [
        Document(
            id=None,
            external_id=f"test_doc_{i}",
            raw_data={"test": "data", "index": i},
            type=doc_type,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        for i, _raw_data in enumerate(raw_data_list)
    ]

    repository.upsert_batch(documents, doc_type.value)
    return documents


def test_execute_returns_zero_when_no_documents(usecase):
    """Test execute returns 0 when repository is empty."""
    input_data = LoadDocumentsInput(
        operation_type=LoadOperationType.FETCH_FROM_API,
        kwargs={"document_type": DocumentType.CORPS},
    )
    result = usecase.execute(input_data)
    assert result["created"] == 0
    assert result["updated"] == 0


def test_execute_returns_correct_count_with_documents(
    usecase, container, raw_corps_documents
):
    """Test execute returns correct count when documents exist."""
    raw_data = copy.deepcopy(raw_corps_documents)
    create_test_documents(container, raw_data)

    input_data = LoadDocumentsInput(
        operation_type=LoadOperationType.FETCH_FROM_API,
        kwargs={"document_type": DocumentType.CORPS},
    )
    result = usecase.execute(input_data)
    assert result["updated"] == len(raw_corps_documents)


def test_get_by_type_returns_documents_of_correct_type_only(
    repository, corps_documents, concours_documents
):
    """Test get_by_type returns only documents of the specified type."""
    repository.upsert_batch(corps_documents, DocumentType.CORPS.value)
    repository.upsert_batch(concours_documents, DocumentType.CONCOURS.value)

    corps_docs = repository.fetch_by_type(DocumentType.CORPS)
    assert len(corps_docs) == len(corps_documents)

    for doc in corps_docs:
        assert doc.type == DocumentType.CORPS


def test_upsert_batch_creates_new_document(repository, corps_document):
    """Test upsert_batch creates a new document when it doesn't exist."""
    result = repository.upsert_batch([corps_document], DocumentType.CORPS.value)

    assert result["created"] == 1
    assert result["updated"] == 0
    assert len(result["errors"]) == 0

    # Verify document was created
    docs = repository.fetch_by_type(DocumentType.CORPS)
    assert len(docs) == 1
    assert docs[0].raw_data == corps_document.raw_data


def test_upsert_batch_returns_correct_counts(repository, corps_documents):
    """Test upsert_batch returns correct created/updated counts."""
    result = repository.upsert_batch(corps_documents, DocumentType.CORPS.value)

    assert result["created"] == len(corps_documents)
    assert result["updated"] == 0


def test_execute_returns_correct_count_with_documents_with_data_input(
    usecase, container, raw_corps_documents
):
    """Test execute returns correct count when documents exist with CSV upload."""
    raw_data = copy.deepcopy(raw_corps_documents)
    documents = create_test_documents(container, raw_data)

    input_data = LoadDocumentsInput(
        operation_type=LoadOperationType.UPLOAD_FROM_CSV,
        kwargs={"documents": documents, "document_type": DocumentType.CORPS},
    )
    result = usecase.execute(input_data)
    assert result["created"] == len(raw_corps_documents)
