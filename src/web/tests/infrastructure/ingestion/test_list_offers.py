from datetime import datetime
from unittest.mock import MagicMock

import pytest

from application.ingestion.interfaces.list_offers_input import GetFilteredOffersInput
from infrastructure.factories.referentiel.offer_factory import OfferFactory


@pytest.fixture(name="offers")
def offers_fixture(db):
    return {
        "archived_expected": OfferFactory.create_model(
            external_id="test-expected-archived", archived_at=datetime.now()
        ),
        "archived_other": OfferFactory.create_model(
            external_id="test-other-archived", archived_at=datetime.now()
        ),
        "active_expected": OfferFactory.create_model(
            external_id="test-expected-active"
        ),
        "active_other": OfferFactory.create_model(external_id="test-other-active"),
    }


@pytest.mark.parametrize(
    "active, external_id_contains, expected_keys",
    [
        pytest.param(True, "unknown", [], id="empty_result"),
        pytest.param(
            True, None, ["active_expected", "active_other"], id="all_active_offers"
        ),
        pytest.param(
            True,
            "expected",
            ["active_expected"],
            id="active_offers_containing_expected",
        ),
        pytest.param(
            False,
            None,
            ["archived_expected", "archived_other"],
            id="all_archived_offers",
        ),
        pytest.param(
            False,
            "expected",
            ["archived_expected"],
            id="archived_offers_containing_expected",
        ),
    ],
)
def test_list_offers_result(
    ingestion_container, offers, active, external_id_contains, expected_keys
):
    input_data = GetFilteredOffersInput(
        active=active, external_id_contains=external_id_contains
    )
    result = ingestion_container.list_offers_usecase().execute(input_data=input_data)

    assert {offer.external_id for offer in result._qs} == {
        offers[key].external_id for key in expected_keys
    }


@pytest.mark.parametrize(
    "offset,limit,expected_keys",
    [
        pytest.param(0, 1, ["active_other"], id="sliced"),
        pytest.param(0, 2, ["active_expected", "active_other"], id="sliced_all"),
        pytest.param(10, 10, [], id="sliced_out_of_bounds"),
    ],
)
def test_list_offers_page_slice(
    ingestion_container, offers, offset, limit, expected_keys
):
    input_data = GetFilteredOffersInput(active=True, external_id_contains=None)
    result = ingestion_container.list_offers_usecase().execute(input_data=input_data)

    assert result.count() == len(["active_expected", "active_other"])

    sliced = list(result.slice(offset=offset, limit=limit))
    assert {offer.external_id for offer in sliced} == {
        offers[key].external_id for key in expected_keys
    }


def test_get_filtered_raises_error(db, ingestion_container):
    shared_container = ingestion_container.shared_container()
    offers_repo = shared_container.offers_repository()

    offers_repo.get_filtered = MagicMock(side_effect=Exception("db error"))

    with pytest.raises(Exception, match="db error"):
        input_data = GetFilteredOffersInput(active=True, external_id_contains=None)
        ingestion_container.list_offers_usecase().execute(input_data=input_data)
