from unittest.mock import patch

import pytest
from django.apps import apps

from config.app_config import AppConfig
from domain.entities.document import DocumentType
from domain.exceptions.concours_errors import ConcoursDoesNotExist
from domain.exceptions.corps_errors import CorpsDoesNotExist
from domain.exceptions.offer_errors import OfferDoesNotExist
from infrastructure.di.ingestion.ingestion_container import IngestionContainer
from infrastructure.django_apps.ingestion.models.raw_document import RawDocument
from infrastructure.django_apps.shared.models.offer import OfferModel
from infrastructure.gateways.shared.logger import LoggerService
from infrastructure.repositories.ingestion.postgres_document_repository import (
    PostgresDocumentRepository,
)
from infrastructure.repositories.shared.postgres_concours_repository import (
    PostgresConcoursRepository,
)
from infrastructure.repositories.shared.postgres_corps_repository import (
    PostgresCorpsRepository,
)
from infrastructure.repositories.shared.postgres_metier_repository import (
    PostgresMetierRepository,
)
from infrastructure.repositories.shared.postgres_offers_repository import (
    PostgresOffersRepository,
)
from tests.fixtures.clean_test_factories import (
    create_test_concours_document,
    create_test_corps_document,
    create_test_offer_document,
)
from tests.fixtures.shared_fixtures import create_shared_qdrant_repository

# Test constants
DOCUMENTS_COUNT = 2
MIXED_DOCUMENTS_COUNT = 3

DOCUMENT_TYPE_MODEL_MAP = {
    DocumentType.CORPS: "CorpsModel",
    DocumentType.CONCOURS: "ConcoursModel",
    DocumentType.OFFERS: "OfferModel",
}

DOCUMENT_FACTORY_MAP = {
    DocumentType.CORPS: create_test_corps_document,
    DocumentType.CONCOURS: create_test_concours_document,
    DocumentType.OFFERS: create_test_offer_document,
}

DB_ERROR = "Database connection error"


def execute_results(created: int = 0, updated: int = 0):
    return {
        "processed": created + updated,
        "cleaned": created + updated,
        "created": created,
        "updated": updated,
        "errors": 0,
        "error_details": [],
    }


def assert_raw_document_pending(processing: bool):
    assert RawDocument.objects.filter(
        processed_at__isnull=True, processing=processing
    ).exists()


def assert_no_offer_cleaned():
    assert not OfferModel.objects.exists()


@pytest.fixture
def clean_documents_integration_container(db):

    container = IngestionContainer()

    app_config = AppConfig.from_django_settings()
    logger_service = LoggerService()

    # Override des services
    container.logger_service.override(logger_service)
    container.app_config.override(app_config)
    container.shared_container.app_config.override(app_config)

    # Repositories Postgres
    postgres_document_repo = PostgresDocumentRepository()
    container.document_repository.override(postgres_document_repo)

    postgres_corps_repo = PostgresCorpsRepository(logger_service)
    container.shared_container.corps_repository.override(postgres_corps_repo)

    postgres_concours_repo = PostgresConcoursRepository(logger_service)
    container.shared_container.concours_repository.override(postgres_concours_repo)

    postgres_offers_repo = PostgresOffersRepository(logger_service)
    container.shared_container.offers_repository.override(postgres_offers_repo)

    # Le repository métier manquant !
    postgres_metier_repo = PostgresMetierRepository(logger_service)
    container.shared_container.metiers_repository.override(postgres_metier_repo)

    # Vector repository pour les tests d'intégration
    qdrant_repository = create_shared_qdrant_repository()
    container.shared_container.vector_repository.override(qdrant_repository)

    return container


@pytest.fixture(name="raw_offer_setup")
def raw_offer_setup_fixture(db, clean_documents_integration_container):
    usecase = clean_documents_integration_container.clean_documents_usecase()
    repository = clean_documents_integration_container.document_repository()
    document = DOCUMENT_FACTORY_MAP[DocumentType.OFFERS](1)
    return usecase, repository, document


@pytest.mark.parametrize(
    "document_type", [DocumentType.CORPS, DocumentType.CONCOURS, DocumentType.OFFERS]
)
def test_execute_handles_empty_documents(
    db, clean_documents_integration_container, document_type
):
    clean_documents_usecase = (
        clean_documents_integration_container.clean_documents_usecase()
    )

    # No documents in database
    assert clean_documents_usecase.execute(document_type) == execute_results()

    # Verify no entities are saved
    model_class = apps.get_model("shared", DOCUMENT_TYPE_MODEL_MAP[document_type])
    assert model_class.objects.count() == 0


@pytest.mark.parametrize("document_type", [DocumentType.CORPS, DocumentType.CONCOURS])
def test_execute_updates_existing_entities(
    db, clean_documents_integration_container, document_type
):
    clean_documents_usecase = (
        clean_documents_integration_container.clean_documents_usecase()
    )

    # Create raw document in database using repository
    document_repository = clean_documents_integration_container.document_repository()

    document = DOCUMENT_FACTORY_MAP[document_type](1)

    document_repository.upsert_batch([document], document_type)

    # First execution - create entity
    assert clean_documents_usecase.execute(document_type) == execute_results(created=1)

    # Second execution with same data - should update
    assert clean_documents_usecase.execute(document_type) == execute_results(updated=1)

    # Verify only one entity exists
    model_class = apps.get_model("shared", DOCUMENT_TYPE_MODEL_MAP[document_type])
    assert model_class.objects.count() == 1


def test_execute_updates_existing_offers_entities(db, raw_offer_setup):
    document_type = DocumentType.OFFERS
    clean_documents_usecase, document_repository, document = raw_offer_setup
    document_repository.upsert_batch([document], document_type)

    # First execution - create entity
    assert clean_documents_usecase.execute(document_type) == execute_results(created=1)

    # Second execution with same data - should not update
    assert clean_documents_usecase.execute(document_type) == execute_results()

    # Third execution with updated entity
    document_repository.upsert_batch([document], document_type)
    assert clean_documents_usecase.execute(document_type) == execute_results(updated=1)

    # Verify only one entity exists
    assert OfferModel.objects.count() == 1


def test_find_by_id_nonexistent(db, clean_documents_integration_container):
    corps_repository = (
        clean_documents_integration_container.shared_container.corps_repository()
    )
    with pytest.raises(CorpsDoesNotExist):
        corps_repository.find_by_id(99999)
    concours_repository = (
        clean_documents_integration_container.shared_container.concours_repository()
    )
    with pytest.raises(ConcoursDoesNotExist):
        concours_repository.find_by_id(99999)
    offers_repository = (
        clean_documents_integration_container.shared_container.offers_repository()
    )
    with pytest.raises(OfferDoesNotExist):
        offers_repository.find_by_id(99999)


def test_repository_get_all_empty(db, clean_documents_integration_container):
    corps_repository = (
        clean_documents_integration_container.shared_container.corps_repository()
    )
    concours_repository = (
        clean_documents_integration_container.shared_container.concours_repository()
    )

    offer_repository = (
        clean_documents_integration_container.shared_container.offers_repository()
    )

    all_corps = corps_repository.get_all()
    all_concours = concours_repository.get_all()
    all_offers = offer_repository.get_all()

    assert len(all_corps) == 0
    assert isinstance(all_corps, list)
    assert len(all_concours) == 0
    assert isinstance(all_concours, list)
    assert len(all_offers) == 0
    assert isinstance(all_offers, list)


def test_upsert_batch_database_error(db, clean_documents_integration_container):
    corps_repository = (
        clean_documents_integration_container.shared_container.corps_repository()
    )
    concours_repository = (
        clean_documents_integration_container.shared_container.concours_repository()
    )

    corps = create_test_corps_document(1)
    corps.name = None  # no QA
    result_corps = corps_repository.upsert_batch([corps])

    concours = create_test_concours_document(1)
    concours.nor_original = None  # no QA
    result_concours = concours_repository.upsert_batch([concours])

    assert result_corps["created"] == 0
    assert result_corps["updated"] == 0
    assert len(result_corps["errors"]) == 1

    assert result_concours["created"] == 0
    assert result_concours["updated"] == 0
    assert len(result_concours["errors"]) == 1


def test_clean_offers_upsert_batch_error(
    db, clean_documents_integration_container, raw_offer_setup
):
    offers_repository = (
        clean_documents_integration_container.shared_container.offers_repository()
    )

    document_type = DocumentType.OFFERS
    clean_documents_usecase, document_repository, document = raw_offer_setup
    document_repository.upsert_batch([document], document_type)

    with patch.object(
        offers_repository,
        "upsert_batch",
        side_effect=Exception(DB_ERROR),
    ) as mocked_method:
        with pytest.raises(Exception, match=DB_ERROR):
            clean_documents_usecase.execute(document_type)
        mocked_method.assert_called_once()

    assert_no_offer_cleaned()
    assert_raw_document_pending(processing=True)


def test_clean_offers_get_pending_processing_error(db, raw_offer_setup):
    document_type = DocumentType.OFFERS
    clean_documents_usecase, document_repository, document = raw_offer_setup
    document_repository.upsert_batch([document], document_type)

    with patch.object(
        document_repository,
        "get_pending_processing",
        side_effect=Exception(DB_ERROR),
    ) as mocked_method:
        with pytest.raises(Exception, match=DB_ERROR):
            clean_documents_usecase.execute(document_type)
        mocked_method.assert_called_once()

    assert_no_offer_cleaned()
    assert_raw_document_pending(processing=False)


def test_clean_offers_cleaner_error(db, raw_offer_setup):
    document_type = DocumentType.OFFERS
    clean_documents_usecase, document_repository, document = raw_offer_setup
    document.raw_data = {"data": "dummy"}
    document_repository.upsert_batch([document], document_type)

    clean_documents_usecase.execute(document_type)

    assert_no_offer_cleaned()
    assert_raw_document_pending(processing=False)


def test_clean_offers_mark_as_processed_error(db, raw_offer_setup):
    document_type = DocumentType.OFFERS
    clean_documents_usecase, document_repository, document = raw_offer_setup
    document_repository.upsert_batch([document], document_type)

    with patch.object(
        document_repository,
        "mark_as_processed",
        side_effect=Exception(DB_ERROR),
    ) as mocked_method:
        with pytest.raises(Exception, match=DB_ERROR):
            clean_documents_usecase.execute(document_type)
        mocked_method.assert_called_once()

    assert_no_offer_cleaned()
    assert_raw_document_pending(processing=True)


def test_clean_offers_mark_as_pending_error(db, raw_offer_setup):
    document_type = DocumentType.OFFERS
    clean_documents_usecase, document_repository, document = raw_offer_setup
    document.raw_data = {"data": "dummy"}
    document_repository.upsert_batch([document], document_type)

    with patch.object(
        document_repository,
        "mark_as_pending",
        side_effect=Exception(DB_ERROR),
    ) as mocked_method:
        with pytest.raises(Exception, match=DB_ERROR):
            clean_documents_usecase.execute(document_type)
        mocked_method.assert_called_once()

    assert_no_offer_cleaned()
    assert_raw_document_pending(processing=True)
