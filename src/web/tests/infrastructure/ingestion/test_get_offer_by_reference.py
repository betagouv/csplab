import pytest
from referentiel.exceptions.offer_errors import OfferDoesNotExist

from application.ingestion.interfaces.get_offer_by_reference_input import (
    GetOfferByReferenceInput,
)
from infrastructure.factories.referentiel.offer_factory import OfferFactory


def test_returns_offer_matching_reference(db, ingestion_container):
    offer = OfferFactory.create_model(reference="REF-1")
    OfferFactory.create_model(reference="REF-2")

    input_data = GetOfferByReferenceInput(reference="REF-1")
    result = ingestion_container.get_offer_by_reference_usecase().execute(input_data)

    assert result.id == offer.id


def test_unknown_reference_raises(db, ingestion_container):
    input_data = GetOfferByReferenceInput(reference="UNKNOWN")

    with pytest.raises(OfferDoesNotExist):
        ingestion_container.get_offer_by_reference_usecase().execute(input_data)
