import pytest
from django.apps import apps
from referentiel.exceptions.concours_errors import ConcoursDoesNotExist
from referentiel.exceptions.corps_errors import CorpsDoesNotExist
from referentiel.exceptions.offer_errors import OfferDoesNotExist

from config.app_config import AppConfig
from domain.ingestion.entities.document import DocumentType
from infrastructure.di.ingestion.ingestion_container import IngestionContainer
from infrastructure.di.shared.shared_container import SharedContainer
from infrastructure.factories.ingestion.document_factory import DocumentFactory
from infrastructure.factories.referentiel.concours_factory import ConcoursFactory
from infrastructure.factories.referentiel.corps_factory import CorpsFactory
from infrastructure.gateways.shared.logger import LoggerService

# Test constants
DOCUMENTS_COUNT = 2
MIXED_DOCUMENTS_COUNT = 3

DOCUMENT_TYPE_MODEL_MAP = {
    DocumentType.CORPS: "CorpsModel",
    DocumentType.CONCOURS: "ConcoursModel",
    DocumentType.METIERS: "MetierModel",
}


def execute_results(created: int = 0, updated: int = 0):
    return {
        "processed": created + updated,
        "cleaned": created + updated,
        "created": created,
        "updated": updated,
        "errors": 0,
        "error_details": [],
    }


@pytest.fixture
def clean_documents_integration_container(db):
    container = IngestionContainer()

    shared_container = SharedContainer()

    app_config = AppConfig.from_django_settings()
    shared_container.app_config.override(app_config)

    logger_service = LoggerService()
    shared_container.logger_service.override(logger_service)

    container.shared_container.override(shared_container)

    container.app_config.override(app_config)
    container.logger_service.override(logger_service)
    return container


@pytest.mark.parametrize(
    "document_type",
    [
        DocumentType.CORPS,
        DocumentType.CONCOURS,
        DocumentType.METIERS,
    ],
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
    model_class = apps.get_model("referentiel", DOCUMENT_TYPE_MODEL_MAP[document_type])
    assert model_class.objects.count() == 0


@pytest.mark.parametrize(
    "document_type", [DocumentType.CORPS, DocumentType.CONCOURS, DocumentType.METIERS]
)
def test_execute_updates_existing_entities(
    db, clean_documents_integration_container, document_type
):
    clean_documents_usecase = (
        clean_documents_integration_container.clean_documents_usecase()
    )

    # Create raw document in database using repository
    document_repository = clean_documents_integration_container.document_repository()

    document = DocumentFactory.create_entity_batch(
        document_type=document_type, count=1
    )[0]

    document_repository.upsert_batch([document], document_type)

    # First execution - create entity
    assert clean_documents_usecase.execute(document_type) == execute_results(created=1)

    # Second execution with same data - should update
    assert clean_documents_usecase.execute(document_type) == execute_results(updated=1)

    # Verify only one entity exists
    model_class = apps.get_model("referentiel", DOCUMENT_TYPE_MODEL_MAP[document_type])
    assert model_class.objects.count() == 1


def test_find_by_id_nonexistent(db, clean_documents_integration_container):
    corps_repository = (
        clean_documents_integration_container.shared_container.corps_repository()
    )
    with pytest.raises(CorpsDoesNotExist):
        corps_repository.get_by_id(99999)
    concours_repository = (
        clean_documents_integration_container.shared_container.concours_repository()
    )
    with pytest.raises(ConcoursDoesNotExist):
        concours_repository.get_by_id(99999)
    offers_repository = (
        clean_documents_integration_container.shared_container.offers_repository()
    )
    with pytest.raises(OfferDoesNotExist):
        offers_repository.get_by_id(99999)


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

    metier_repository = (
        clean_documents_integration_container.shared_container.metiers_repository()
    )

    all_corps = corps_repository.get_all()
    all_concours = concours_repository.get_all()
    all_offers = offer_repository.get_all()
    all_metiers = metier_repository.get_all()

    assert len(all_corps) == 0
    assert isinstance(all_corps, list)
    assert len(all_concours) == 0
    assert isinstance(all_concours, list)
    assert len(all_offers) == 0
    assert isinstance(all_offers, list)
    assert len(all_metiers) == 0
    assert isinstance(all_metiers, list)


def test_upsert_batch_database_error(db, clean_documents_integration_container):
    corps_repository = (
        clean_documents_integration_container.shared_container.corps_repository()
    )
    concours_repository = (
        clean_documents_integration_container.shared_container.concours_repository()
    )

    corps = CorpsFactory.create_model()
    corps.name = None  # no QA
    result_corps = corps_repository.upsert_batch([corps])

    concours = ConcoursFactory.create_model()
    concours.nor_original = None  # no QA
    result_concours = concours_repository.upsert_batch([concours])

    assert result_corps["created"] == 0
    assert result_corps["updated"] == 0
    assert len(result_corps["errors"]) == 1

    assert result_concours["created"] == 0
    assert result_concours["updated"] == 0
    assert len(result_concours["errors"]) == 1
