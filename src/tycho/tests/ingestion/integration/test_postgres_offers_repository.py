"""Integration tests for PostgresOffersRepository."""

import pytest

from infrastructure.repositories.shared.postgres_offers_repository import (
    PostgresOffersRepository,
)
from tests.fixtures.vectorize_test_factories import create_test_offer_for_integration


@pytest.mark.django_db
def test_find_by_id_not_found():
    """Test find_by_id returns None for non-existent offer."""
    repository = PostgresOffersRepository()

    result = repository.find_by_id(999999)  # Non-existent ID

    assert result is None


@pytest.mark.django_db
def test_find_by_id_success():
    """Test find_by_id returns offer when it exists."""
    repository = PostgresOffersRepository()

    # Create and save an offer
    offer = create_test_offer_for_integration(1)
    upsert_result = repository.upsert_batch([offer])
    assert upsert_result["created"] == 1
    assert upsert_result["errors"] == []

    # Find the offer
    found_offer = repository.find_by_id(offer.id)

    assert found_offer is not None
    assert found_offer.id == offer.id
    assert found_offer.external_id == offer.external_id
    assert found_offer.titre == offer.titre
