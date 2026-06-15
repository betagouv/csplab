import uuid

from application.ingestion.interfaces.upsert_offers_input import (
    UpsertOffersInput,
)


def test_execute_returns_empty_list_when_no_sources(upsert_offers_usecase):
    input_data = UpsertOffersInput(source_id=uuid.uuid4(), offers=[])
    upsert_offers_usecase.execute(input_data=input_data)
    offers = upsert_offers_usecase.offers_repository.get_all()
    assert offers == []
