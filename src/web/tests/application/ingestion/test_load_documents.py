import pytest

from application.ingestion.interfaces.load_documents_input import LoadDocumentsInput
from application.ingestion.interfaces.load_operation_type import LoadOperationType
from domain.ingestion.entities.document import DocumentType
from tests.factories.document_factory import DocumentFactory

TWO_DOCUMENTS_COUNT = 2


@pytest.fixture
def sample_documents():
    return DocumentFactory.create_entity_batch(
        count=TWO_DOCUMENTS_COUNT, document_type=DocumentType.CORPS
    )


async def test_execute_with_no_documents_returns_zero_counts(load_documents_usecase):
    strategy_factory = load_documents_usecase.strategy_factory
    strategy = strategy_factory.create.return_value
    strategy.load_documents.return_value = ([], False)

    input_data = LoadDocumentsInput(
        operation_type=LoadOperationType.FETCH_FROM_API,
        kwargs={"document_type": DocumentType.CORPS},
    )

    result = await load_documents_usecase.execute(input_data)

    assert result["created"] == 0
    assert result["updated"] == 0
    assert result["errors"] == []

    strategy_factory.create.assert_called_once_with(LoadOperationType.FETCH_FROM_API)
    strategy.load_documents.assert_called_once_with(
        document_type=DocumentType.CORPS, start=1
    )


async def test_execute_with_single_batch_documents(
    load_documents_usecase, sample_documents
):
    strategy_factory = load_documents_usecase.strategy_factory
    strategy = strategy_factory.create.return_value
    strategy.load_documents.return_value = (sample_documents, False)
    repo = load_documents_usecase.document_repository

    input_data = LoadDocumentsInput(
        operation_type=LoadOperationType.FETCH_FROM_API,
        kwargs={"document_type": DocumentType.CORPS},
    )

    result = await load_documents_usecase.execute(input_data)

    assert result["created"] == len(sample_documents)
    assert result["updated"] == 0
    assert result["errors"] == []

    assert len(repo.get_by_type(DocumentType.CORPS, 0)) == len(sample_documents)


async def test_execute_with_pagination_logic(load_documents_usecase, sample_documents):
    strategy_factory = load_documents_usecase.strategy_factory
    strategy = strategy_factory.create.return_value
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

    result = await load_documents_usecase.execute(input_data)

    assert result["created"] == len(sample_documents)
    assert result["updated"] == 0
    assert result["errors"] == []

    assert strategy.load_documents.call_count == TWO_DOCUMENTS_COUNT

    first_call = strategy.load_documents.call_args_list[0]
    second_call = strategy.load_documents.call_args_list[1]

    assert first_call.kwargs["start"] == 1
    assert second_call.kwargs["start"] == TWO_DOCUMENTS_COUNT


async def test_execute_sets_default_start_parameter(load_documents_usecase):
    strategy_factory = load_documents_usecase.strategy_factory
    strategy = strategy_factory.create.return_value

    strategy.load_documents.return_value = ([], False)

    input_data = LoadDocumentsInput(
        operation_type=LoadOperationType.FETCH_FROM_API,
        kwargs={"document_type": DocumentType.CORPS},
    )

    await load_documents_usecase.execute(input_data)

    strategy.load_documents.assert_called_once_with(
        document_type=DocumentType.CORPS, start=1
    )


async def test_execute_preserves_existing_start_parameter(load_documents_usecase):
    strategy_factory = load_documents_usecase.strategy_factory
    strategy = strategy_factory.create.return_value

    strategy.load_documents.return_value = ([], False)

    input_data = LoadDocumentsInput(
        operation_type=LoadOperationType.FETCH_FROM_API,
        kwargs={"document_type": DocumentType.CORPS, "start": 5},
    )

    await load_documents_usecase.execute(input_data)

    strategy.load_documents.assert_called_once_with(
        document_type=DocumentType.CORPS, start=5
    )


async def test_execute_with_upload_from_csv_operation(
    load_documents_usecase, sample_documents
):
    strategy_factory = load_documents_usecase.strategy_factory
    strategy = strategy_factory.create.return_value

    strategy.load_documents.return_value = (sample_documents, False)

    input_data = LoadDocumentsInput(
        operation_type=LoadOperationType.UPLOAD_FROM_CSV,
        kwargs={"document_type": DocumentType.CORPS, "documents": sample_documents},
    )

    await load_documents_usecase.execute(input_data)

    strategy_factory.create.assert_called_once_with(LoadOperationType.UPLOAD_FROM_CSV)

    strategy.load_documents.assert_called_once_with(
        document_type=DocumentType.CORPS, documents=sample_documents, start=1
    )


async def test_execute_aggregates_results_from_multiple_batches(
    load_documents_usecase, sample_documents
):
    strategy_factory = load_documents_usecase.strategy_factory
    strategy = strategy_factory.create.return_value
    repo = load_documents_usecase.document_repository

    doc1 = sample_documents[0]
    existing_doc = sample_documents[1]

    repo.upsert_batch([existing_doc], DocumentType.CORPS)

    strategy.load_documents.side_effect = [
        ([doc1], True),
        ([existing_doc], False),
    ]

    input_data = LoadDocumentsInput(
        operation_type=LoadOperationType.FETCH_FROM_API,
        kwargs={"document_type": DocumentType.CORPS},
    )

    result = await load_documents_usecase.execute(input_data)

    assert result["created"] + result["updated"] == TWO_DOCUMENTS_COUNT
    assert result["errors"] == []
