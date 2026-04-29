from datetime import datetime, timezone
from unittest.mock import AsyncMock, Mock

import pytest

from application.ingestion.interfaces.load_documents_input import LoadDocumentsInput
from application.ingestion.interfaces.load_operation_type import LoadOperationType
from application.ingestion.usecases.load_documents import LoadDocumentsUsecase
from domain.entities.document import Document, DocumentType
from infrastructure.gateways.shared.logger import LoggerService
from tests.utils.in_memory_document_repository import InMemoryDocumentRepository

TWO_DOCUMENTS_COUNT = 2


@pytest.fixture
def load_documents():
    logger_service = LoggerService()
    document_repo = InMemoryDocumentRepository()

    mock_strategy = Mock()
    mock_strategy.load_documents = AsyncMock()

    strategy_factory = Mock()
    strategy_factory.create.return_value = mock_strategy

    usecase = LoadDocumentsUsecase(
        strategy_factory=strategy_factory,
        document_repository=document_repo,
        logger=logger_service,
    )

    return usecase, document_repo, strategy_factory, mock_strategy


@pytest.fixture
def sample_documents():
    return [
        Document(
            external_id="doc_1",
            raw_data={"name": "Document 1", "description": "First document"},
            type=DocumentType.CORPS,
            created_at=datetime.now(timezone.utc),
        ),
        Document(
            external_id="doc_2",
            raw_data={"name": "Document 2", "description": "Second document"},
            type=DocumentType.CORPS,
            created_at=datetime.now(timezone.utc),
        ),
    ]


async def test_execute_with_no_documents_returns_zero_counts(load_documents):
    usecase, _, factory, strategy = load_documents

    strategy.load_documents.return_value = ([], False)

    input_data = LoadDocumentsInput(
        operation_type=LoadOperationType.FETCH_FROM_API,
        kwargs={"document_type": DocumentType.CORPS},
    )

    result = await usecase.execute(input_data)

    assert result["created"] == 0
    assert result["updated"] == 0
    assert result["errors"] == []

    factory.create.assert_called_once_with(LoadOperationType.FETCH_FROM_API)
    strategy.load_documents.assert_called_once_with(
        document_type=DocumentType.CORPS, start=1
    )


async def test_execute_with_single_batch_documents(load_documents, sample_documents):
    usecase, repo, _, strategy = load_documents

    strategy.load_documents.return_value = (sample_documents, False)

    input_data = LoadDocumentsInput(
        operation_type=LoadOperationType.FETCH_FROM_API,
        kwargs={"document_type": DocumentType.CORPS},
    )

    result = await usecase.execute(input_data)

    assert result["created"] == len(sample_documents)
    assert result["updated"] == 0
    assert result["errors"] == []

    assert len(repo.get_by_type(DocumentType.CORPS, 0)) == len(sample_documents)


async def test_execute_with_pagination_logic(load_documents, sample_documents):
    usecase, _, _, strategy = load_documents

    first_batch = sample_documents[:1]
    second_batch = sample_documents[1:]

    strategy.load_documents.side_effect = [
        (first_batch, True),
        (second_batch, False),
    ]

    input_data = LoadDocumentsInput(
        operation_type=LoadOperationType.FETCH_FROM_API,
        kwargs={"document_type": DocumentType.CORPS},
    )

    result = await usecase.execute(input_data)

    assert result["created"] == len(sample_documents)
    assert result["updated"] == 0
    assert result["errors"] == []

    assert strategy.load_documents.call_count == TWO_DOCUMENTS_COUNT

    first_call = strategy.load_documents.call_args_list[0]
    second_call = strategy.load_documents.call_args_list[1]

    assert first_call.kwargs["start"] == 1
    assert second_call.kwargs["start"] == TWO_DOCUMENTS_COUNT


async def test_execute_sets_default_start_parameter(load_documents):
    usecase, repo, factory, strategy = load_documents

    strategy.load_documents.return_value = ([], False)

    input_data = LoadDocumentsInput(
        operation_type=LoadOperationType.FETCH_FROM_API,
        kwargs={"document_type": DocumentType.CORPS},
    )

    await usecase.execute(input_data)

    strategy.load_documents.assert_called_once_with(
        document_type=DocumentType.CORPS, start=1
    )


async def test_execute_preserves_existing_start_parameter(load_documents):
    usecase, _, _, strategy = load_documents

    strategy.load_documents.return_value = ([], False)

    input_data = LoadDocumentsInput(
        operation_type=LoadOperationType.FETCH_FROM_API,
        kwargs={"document_type": DocumentType.CORPS, "start": 5},
    )

    await usecase.execute(input_data)

    strategy.load_documents.assert_called_once_with(
        document_type=DocumentType.CORPS, start=5
    )


async def test_execute_with_upload_from_csv_operation(load_documents, sample_documents):
    usecase, _, factory, strategy = load_documents

    strategy.load_documents.return_value = (sample_documents, False)

    input_data = LoadDocumentsInput(
        operation_type=LoadOperationType.UPLOAD_FROM_CSV,
        kwargs={"document_type": DocumentType.CORPS, "documents": sample_documents},
    )

    await usecase.execute(input_data)

    factory.create.assert_called_once_with(LoadOperationType.UPLOAD_FROM_CSV)

    strategy.load_documents.assert_called_once_with(
        document_type=DocumentType.CORPS, documents=sample_documents, start=1
    )


async def test_execute_aggregates_results_from_multiple_batches(load_documents):
    usecase, repo, _, strategy = load_documents

    doc1 = Document(
        external_id="new_doc",
        raw_data={"name": "New Document"},
        type=DocumentType.CORPS,
        created_at=datetime.now(timezone.utc),
    )

    existing_doc = Document(
        external_id="existing_doc",
        raw_data={"name": "Existing Document"},
        type=DocumentType.CORPS,
        created_at=datetime.now(timezone.utc),
    )
    repo.upsert_batch([existing_doc], DocumentType.CORPS)

    strategy.load_documents.side_effect = [
        ([doc1], True),
        ([existing_doc], False),
    ]

    input_data = LoadDocumentsInput(
        operation_type=LoadOperationType.FETCH_FROM_API,
        kwargs={"document_type": DocumentType.CORPS},
    )

    result = await usecase.execute(input_data)

    assert result["created"] + result["updated"] == TWO_DOCUMENTS_COUNT
    assert result["errors"] == []
