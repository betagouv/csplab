from unittest.mock import MagicMock

import pytest

from application.ingestion.usecases.archive_offer_by_reference import (
    ArchiveOfferByReferenceUseCase,
)
from domain.exceptions.offer_errors import OfferDoesNotExist
from tests.factories.offer_factory import OfferFactory
from tests.utils.in_memory_offers_repository import InMemoryOffersRepository

REFERENCE = "12345"


@pytest.fixture
def offers_repository():
    return InMemoryOffersRepository()


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
    def test_archives_offer_by_reference(self, use_case, offers_repository):
        offers_repository.upsert_batch(
            [OfferFactory.create_entity(external_id=f"Versant_FPE-{REFERENCE}")]
        )
        use_case.execute(REFERENCE)
        offer = offers_repository.get_by_reference(REFERENCE)
        assert offer.archived_at is not None

    def test_deletes_vectors_for_offer(
        self, use_case, offers_repository, vector_repository
    ):
        offer = OfferFactory.create_entity(external_id=f"Versant_FPE-{REFERENCE}")
        offers_repository.upsert_batch([offer])
        use_case.execute(REFERENCE)
        vector_repository.delete_vectorized_documents.assert_called_once_with(
            [offer.id]
        )

    def test_raises_when_reference_not_found(self, use_case):
        with pytest.raises(OfferDoesNotExist):
            use_case.execute("unknown-ref")
