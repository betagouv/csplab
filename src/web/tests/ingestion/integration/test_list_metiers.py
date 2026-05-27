from unittest.mock import MagicMock

import pytest

from application.ingestion.interfaces.list_metiers_input import GetFilteredMetiersInput
from config.app_config import AppConfig
from infrastructure.di.ingestion.ingestion_container import IngestionContainer
from infrastructure.di.shared.shared_container import SharedContainer
from infrastructure.gateways.shared.logger import LoggerService
from tests.factories.metier_factory import MetierFactory


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


@pytest.fixture(name="metiers")
def metiers_fixture(db):
    return {
        "TRE1": MetierFactory.create_model(
            domaine_fonctionnel_code="TRE", offer_family_code="TRE00001"
        ),
        "TRE2": MetierFactory.create_model(
            domaine_fonctionnel_code="TRE", offer_family_code="TRE00002"
        ),
        "AFK1": MetierFactory.create_model(
            domaine_fonctionnel_code="AFK", offer_family_code="AFK00001"
        ),
    }


@pytest.mark.parametrize(
    "domain, expected_keys",
    [
        pytest.param(None, ["TRE1", "TRE2", "AFK1"], id="all"),
        pytest.param("TRE", ["TRE1", "TRE2"], id="TRE"),
        pytest.param("ABC", [], id="empty_result"),
    ],
)
def test_list_metiers_result(
    documents_integration_container, metiers, domain, expected_keys
):
    input_data = GetFilteredMetiersInput(domain=domain)
    result = documents_integration_container.list_metiers_usecase().execute(
        input_data=input_data
    )

    assert {metier.external_id for metier in result._qs} == {
        metiers[key].external_id for key in expected_keys
    }


@pytest.mark.parametrize(
    "offset,limit,expected_keys",
    [
        pytest.param(0, 1, ["AFK1"], id="sliced"),
        pytest.param(0, 4, ["AFK1", "TRE1", "TRE2"], id="sliced_all"),
        pytest.param(10, 10, [], id="sliced_out_of_bounds"),
    ],
)
def test_list_metiers_page_slice(
    documents_integration_container, metiers, offset, limit, expected_keys
):
    input_data = GetFilteredMetiersInput(domain=None)
    result = documents_integration_container.list_metiers_usecase().execute(
        input_data=input_data
    )

    assert result.count() == len(["AFK1", "TRE1", "TRE2"])

    sliced = list(result.slice(offset=offset, limit=limit))
    assert {metier.external_id for metier in sliced} == {
        metiers[key].external_id for key in expected_keys
    }


def test_get_filtered_slice_raises_error(db, documents_integration_container):
    shared_container = documents_integration_container.shared_container()
    metiers_repo = shared_container.metiers_repository()

    metiers_repo.get_filtered_slice = MagicMock(side_effect=Exception("db error"))

    with pytest.raises(Exception, match="db error"):
        input_data = GetFilteredMetiersInput(domain=None)
        documents_integration_container.list_metiers_usecase().execute(
            input_data=input_data
        )
