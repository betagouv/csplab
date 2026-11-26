import pytest
from faker import Faker

from config.app_config import AppConfig
from domain.candidate.value_objects.opportunity_type import OpportunityType
from infrastructure.di.candidate.candidate_container import CandidateContainer
from infrastructure.di.shared.shared_container import SharedContainer
from infrastructure.factories.referentiel.metier_django_factory import (
    MetierDjangoFactory,
)
from infrastructure.factories.referentiel.offer_django_factory import (
    OfferDjangoFactory,
)
from infrastructure.gateways.shared.logger import LoggerService
from tests.utils.shared_fixtures import (
    create_shared_qdrant_repository,
)

fake = Faker()


@pytest.fixture
def candidate_container():
    shared_qdrant_repository = create_shared_qdrant_repository()

    container = CandidateContainer()

    shared_container = SharedContainer()

    app_config = AppConfig.from_django_settings()
    shared_container.app_config.override(app_config)

    logger_service = LoggerService()
    shared_container.logger_service.override(logger_service)

    shared_container.vector_repository.override(shared_qdrant_repository)

    container.shared_container.override(shared_container)

    container.app_config.override(app_config)
    container.logger_service.override(logger_service)

    return container


@pytest.fixture
def test_app_config(candidate_container):
    return candidate_container.app_config()


@pytest.mark.parametrize(
    ("offer_family_code", "metier_family_code", "expected_metiers_count"),
    [
        pytest.param("ERJUR011", "ERJUR011", 1, id="nominal_case"),
        pytest.param(None, "ERJUR011", 0, id="no_family_code"),
        pytest.param("ERJUR011", "ERJUR022", 0, id="no_matching_metiers"),
    ],
)
def test_execute_get_offer_details(
    db,
    candidate_container,
    offer_family_code,
    metier_family_code,
    expected_metiers_count,
):
    offer = OfferDjangoFactory(code_emploi_csp=offer_family_code)
    MetierDjangoFactory(offer_family_code=metier_family_code)

    usecase = candidate_container.get_opportunity_details_usecase()
    result_offer, result_metiers = usecase.execute(
        opportunity_type=OpportunityType.OFFER, opportunity_id=offer.id
    )

    assert result_offer.id == offer.id
    assert [metier.offer_family_code for metier in result_metiers] == [
        metier_family_code
    ] * expected_metiers_count
