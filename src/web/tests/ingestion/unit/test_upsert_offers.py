from unittest.mock import MagicMock

from application.ingestion.interfaces.upsert_offers_input import (
    UpsertOffersInput,
)


def test_execute_returns_empty_list_when_no_sources(upsert_offers_usecase):
    upsert_offers_usecase.offers_repository.upsert_batch = MagicMock(
        return_value={"created": 0, "updated": 0, "errors": []}
    )

    input_data = UpsertOffersInput(offers=[])
    upsert_offers_usecase.execute(input_data=input_data)
    upsert_offers_usecase.offers_repository.upsert_batch.assert_called_once()
