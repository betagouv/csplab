import pytest

from config.app_config import AppConfig
from domain.exceptions.cv_errors import CVProcessingFailedError
from domain.value_objects.cv_processing_status import CVStatus
from infrastructure.di.candidate.candidate_container import CandidateContainer
from infrastructure.di.shared.shared_container import SharedContainer
from infrastructure.gateways.shared.logger import LoggerService
from tests.factories.cv_metadata_factory import create_cv_metadata_initial
from tests.utils.in_memory_concours_repository import InMemoryConcoursRepository
from tests.utils.in_memory_cv_metadata_repository import InMemoryCVMetadataRepository
from tests.utils.in_memory_offers_repository import InMemoryOffersRepository


@pytest.fixture
def candidate_container():
    container = CandidateContainer()

    shared_container = SharedContainer()

    app_config = AppConfig.from_django_settings()
    shared_container.app_config.override(app_config)

    logger_service = LoggerService()
    shared_container.logger_service.override(logger_service)

    concours_repo = InMemoryConcoursRepository()
    shared_container.concours_repository.override(concours_repo)

    offers_repo = InMemoryOffersRepository()
    shared_container.offers_repository.override(offers_repo)

    cv_repo = InMemoryCVMetadataRepository()
    container.postgres_cv_metadata_repository.override(cv_repo)

    container.shared_container.override(shared_container)

    container.app_config.override(app_config)
    container.logger_service.override(logger_service)

    return container


@pytest.fixture(name="cv_metadata_initial")
def cv_metadata_initial_fixture():
    return create_cv_metadata_initial()


@pytest.fixture(name="cv_metadata_failed")
def cv_metadata_failed_fixture(cv_metadata_initial):
    cv_metadata, cv_id = cv_metadata_initial
    cv_metadata.status = CVStatus.FAILED
    return cv_metadata, cv_id


def test_execute_with_failed_cv_raises_error(candidate_container, cv_metadata_failed):
    cv_metadata, cv_id = cv_metadata_failed

    cv_repo = candidate_container.postgres_cv_metadata_repository()
    cv_repo.save(cv_metadata)

    usecase = candidate_container.match_cv_to_opportunities_usecase()

    with pytest.raises(CVProcessingFailedError) as exc_info:
        usecase.execute(cv_metadata, limit=10)

    assert exc_info.value.cv_id == str(cv_id)
