"""Unit test cases for LoadDocuments documents_usecase.

IMPORTANT: Dependency Injection Override Timing
- Override timing is crucial with dependency-injector
- Always override BEFORE creating the documents_usecase, not after
- Dependencies are resolved at creation time, not execution time
"""

import copy
from datetime import datetime

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

    def test_execute_returns_correct_count_with_documents(
        self,
        documents_usecase,
        documents_ingestion_container,
        raw_corps_documents,
    ):
        """Test execute returns correct count when documents exist."""
        raw_data = copy.deepcopy(raw_corps_documents)
        create_test_documents(documents_ingestion_container, raw_data)

        input_data = LoadDocumentsInput(
            operation_type=LoadOperationType.FETCH_FROM_API,
            kwargs={"document_type": DocumentType.CORPS},
        )
        result = documents_usecase.execute(input_data)
        assert result["updated"] == len(raw_corps_documents)

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


class TestDocumentsRepository:
    """Test documents repository."""

    def test_get_by_type_returns_documents_of_correct_type_only(
        self, documents_repository, corps_documents, concours_documents
    ):
        """Test get_by_type returns only documents of the specified type."""
        datas = [
            (corps_documents, DocumentType.CORPS),
            (concours_documents, DocumentType.CONCOURS),
        ]
        for documents, document_type in datas:
            documents_repository.upsert_batch(documents, document_type.value)

        for documents, document_type in datas:
            docs = documents_repository.fetch_by_type(document_type)
            assert len(docs) == len(documents)
            for doc in docs:
                assert doc.type == document_type

    def test_upsert_batch_creates_new_document(
        self, documents_repository, corps_document
    ):
        """Test upsert_batch creates a new document when it doesn't exist."""
        result = documents_repository.upsert_batch(
            [corps_document], DocumentType.CORPS.value
        )

        assert result["created"] == 1
        assert result["updated"] == 0
        assert len(result["errors"]) == 0

        # Verify document was created
        docs = documents_repository.fetch_by_type(DocumentType.CORPS)
        assert len(docs) == 1
        assert docs[0].raw_data == corps_document.raw_data

    @pytest.mark.parametrize(
        "documents_fixture,document_type",
        [
            ("corps_documents", DocumentType.CORPS),
        ],
    )
    def test_upsert_batch_returns_correct_counts(
        self, documents_repository, documents_fixture, document_type, request
    ):
        """Test upsert_batch returns correct created/updated counts."""
        documents = request.getfixturevalue(documents_fixture)
        result = documents_repository.upsert_batch(documents, document_type.value)

        assert result["created"] == len(documents)
        assert result["updated"] == 0
