"""Unit test cases for MatchCVToOpportunitiesUsecase."""

import pytest

from domain.entities.concours import Concours
from domain.exceptions.cv_errors import CVProcessingFailedError
from infrastructure.di.candidate.candidate_container import CandidateContainer
from infrastructure.di.shared.shared_container import SharedContainer
from infrastructure.gateways.shared.logger import LoggerService
from tests.fixtures.fixture_loader import load_fixture
from tests.utils.in_memory_concours_repository import InMemoryConcoursRepository
from tests.utils.in_memory_cv_metadata_repository import InMemoryCVMetadataRepository
from tests.utils.in_memory_vector_repository import InMemoryVectorRepository
from tests.utils.mock_embedding_generator import MockEmbeddingGenerator


@pytest.fixture
def _candidate_container():
    """Create a test candidate container with minimal dependencies."""
    container = CandidateContainer()

    shared_container = SharedContainer()

    # Setup logger service for both containers
    logger_service = LoggerService()
    shared_container.logger_service.override(logger_service)

    concours_repo = InMemoryConcoursRepository()
    shared_container.concours_repository.override(concours_repo)

    embedding_fixtures = load_fixture("../fixtures/embedding_fixtures.json")
    embedding_generator = MockEmbeddingGenerator(embedding_fixtures)
    shared_container.embedding_generator.override(embedding_generator)

    vector_repo = InMemoryVectorRepository()
    shared_container.vector_repository.override(vector_repo)

    container.shared_container.override(shared_container)

    container.logger_service.override(logger_service)

    cv_repo = InMemoryCVMetadataRepository()
    container.postgres_cv_metadata_repository.override(cv_repo)

    return container


def test_execute_with_valid_cv_returns_concours(
    _candidate_container,
    cv_metadata_completed,
    concours,
    vectorized_concours_documents,
):
    """Test that valid CV metadata returns Concours with scores."""
    cv_metadata, cv_id = cv_metadata_completed

    # Setup CV metadata
    cv_repo = _candidate_container.postgres_cv_metadata_repository()
    cv_repo.save(cv_metadata)

    # Populate concours data
    concours_repo = _candidate_container.shared_container.concours_repository()
    concours_repo.upsert_batch(concours)

    # Populate vector data
    vector_repo = _candidate_container.shared_container.vector_repository()
    for vectorized_doc in vectorized_concours_documents:
        vector_repo.store_embedding(vectorized_doc)

    usecase = _candidate_container.match_cv_to_opportunities_usecase()
    result = usecase.execute(cv_metadata, limit=10)

    assert isinstance(result, list)
    assert len(result) > 0

    # Check result structure
    for c, score in result:
        assert isinstance(c, Concours)
        assert isinstance(score, float)
        assert 0.0 <= score <= 1.0


def test_execute_with_failed_cv_raises_error(_candidate_container, cv_metadata_failed):
    """Test that FAILED CV status raises CVProcessingFailedError."""
    cv_metadata, cv_id = cv_metadata_failed

    cv_repo = _candidate_container.postgres_cv_metadata_repository()
    cv_repo.save(cv_metadata)

    usecase = _candidate_container.match_cv_to_opportunities_usecase()

    with pytest.raises(CVProcessingFailedError) as exc_info:
        usecase.execute(cv_metadata, limit=10)

    assert exc_info.value.cv_id == str(cv_id)


def test_execute_respects_limit_parameter(
    _candidate_container,
    cv_metadata_completed,
    concours,
    vectorized_concours_documents,
):
    """Test that the limit parameter is respected."""
    cv_metadata, cv_id = cv_metadata_completed

    # Setup CV metadata
    cv_repo = _candidate_container.postgres_cv_metadata_repository()
    cv_repo.save(cv_metadata)

    # Populate concours data
    concours_repo = _candidate_container.shared_container.concours_repository()
    concours_repo.upsert_batch(concours)

    # Populate vector data
    vector_repo = _candidate_container.shared_container.vector_repository()
    for vectorized_doc in vectorized_concours_documents:
        vector_repo.store_embedding(vectorized_doc)

    usecase = _candidate_container.match_cv_to_opportunities_usecase()

    # Test with limit smaller than available concours
    result = usecase.execute(cv_metadata, limit=1)
    assert len(result) <= 1

    # Test with limit larger than available concours
    result = usecase.execute(cv_metadata, limit=10)
    assert len(result) <= len(concours)
