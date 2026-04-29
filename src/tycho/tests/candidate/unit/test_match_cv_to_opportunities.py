from unittest.mock import AsyncMock, Mock

import pytest

from application.candidate.usecases.match_cv_to_opportunities import (
    MatchCVToOpportunitiesUsecase,
)
from domain.exceptions.cv_errors import CVProcessingFailedError
from domain.value_objects.cv_processing_status import CVStatus
from infrastructure.gateways.shared.logger import LoggerService
from tests.factories.cv_metadata_factory import CVMetadataFactory
from tests.utils.in_memory_concours_repository import InMemoryConcoursRepository
from tests.utils.in_memory_cv_metadata_repository import InMemoryCVMetadataRepository
from tests.utils.in_memory_offers_repository import InMemoryOffersRepository
from tests.utils.in_memory_vector_repository import InMemoryVectorRepository


@pytest.fixture
def match_cv_to_opportunities():

    logger_service = LoggerService()

    embedding_generator_mock = Mock()
    embedding_generator_mock.generate_embedding = AsyncMock(
        return_value=[0.1, 0.2, 0.3]
    )
    concours_repo = InMemoryConcoursRepository()
    offers_repo = InMemoryOffersRepository()
    cv_repo = InMemoryCVMetadataRepository()
    vector_repo = InMemoryVectorRepository(logger=logger_service)

    usecase = MatchCVToOpportunitiesUsecase(
        postgres_cv_metadata_repository=cv_repo,
        embedding_generator=embedding_generator_mock,
        vector_repository=vector_repo,
        concours_repository=concours_repo,
        offers_repository=offers_repo,
        logger=logger_service,
    )

    return usecase, cv_repo


def test_execute_with_failed_cv_raises_error(match_cv_to_opportunities):
    cv_metadata = CVMetadataFactory.create_entity(status=CVStatus.FAILED)

    usecase, cv_repo = match_cv_to_opportunities
    cv_repo.save(cv_metadata)

    with pytest.raises(CVProcessingFailedError) as exc_info:
        usecase.execute(cv_metadata, limit=10)

    assert exc_info.value.cv_id == str(cv_metadata.id)
