from unittest.mock import MagicMock

import pytest
from faker import Faker

from application.ingestion.interfaces.archive_offer_by_reference_input import (
    ArchiveOfferByReferenceInput,
)
from application.ingestion.usecases.archive_offer_by_reference import (
    ArchiveOfferByReferenceUseCase,
)
from domain.exceptions.offer_errors import OfferDoesNotExist
from infrastructure.gateways.shared.logger import LoggerService
from infrastructure.repositories.shared.postgres_offers_repository import (
    PostgresOffersRepository,
)
from tests.factories.offer_factory import OfferFactory

fake = Faker()

REFERENCE = fake.bothify("REF-####")
SOURCE_ID = str(fake.uuid4())


@pytest.fixture
def offers_repository():
    return PostgresOffersRepository(LoggerService())


@pytest.fixture
def vector_repository():
    mock = MagicMock()
    mock.delete_vectorized_documents.return_value = {"deleted": 1, "errors": []}
    return mock


@pytest.fixture
def use_case(offers_repository, vector_repository):
    return ArchiveOfferByReferenceUseCase(
        offers_repository=offers_repository,
        vector_repository=vector_repository,
    )


class TestArchiveOfferByReferenceUseCase:
    def test_archives_offer_by_reference(self, db, use_case, offers_repository):
        OfferFactory.create_model(
            external_id=f"Versant_FPE-{REFERENCE}", source_id=SOURCE_ID
        )
        use_case.execute(
            ArchiveOfferByReferenceInput(reference=REFERENCE, source_id=SOURCE_ID)
        )
        offer = offers_repository.get_by_reference_and_source_id(REFERENCE, SOURCE_ID)
        assert offer.archived_at is not None

    def test_deletes_vectors_for_offer(self, db, use_case, vector_repository):
        offer = OfferFactory.create_model(
            external_id=f"Versant_FPE-{REFERENCE}", source_id=SOURCE_ID
        ).to_entity()
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
