"""Unit test cases for MatchCVToOpportunitiesUsecase."""

from unittest.mock import patch

import pytest

from domain.entities.concours import Concours
from domain.entities.offer import Offer
from domain.exceptions.cv_errors import CVProcessingFailedError
from infrastructure.di.candidate.candidate_container import CandidateContainer
from infrastructure.di.shared.shared_container import SharedContainer
from infrastructure.gateways.shared.logger import LoggerService
from tests.fixtures.fixture_loader import load_fixture
from tests.utils.in_memory_concours_repository import InMemoryConcoursRepository
from tests.utils.in_memory_cv_metadata_repository import InMemoryCVMetadataRepository
from tests.utils.in_memory_offers_repository import InMemoryOffersRepository
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

    offers_repo = InMemoryOffersRepository()
    shared_container.offers_repository.override(offers_repo)

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


def test_execute_with_valid_cv_returns_opportunities(
    _candidate_container,
    cv_metadata_completed,
    concours,
    vectorized_concours_documents,
    offers,
    vectorized_offers_documents,
):
    """Test that valid CV metadata returns Concours with scores."""
    cv_metadata, cv_id = cv_metadata_completed

    # Setup CV metadata
    cv_repo = _candidate_container.postgres_cv_metadata_repository()
    cv_repo.save(cv_metadata)

    # Populate data
    concours_repo = _candidate_container.shared_container.concours_repository()
    concours_repo.upsert_batch(concours)

    offers_repo = _candidate_container.shared_container.offers_repository()
    offers_repo.upsert_batch(offers)

    # Populate vector data
    vector_repo = _candidate_container.shared_container.vector_repository()
    for vectorized_doc in vectorized_concours_documents + vectorized_offers_documents:
        vector_repo.store_embedding(vectorized_doc)

    usecase = _candidate_container.match_cv_to_opportunities_usecase()
    result = usecase.execute(cv_metadata, limit=10)

    assert isinstance(result, list)
    assert len(result) == len(
        vectorized_concours_documents + vectorized_offers_documents
    )

    assert sum(isinstance(obj, Concours) for obj, _ in result) == len(
        vectorized_concours_documents
    )
    assert sum(isinstance(obj, Offer) for obj, _ in result) == len(
        vectorized_offers_documents
    )
    # TODO - reactivate these assertions
    # assert all(0.0 <= score <= 1.0 for _, score in result)
    # assert all(isinstance(score, float) for _, score in result)


def test_execute_with_failed_cv_raises_error(_candidate_container, cv_metadata_failed):
    """Test that FAILED CV status raises CVProcessingFailedError."""
    cv_metadata, cv_id = cv_metadata_failed

    cv_repo = _candidate_container.postgres_cv_metadata_repository()
    cv_repo.save(cv_metadata)

    usecase = _candidate_container.match_cv_to_opportunities_usecase()

    with pytest.raises(CVProcessingFailedError) as exc_info:
        usecase.execute(cv_metadata, limit=10)

    assert exc_info.value.cv_id == str(cv_id)


@patch(
    "tests.utils.in_memory_vector_repository.InMemoryVectorRepository._cosine_similarity"
)
def test_execute_respects_sorting_and_limit_parameter(
    mock_method,
    _candidate_container,
    cv_metadata_completed,
    concours,
    vectorized_concours_documents,
    offers,
    vectorized_offers_documents,
):
    """Test that the limit parameter is respected and results are sorted by score."""
    # Mock scores for semantic_search calls
    # TO BE FIXED - semantic_search checks ALL vectorized documents
    # even when document_type is provided
    mock_method.side_effect = [i / 10 for i in range(10)]

    # setup data for the tests
    cv_metadata, cv_id = cv_metadata_completed

    cv_repo = _candidate_container.postgres_cv_metadata_repository()
    cv_repo.save(cv_metadata)

    concours_repo = _candidate_container.shared_container.concours_repository()
    concours_repo.upsert_batch(concours)

    offers_repo = _candidate_container.shared_container.offers_repository()
    offers_repo.upsert_batch(offers)

    vector_repo = _candidate_container.shared_container.vector_repository()
    for vectorized_doc in vectorized_concours_documents + vectorized_offers_documents:
        vector_repo.store_embedding(vectorized_doc)

    # case 1
    usecase = _candidate_container.match_cv_to_opportunities_usecase()

    result = usecase.execute(cv_metadata, limit=1)

    assert len(result) == 1
    assert result[0][1] == 0.4  # noqa

    # case 2
    result = usecase.execute(cv_metadata, limit=10)
    scores = [score for _, score in result]

    assert len(result) == len(concours) + len(offers)
    assert scores == sorted(scores, reverse=True)
