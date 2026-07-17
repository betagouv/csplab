from unittest.mock import MagicMock
from uuid import UUID

import pytest
from faker import Faker
from referentiel.exceptions.offer_errors import OfferDoesNotExist

from application.ingestion.interfaces.archive_offer_by_reference_input import (
    ArchiveOfferByReferenceInput,
)
from config.app_config import AppConfig
from infrastructure.di.ingestion.ingestion_container import IngestionContainer
from infrastructure.di.shared.shared_container import SharedContainer
from infrastructure.factories.referentiel.offer_factory import OfferFactory
from infrastructure.gateways.shared.logger import LoggerService
from infrastructure.mappers.offer_mapper import OfferMapper
from infrastructure.repositories.shared.postgres_offers_repository import (
    PostgresOffersRepository,
)

_mapper = OfferMapper()

fake = Faker()

REFERENCE = fake.bothify("REF-####")
SOURCE_ID = UUID(fake.uuid4())


@pytest.fixture
def offers_repository():
    return PostgresOffersRepository(LoggerService(), _mapper)


@pytest.fixture
def vector_repository():
    mock = MagicMock()
    mock.delete_vectorized_documents.return_value = {"deleted": 1, "errors": []}
    return mock


@pytest.fixture
def use_case(db, vector_repository):
    shared_container = SharedContainer()
    app_config = AppConfig.from_django_settings()
    logger_service = LoggerService()
    shared_container.app_config.override(app_config)
    shared_container.logger_service.override(logger_service)
    shared_container.vector_repository.override(vector_repository)
    shared_container.embedding_generator.override(MagicMock())

    container = IngestionContainer()
    container.app_config.override(app_config)
    container.logger_service.override(logger_service)
    container.shared_container.override(shared_container)
    return container.archive_offer_by_reference_usecase()


class TestArchiveOfferByReferenceUseCase:
    def test_archives_offer_by_reference(self, db, use_case, offers_repository):
        OfferFactory.create_model(reference=REFERENCE, source_id=SOURCE_ID)
        use_case.execute(
            ArchiveOfferByReferenceInput(reference=REFERENCE, source_id=SOURCE_ID)
        )
        offer = offers_repository.get_by_reference_and_source_id(REFERENCE, SOURCE_ID)
        assert offer.archived_at is not None

    def test_deletes_vectors_for_offer(self, db, use_case, vector_repository):
        offer = _mapper.to_domain(
            OfferFactory.create_model(reference=REFERENCE, source_id=SOURCE_ID)
        )
        use_case.execute(
            ArchiveOfferByReferenceInput(reference=REFERENCE, source_id=SOURCE_ID)
        )
        vector_repository.delete_vectorized_documents.assert_called_once_with(
            [offer.id]
        )

    def test_raises_when_reference_not_found(self, db, use_case):
        with pytest.raises(OfferDoesNotExist):
            use_case.execute(
                ArchiveOfferByReferenceInput(
                    reference="unknown-ref", source_id=SOURCE_ID
                )
            )
