from unittest.mock import patch

import pytest
from django.apps import apps

from config.app_config import AppConfig
from domain.entities.document import DocumentType
from domain.exceptions.concours_errors import ConcoursDoesNotExist
from domain.exceptions.corps_errors import CorpsDoesNotExist
from domain.exceptions.offer_errors import OfferDoesNotExist
from infrastructure.di.ingestion.ingestion_container import IngestionContainer
from infrastructure.di.shared.shared_container import SharedContainer
from infrastructure.django_apps.ingestion.models.raw_document import RawDocument
from infrastructure.django_apps.shared.models.offer import OfferModel
from infrastructure.gateways.shared.logger import LoggerService
from tests.factories.concours_factory import ConcoursFactory
from tests.factories.corps_factory import CorpsFactory
from tests.factories.document_factory import DocumentFactory
from tests.factories.source_factory import SourceFactory
from tests.factories.talentsoft_factories import (
    TalentsoftCodedObjectFactory,
    TalentsoftCustomCodeTableFactory,
    TalentsoftCustomFieldsFactory,
    TalentsoftDescriptionCustomFieldsFactory,
    TalentsoftOfferFactory,
)

# Test constants
DOCUMENTS_COUNT = 2
MIXED_DOCUMENTS_COUNT = 3

DOCUMENT_TYPE_MODEL_MAP = {
    DocumentType.CORPS: "CorpsModel",
    DocumentType.CONCOURS: "ConcoursModel",
    DocumentType.OFFERS: "OfferModel",
    DocumentType.METIERS: "MetierModel",
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


def assert_raw_document_failed():
    assert RawDocument.objects.filter(
        processed_at__isnull=False, processing=False, error_msg__isnull=False
    ).exists()


def assert_no_offer_cleaned():
    assert not OfferModel.objects.exists()


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


@pytest.fixture(name="offer_source")
def offer_source_fixture(db):
    return SourceFactory.create_model()


@pytest.fixture(name="raw_offer_setup")
def raw_offer_setup_fixture(db, clean_documents_integration_container, offer_source):
    usecase = clean_documents_integration_container.clean_documents_usecase()
    repository = clean_documents_integration_container.document_repository()
    # Créer un nouveau document à chaque fois pour éviter la réutilisation
    document = DocumentFactory.create_entity(document_type=DocumentType.OFFERS)
    return usecase, repository, document


@pytest.mark.parametrize(
    "document_type",
    [
        DocumentType.CORPS,
        DocumentType.CONCOURS,
        DocumentType.OFFERS,
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
    model_class = apps.get_model("shared", DOCUMENT_TYPE_MODEL_MAP[document_type])
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
    assert_raw_document_failed()


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


def test_clean_offers_mark_as_failed_error(db, raw_offer_setup):
    document_type = DocumentType.OFFERS
    clean_documents_usecase, document_repository, document = raw_offer_setup
    document.raw_data = {"data": "dummy"}
    document_repository.upsert_batch([document], document_type)

    with patch.object(
        document_repository,
        "mark_as_failed",
        side_effect=Exception(DB_ERROR),
    ) as mocked_method:
        with pytest.raises(Exception, match=DB_ERROR):
            clean_documents_usecase.execute(document_type)
        mocked_method.assert_called_once()

    assert_no_offer_cleaned()
    assert_raw_document_pending(processing=True)


@pytest.mark.parametrize(
    "category, expected",
    [
        ("CAT-AEF", "APLUS"),
        ("CAT-ESD", "APLUS"),
        ("CAT-ES", "APLUS"),
        ("CAT-A", "A"),
        ("CAT-B", "B"),
        ("CAT-C", "C"),
    ],
)
def test_execute_clean_offers_with_category(
    db, clean_documents_integration_container, offer_source, category, expected
):
    usecase = clean_documents_integration_container.clean_documents_usecase()
    document_repository = clean_documents_integration_container.document_repository()

    offer_dto = TalentsoftOfferFactory.build(
        customFields=TalentsoftCustomFieldsFactory.build(
            description=TalentsoftDescriptionCustomFieldsFactory.build(
                customCodeTable1=TalentsoftCustomCodeTableFactory.build(
                    clientCode=category
                )
            )
        )
    )

    document = DocumentFactory.create_entity(
        document_type=DocumentType.OFFERS, raw_data=offer_dto.model_dump()
    )

    document_repository.upsert_batch([document], DocumentType.OFFERS)

    result = usecase.execute(DocumentType.OFFERS)

    assert result["created"] == 1

    cleaned_offer = OfferModel.objects.first()
    assert cleaned_offer is not None
    assert cleaned_offer.category == expected


@pytest.mark.parametrize(
    (
        "area, country, region, department,"
        "expected_area, expected_country, expected_region, expected_department"
    ),
    [
        ("_TS_CO_GeographicalArea_Europe", "FRA", "R24", "41", "EU", "FRA", "24", "41"),
        ("_TS_CO_GeographicalArea_Europe", "FRA", "R11", "75", "EU", "FRA", "11", "75"),
        (
            "_TS_CO_GeographicalArea_Afrique",
            "FRA",
            "_TS_CO_Region_DOM",
            "971",
            "AF",
            "FRA",
            "DOM",
            "971",
        ),
        (
            "_TS_CO_GeographicalArea_AmriquesCaraibe",
            "FRA",
            "_TS_CO_Region_TOM",
            "987",
            "AM",
            "FRA",
            "TOM",
            "987",
        ),
        (
            "_TS_CO_GeographicalArea_Ocanie",
            "FRA",
            "R84",
            "_TS_CO_Department_NouvelleCaldonie988",
            "OC",
            "FRA",
            "84",
            "988",
        ),
    ],
)
def test_execute_clean_offers_with_geographical_area(
    db,
    clean_documents_integration_container,
    offer_source,
    area,
    country,
    region,
    department,
    expected_area,
    expected_country,
    expected_region,
    expected_department,
):
    usecase = clean_documents_integration_container.clean_documents_usecase()
    document_repository = clean_documents_integration_container.document_repository()

    offer_dto = TalentsoftOfferFactory.build(
        geographicalLocation=[
            TalentsoftCodedObjectFactory.build(
                clientCode=area, type="offerGeographicalLocation"
            )
        ],
        country=[
            TalentsoftCodedObjectFactory.build(clientCode=country, type="offerCountry")
        ],
        region=[
            TalentsoftCodedObjectFactory.build(clientCode=region, type="offerRegion")
        ],
        department=[
            TalentsoftCodedObjectFactory.build(
                clientCode=department, type="offerDepartment"
            )
        ],
    )

    document = DocumentFactory.create_entity(
        document_type=DocumentType.OFFERS, raw_data=offer_dto.model_dump()
    )

    document_repository.upsert_batch([document], DocumentType.OFFERS)

    result = usecase.execute(DocumentType.OFFERS)

    assert result["created"] == 1

    cleaned_offer = OfferModel.objects.first()
    assert cleaned_offer is not None
    assert cleaned_offer.area == expected_area
    assert cleaned_offer.country == expected_country
    assert cleaned_offer.region == expected_region
    assert cleaned_offer.department == expected_department


def test_execute_clean_offers_source_id(
    db, clean_documents_integration_container, offer_source
):
    usecase = clean_documents_integration_container.clean_documents_usecase()
    document_repository = clean_documents_integration_container.document_repository()

    document = DocumentFactory.create_entity(document_type=DocumentType.OFFERS)
    document_repository.upsert_batch([document], DocumentType.OFFERS)

    result = usecase.execute(DocumentType.OFFERS)

    assert result["created"] == 1

    cleaned_offer = OfferModel.objects.get()
    assert cleaned_offer.source_id == offer_source.source_id
