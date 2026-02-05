"""Unit test cases for MatchCVToOpportunitiesUsecase."""

from uuid import uuid4

import pytest

from domain.entities.concours import Concours
from domain.exceptions.cv_errors import (
    CVNotFoundError,
    CVProcessingFailedError,
    CVProcessingTimeoutError,
)
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

    concours_repo = InMemoryConcoursRepository()
    shared_container.concours_repository.override(concours_repo)

    embedding_fixtures = load_fixture("../fixtures/embedding_fixtures.json")
    embedding_generator = MockEmbeddingGenerator(embedding_fixtures)
    shared_container.embedding_generator.override(embedding_generator)

    vector_repo = InMemoryVectorRepository()
    shared_container.vector_repository.override(vector_repo)

    container.shared_container.override(shared_container)

    logger_service = LoggerService()
    container.logger_service.override(logger_service)

    cv_repo = InMemoryCVMetadataRepository()
    container.postgres_cv_metadata_repository.override(cv_repo)

    return container


def test_execute_with_valid_cv_returns_concours(
    _candidate_container,
    cv_metadata_completed,
    concours,
    vectorized_documents,
):
    """Test that valid CV ID returns Concours with scores."""
    cv_metadata, cv_id = cv_metadata_completed

    # Setup CV metadata
    cv_repo = _candidate_container.postgres_cv_metadata_repository()
    cv_repo.save(cv_metadata)

    # Populate concours data
    concours_repo = _candidate_container.shared_container.concours_repository()
    concours_repo.upsert_batch(concours)

    # Populate vector data
    vector_repo = _candidate_container.shared_container.vector_repository()
    for vectorized_doc in vectorized_documents:
        vector_repo.store_embedding(vectorized_doc)

    usecase = _candidate_container.match_cv_to_opportunities_usecase()
    result = usecase.execute(str(cv_id), limit=10)

    assert isinstance(result, list)
    assert len(result) > 0

    # Check result structure
    for c, score in result:
        assert isinstance(c, Concours)
        assert isinstance(score, float)
        assert 0.0 <= score <= 1.0


def test_execute_with_invalid_cv_id_raises_error(_candidate_container):
    """Test that invalid CV ID raises CVNotFoundError."""
    usecase = _candidate_container.match_cv_to_opportunities_usecase()
    invalid_cv_id = str(uuid4())

    with pytest.raises(CVNotFoundError) as exc_info:
        usecase.execute(invalid_cv_id, limit=10)

    assert exc_info.value.cv_id == invalid_cv_id


def test_execute_with_failed_cv_raises_error(_candidate_container, cv_metadata_failed):
    """Test that FAILED CV status raises CVProcessingFailedError."""
    cv_metadata, cv_id = cv_metadata_failed

    cv_repo = _candidate_container.postgres_cv_metadata_repository()
    cv_repo.save(cv_metadata)

    usecase = _candidate_container.match_cv_to_opportunities_usecase()

    with pytest.raises(CVProcessingFailedError) as exc_info:
        usecase.execute(str(cv_id), limit=10)

    assert exc_info.value.cv_id == str(cv_id)


def test_execute_respects_limit_parameter(
    _candidate_container,
    cv_metadata_completed,
    concours,
    vectorized_documents,
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
    for vectorized_doc in vectorized_documents:
        vector_repo.store_embedding(vectorized_doc)

    usecase = _candidate_container.match_cv_to_opportunities_usecase()

    # Test with limit smaller than available concours
    result = usecase.execute(str(cv_id), limit=1)
    assert len(result) <= 1

    # Test with limit larger than available concours
    result = usecase.execute(str(cv_id), limit=10)
    assert len(result) <= len(concours)


def test_execute_wait_for_completion_with_completed_cv(
    _candidate_container, cv_metadata_completed
):
    """Test wait_for_completion=True with already completed CV."""
    cv_metadata, cv_id = cv_metadata_completed

    cv_repo = _candidate_container.postgres_cv_metadata_repository()
    cv_repo.save(cv_metadata)

    usecase = _candidate_container.match_cv_to_opportunities_usecase()

    # Should return immediately since CV is already completed
    result = usecase.execute(str(cv_id), limit=10, wait_for_completion=True, timeout=5)
    assert isinstance(result, list)


def test_execute_wait_for_completion_timeout(_candidate_container, cv_metadata_initial):
    """Test wait_for_completion=True with timeout."""
    timeout_seconds = 2
    cv_metadata, cv_id = cv_metadata_initial  # PENDING status

    cv_repo = _candidate_container.postgres_cv_metadata_repository()
    cv_repo.save(cv_metadata)

    usecase = _candidate_container.match_cv_to_opportunities_usecase()

    # Should timeout since CV stays PENDING
    with pytest.raises(CVProcessingTimeoutError) as exc_info:
        usecase.execute(str(cv_id), limit=10, wait_for_completion=True, timeout=2)

    assert exc_info.value.cv_id == str(cv_id)
    assert exc_info.value.timeout == timeout_seconds


def test_execute_wait_for_completion_with_failed_cv(
    _candidate_container, cv_metadata_failed
):
    """Test wait_for_completion=True with CV that has failed processing."""
    cv_metadata, cv_id = cv_metadata_failed

    cv_repo = _candidate_container.postgres_cv_metadata_repository()
    cv_repo.save(cv_metadata)

    usecase = _candidate_container.match_cv_to_opportunities_usecase()

    # CV is already in FAILED status, should raise exception immediately
    with pytest.raises(CVProcessingFailedError) as exc_info:
        usecase.execute(str(cv_id), limit=10, wait_for_completion=True, timeout=5)

    assert exc_info.value.cv_id == str(cv_id)
