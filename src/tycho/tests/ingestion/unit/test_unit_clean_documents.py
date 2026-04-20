from datetime import datetime, timezone

import pytest

from config.app_config import AppConfig
from domain.entities.document import Document, DocumentType
from domain.exceptions.document_error import UnsupportedDocumentTypeError
from infrastructure.di.ingestion.ingestion_container import IngestionContainer
from infrastructure.gateways.shared.logger import LoggerService
from tests.fixtures.clean_test_factories import (
    THREE_DOCUMENTS_COUNT,
    TWO_DOCUMENTS_COUNT,
    create_test_concours_document,
    create_test_concours_document_invalid_status,
    create_test_concours_document_old_year,
    create_test_corps_document,
    create_test_corps_document_fpt,
    create_test_corps_document_minarm,
    create_test_metier_document,
)
from tests.utils.in_memory_concours_repository import InMemoryConcoursRepository
from tests.utils.in_memory_corps_repository import InMemoryCorpsRepository
from tests.utils.in_memory_document_repository import InMemoryDocumentRepository
from tests.utils.in_memory_metier_repository import InMemoryMetierRepository
from tests.utils.in_memory_offers_repository import InMemoryOffersRepository

# Test constants for offers edge cases
OFFERS_TOTAL_DOCUMENTS = 6
OFFERS_VALID_DOCUMENTS = 4
OFFERS_ERROR_DOCUMENTS = 2


@pytest.fixture
def clean_documents_container():

    container = IngestionContainer()

    app_config = AppConfig.from_django_settings()
    logger_service = LoggerService()

    # Override des services
    container.logger_service.override(logger_service)
    container.app_config.override(app_config)
    container.shared_container.app_config.override(app_config)

    in_memory_document_repo = InMemoryDocumentRepository()
    container.document_repository.override(in_memory_document_repo)

    in_memory_corps_repo = InMemoryCorpsRepository()
    container.shared_container.corps_repository.override(in_memory_corps_repo)

    in_memory_concours_repo = InMemoryConcoursRepository()
    container.shared_container.concours_repository.override(in_memory_concours_repo)

    in_memory_offers_repo = InMemoryOffersRepository()
    container.shared_container.offers_repository.override(in_memory_offers_repo)

    # Le repository métier manquant !
    in_memory_metier_repo = InMemoryMetierRepository()
    container.shared_container.metiers_repository.override(in_memory_metier_repo)

    return container


@pytest.mark.parametrize(
    "document_type", [DocumentType.CORPS, DocumentType.CONCOURS, DocumentType.METIERS]
)
def test_clean_multiple_documents_success(clean_documents_container, document_type):
    usecase = clean_documents_container.clean_documents_usecase()
    # Create multiple documents
    if document_type == DocumentType.CORPS:
        documents = [
            create_test_corps_document(i) for i in range(1, THREE_DOCUMENTS_COUNT + 1)
        ]
    elif document_type == DocumentType.CONCOURS:
        documents = [
            create_test_concours_document(i)
            for i in range(1, THREE_DOCUMENTS_COUNT + 1)
        ]
    else:  # DocumentType.METIERS
        documents = [
            create_test_metier_document(i) for i in range(1, THREE_DOCUMENTS_COUNT + 1)
        ]
    # Add documents to repository
    repository = clean_documents_container.document_repository()
    repository.upsert_batch(documents, document_type)

    result = usecase.execute(document_type)

    assert result["processed"] == THREE_DOCUMENTS_COUNT
    assert result["cleaned"] == THREE_DOCUMENTS_COUNT
    assert result["created"] == THREE_DOCUMENTS_COUNT
    assert result["updated"] == 0
    assert result["errors"] == 0


@pytest.mark.parametrize(
    "document_type", [DocumentType.CORPS, DocumentType.CONCOURS, DocumentType.METIERS]
)
def test_clean_documents_with_empty_repository(
    clean_documents_container, document_type
):
    usecase = clean_documents_container.clean_documents_usecase()

    result = usecase.execute(document_type)

    assert result["processed"] == 0
    assert result["cleaned"] == 0
    assert result["created"] == 0
    assert result["updated"] == 0
    assert result["errors"] == 0


def test_execute_raises_error_for_unsupported_document_type(clean_documents_container):
    # Create a GRADE document (unsupported)
    grade_document = Document(
        external_id="grade_test_1",
        raw_data={"test": "data"},
        type=DocumentType.GRADE,
        created_at=datetime.now(timezone.utc),
    )

    repository = clean_documents_container.document_repository()
    repository.upsert_batch([grade_document], DocumentType.GRADE)

    usecase = clean_documents_container.clean_documents_usecase()

    with pytest.raises(UnsupportedDocumentTypeError) as exc_info:
        usecase.execute(DocumentType.GRADE)

    assert "GRADE" in str(exc_info.value)


def test_clean_corps_filters_invalid_documents(clean_documents_container):
    usecase = clean_documents_container.clean_documents_usecase()

    # Create mixed data: 1 valid FPE + 1 invalid FPT
    valid_document = create_test_corps_document(1)
    fpt_document = create_test_corps_document_fpt(8)
    minarm_document = create_test_corps_document_minarm(9)

    repository = clean_documents_container.document_repository()
    repository.upsert_batch(
        [
            valid_document,
            fpt_document,
            minarm_document,
        ],
        DocumentType.CORPS,
    )
    result = usecase.execute(DocumentType.CORPS)

    assert result["processed"] == THREE_DOCUMENTS_COUNT
    assert result["cleaned"] == 1
    assert result["created"] == 1
    assert result["updated"] == 0
    assert result["errors"] == TWO_DOCUMENTS_COUNT


def test_clean_concours_filters_invalid_documents(clean_documents_container):
    usecase = clean_documents_container.clean_documents_usecase()

    # Create mixed data: 1 valid FPE + 1 invalid FPT
    valid_document = create_test_concours_document(1)
    invalid_status_document = create_test_concours_document_invalid_status(4)
    old_document = create_test_concours_document_old_year(5)

    repository = clean_documents_container.document_repository()
    repository.upsert_batch(
        [
            valid_document,
            invalid_status_document,
            old_document,
        ],
        DocumentType.CONCOURS,
    )
    result = usecase.execute(DocumentType.CONCOURS)

    assert result["processed"] == THREE_DOCUMENTS_COUNT
    assert result["cleaned"] == 1
    assert result["created"] == 1
    assert result["updated"] == 0
    assert result["errors"] == TWO_DOCUMENTS_COUNT
