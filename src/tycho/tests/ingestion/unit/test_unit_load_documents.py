"""Unit test cases for LoadDocuments documents_usecase.

IMPORTANT: Dependency Injection Override Timing
- Override timing is crucial with dependency-injector
- Always override BEFORE creating the documents_usecase, not after
- Dependencies are resolved at creation time, not execution time
"""

import copy
from datetime import datetime
from unittest.mock import patch

import pytest

from application.ingestion.interfaces.load_documents_input import LoadDocumentsInput
from application.ingestion.interfaces.load_operation_type import LoadOperationType
from domain.entities.document import Document, DocumentType
from infrastructure.exceptions.ingestion_exceptions import (
    MissingOperationParameterError,
)


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


@pytest.fixture(name="offer_documents")
def offer_documents_fixture():
    """Create multiple offer documents for batch testing."""
    return [
        Document(
            id=None,
            external_id="offer_1",
            raw_data={"name": "Offer 1", "description": "First offer"},
            type=DocumentType.OFFERS,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        ),
        Document(
            id=None,
            external_id="offer_2",
            raw_data={"name": "Offer 2", "description": "Second offer"},
            type=DocumentType.OFFERS,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        ),
    ]


@pytest.fixture(name="raw_offer_documents")
def raw_offer_documents_fixture(offer_documents):
    """Return raw_data of offer_documents fixture."""
    return [doc.raw_data for doc in offer_documents]


@pytest.fixture(name="concours_documents")
def concours_documents_fixture():
    """Create sample contest documents."""
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


@pytest.fixture(name="raw_concours_documents")
def raw_concours_documents_fixture(concours_documents):
    """Return raw_data of concours_documents fixture."""
    return [doc.raw_data for doc in concours_documents]


def create_test_documents(
    documents_ingestion_container,
    raw_data_list,
    doc_type=DocumentType.CORPS,
):
    """Helper to create test documents and load them into documents_repository."""
    documents_repository = documents_ingestion_container.document_repository()

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

    documents_repository.upsert_batch(documents, doc_type.value)
    return documents


class TestDocumentsUsecase:
    """Test documents usecase."""

    def test_execute_returns_zero_when_no_documents(self, documents_usecase):
        """Test execute returns 0 when documents_repository is empty."""
        input_data = LoadDocumentsInput(
            operation_type=LoadOperationType.FETCH_FROM_API,
            kwargs={"document_type": DocumentType.CORPS},
        )
        result = documents_usecase.execute(input_data)
        assert result["created"] == 0
        assert result["updated"] == 0

    @pytest.mark.parametrize(
        "documents_fixture,document_type",
        [
            ("corps_documents", DocumentType.CORPS),
            ("offer_documents", DocumentType.OFFERS),
        ],
    )
    def test_execute_creates_new_documents_when_none_exist(
        self,
        documents_usecase,
        documents_ingestion_container,
        documents_fixture,
        document_type,
        request,
    ):
        """Test execute creates new documents when none exist in the system."""
        documents = request.getfixturevalue(documents_fixture)

        strategy = documents_ingestion_container.load_documents_strategy_factory()
        document_fetcher = strategy.document_fetcher

        with patch.object(
            document_fetcher,
            "fetch_by_type",
            return_value=(documents, False),
        ):
            input_data = LoadDocumentsInput(
                operation_type=LoadOperationType.FETCH_FROM_API,
                kwargs={"document_type": document_type},
            )
            result = documents_usecase.execute(input_data)

        assert result["created"] == len(documents)
        assert result["updated"] == 0

    @pytest.mark.parametrize(
        "raw_documents_fixture,document_type",
        [
            ("raw_corps_documents", DocumentType.CORPS),
            ("raw_offer_documents", DocumentType.OFFERS),
        ],
    )
    def test_execute_updates_documents_when_exist(
        self,
        documents_usecase,
        documents_ingestion_container,
        raw_documents_fixture,
        document_type,
        request,
    ):
        """Test execute updates existing documents."""
        raw_documents = request.getfixturevalue(raw_documents_fixture)
        raw_data = copy.deepcopy(raw_documents)
        create_test_documents(
            documents_ingestion_container, raw_data, doc_type=document_type
        )

        input_data = LoadDocumentsInput(
            operation_type=LoadOperationType.FETCH_FROM_API,
            kwargs={"document_type": document_type},
        )
        result = documents_usecase.execute(input_data)
        assert result["created"] == 0
        assert result["updated"] == len(raw_documents)

    def test_execute_returns_correct_count_with_documents_with_data_input(
        self,
        documents_usecase,
        documents_ingestion_container,
        raw_corps_documents,
    ):
        """Test execute returns correct count when documents exist with CSV upload."""
        raw_data = copy.deepcopy(raw_corps_documents)
        documents = create_test_documents(documents_ingestion_container, raw_data)

        input_data = LoadDocumentsInput(
            operation_type=LoadOperationType.UPLOAD_FROM_CSV,
            kwargs={"documents": documents, "document_type": DocumentType.CORPS},
        )
        result = documents_usecase.execute(input_data)
        assert result["created"] == len(raw_corps_documents)

    def test_missing_document_type_raises_missing_operation_parameter_error(
        self, documents_usecase
    ):
        """Test that missing document_type in kwargs raises ApplicationError."""
        input_data = LoadDocumentsInput(
            operation_type=LoadOperationType.FETCH_FROM_API,
            kwargs={},
        )
        with pytest.raises(MissingOperationParameterError):
            documents_usecase.execute(input_data)
