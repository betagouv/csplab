from datetime import datetime
from unittest.mock import MagicMock

import pytest

from application.ingestion.interfaces.list_offers_input import GetFilteredOffersInput
from config.app_config import AppConfig
from infrastructure.di.ingestion.ingestion_container import IngestionContainer
from infrastructure.di.shared.shared_container import SharedContainer
from infrastructure.gateways.shared.logger import LoggerService
from tests.factories.offer_factory import OfferFactory


@pytest.fixture(name="documents_integration_container")
def documents_integration_container_fixture(db):
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
    documents_integration_container, offers, active, external_id_contains, expected_keys
):
    input_data = GetFilteredOffersInput(
        active=active, external_id_contains=external_id_contains
    )
    result = documents_integration_container.list_offers_usecase().execute(
        input_data=input_data
    )

    assert {offer.external_id for offer in result.page._qs} == {
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
    documents_integration_container, offers, offset, limit, expected_keys
):
    input_data = GetFilteredOffersInput(active=True, external_id_contains=None)
    result = documents_integration_container.list_offers_usecase().execute(
        input_data=input_data
    )

    assert result.page.count() == len(["active_expected", "active_other"])

    sliced = list(result.page.slice(offset=offset, limit=limit))
    assert {offer.external_id for offer in sliced} == {
        offers[key].external_id for key in expected_keys
    }


def test_get_filtered_raises_error(db, documents_integration_container):
    shared_container = documents_integration_container.shared_container()
    offers_repo = shared_container.offers_repository()

    offers_repo.get_filtered_qs = MagicMock(side_effect=Exception("db error"))

    with pytest.raises(Exception, match="db error"):
        input_data = GetFilteredOffersInput(active=True, external_id_contains=None)
        documents_integration_container.list_offers_usecase().execute(
            input_data=input_data
        )
