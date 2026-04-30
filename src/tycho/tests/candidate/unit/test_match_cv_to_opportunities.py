from typing import cast
from unittest.mock import AsyncMock, Mock

import pytest

from application.candidate.usecases.match_cv_to_opportunities import (
    MatchCVToOpportunitiesUsecase,
)
from domain.exceptions.cv_errors import CVProcessingFailedError
from domain.repositories.concours_repository_interface import IConcoursRepository
from domain.repositories.cv_metadata_repository_interface import ICVMetadataRepository
from domain.repositories.offers_repository_interface import IOffersRepository
from domain.repositories.vector_repository_interface import IVectorRepository
from domain.value_objects.cv_processing_status import CVStatus
from infrastructure.gateways.shared.logger import LoggerService
from tests.factories.cv_metadata_factory import CVMetadataFactory
from tests.utils.interface_aware_mock import create_interface_aware_mock


@pytest.fixture
def match_cv_to_opportunities():

    logger_service = LoggerService()

    embedding_generator_mock = Mock()
    embedding_generator_mock.generate_embedding = AsyncMock(
        return_value=[0.1, 0.2, 0.3]
    )
    concours_repo = cast(
        IConcoursRepository, create_interface_aware_mock(IConcoursRepository)
    )
    offers_repo = cast(
        IOffersRepository, create_interface_aware_mock(IOffersRepository)
    )
    cv_repo = cast(
        ICVMetadataRepository, create_interface_aware_mock(ICVMetadataRepository)
    )
    vector_repo = cast(
        IVectorRepository, create_interface_aware_mock(IVectorRepository)
    )

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
