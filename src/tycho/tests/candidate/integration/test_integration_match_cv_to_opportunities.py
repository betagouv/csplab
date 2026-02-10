"""Integration test cases for MatchCVToOpportunitiesUsecase."""

import pytest

from domain.entities.concours import Concours
from infrastructure.di.candidate.candidate_container import CandidateContainer
from infrastructure.di.shared.shared_container import SharedContainer
from infrastructure.gateways.shared.logger import LoggerService
from tests.fixtures.fixture_loader import load_fixture
from tests.utils.mock_embedding_generator import MockEmbeddingGenerator


@pytest.fixture
def _integration_candidate_container():
    """Create a test candidate container for integration tests with real DB."""
    container = CandidateContainer()

    # Setup shared container with real repositories (except embedding generator)
    shared_container = SharedContainer()

    # Add logger service to shared container
    logger_service = LoggerService()
    shared_container.logger_service.override(logger_service)

    # Use mock embedding generator for consistent test results
    embedding_fixtures = load_fixture("../fixtures/embedding_fixtures.json")
    embedding_generator = MockEmbeddingGenerator(embedding_fixtures)
    shared_container.embedding_generator.override(embedding_generator)

    container.shared_container.override(shared_container)

    # Setup logger for candidate container too
    container.logger_service.override(logger_service)

    return container


@pytest.mark.django_db
def test_execute_with_valid_cv_returns_concours(
    _integration_candidate_container,
    cv_metadata_completed,
    concours,
    vectorized_concours_documents,
):
    """Test that valid CV metadata returns Concours with scores using real DB."""
    cv_metadata, cv_id = cv_metadata_completed

    # Setup CV metadata in real DB
    cv_repo = _integration_candidate_container.postgres_cv_metadata_repository()
    cv_repo.save(cv_metadata)

    # Populate concours data in real DB
    concours_repo = (
        _integration_candidate_container.shared_container.concours_repository()
    )
    concours_repo.upsert_batch(concours)

    # Populate vector data in real DB
    vector_repo = _integration_candidate_container.shared_container.vector_repository()
    for vectorized_doc in vectorized_concours_documents:
        vector_repo.store_embedding(vectorized_doc)

    usecase = _integration_candidate_container.match_cv_to_opportunities_usecase()
    result = usecase.execute(cv_metadata, limit=10)

    assert isinstance(result, list)
    assert len(result) > 0

    # Check result structure
    for c, score in result:
        assert isinstance(c, Concours)
        assert isinstance(score, float)
