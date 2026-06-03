import pytest
from faker import Faker

from config.app_config import AppConfig
from domain.value_objects.opportunity_type import OpportunityType
from infrastructure.di.candidate.candidate_container import CandidateContainer
from infrastructure.di.shared.shared_container import SharedContainer
from infrastructure.gateways.shared.logger import LoggerService
from tests.factories.metier_factory import MetierFactory
from tests.factories.offer_factory import OfferFactory
from tests.factories.source_factory import SourceFactory
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


def test_execute_get_offer_details(db, candidate_container):
    source = SourceFactory.create_model()
    offer = OfferFactory.create_entity(
        family_code="ERJUR011", source_id=source.source_id
    )

    offers_repo = candidate_container.shared_container.offers_repository()
    offers_repo.upsert_batch([offer])

    MetierFactory.create_model(offer_family_code="ERJUR011")

    usecase = candidate_container.get_opportunity_details_usecase()
    result_offer, result_metiers = usecase.execute(
        opportunity_type=OpportunityType.OFFER, opportunity_id=offer.id
    )

    assert result_offer.id == offer.id
    assert len(result_metiers) == 1
    assert result_metiers[0].offer_family_code == offer.family_code
