"""Integration test cases for MatchCVToOpportunitiesUsecase."""

from datetime import datetime, timezone

import pytest
from faker import Faker

from domain.entities.concours import Concours
from domain.entities.document import DocumentType
from domain.entities.offer import Offer
from domain.entities.vectorized_document import VectorizedDocument
from infrastructure.di.candidate.candidate_container import CandidateContainer
from infrastructure.di.shared.shared_container import SharedContainer
from infrastructure.gateways.shared.logger import LoggerService
from tests.fixtures.fixture_loader import load_fixture
from tests.utils.mock_embedding_generator import MockEmbeddingGenerator

fake = Faker()


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


def generate_vectorized_documents(documents):
    """Generate vectorized docs using entity UUID."""
    return [
        VectorizedDocument(
            entity_id=obj.id,
            document_type=DocumentType.CONCOURS
            if isinstance(obj, Concours)
            else DocumentType.OFFERS,
            content=fake.word(),
            embedding=[0.2] * 3072,  # Mock embedding
            metadata={"source": "test"},
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        for obj in documents
    ]


@pytest.mark.django_db
def test_execute_with_valid_cv_returns_opportunities(
    _integration_candidate_container,
    cv_metadata_completed,
    concours,
    offers,
):
    """Test that valid CV metadata returns Concours/Offers with scores using real DB."""
    cv_metadata, cv_id = cv_metadata_completed

    # Setup CV metadata in real DB
    cv_repo = _integration_candidate_container.postgres_cv_metadata_repository()
    cv_repo.save(cv_metadata)

    # Populate concours data in real DB
    concours_repo = (
        _integration_candidate_container.shared_container.concours_repository()
    )
    concours_repo.upsert_batch(concours)

    offers_repo = _integration_candidate_container.shared_container.offers_repository()
    offers_repo.upsert_batch(offers)

    # Generate vectorized documents using entity UUIDs
    vectorized_documents = generate_vectorized_documents(
        concours_repo.get_all() + offers_repo.get_all()
    )

    # Populate vector data in real DB
    vector_repo = _integration_candidate_container.shared_container.vector_repository()
    for vectorized_doc in vectorized_documents:
        vector_repo.store_embedding(vectorized_doc)

    usecase = _integration_candidate_container.match_cv_to_opportunities_usecase()
    result = usecase.execute(cv_metadata, limit=10)

    assert isinstance(result, list)
    assert len(result) == len(vectorized_documents)

    assert sum(isinstance(obj, Concours) for obj, _ in result) == len(concours)
    assert sum(isinstance(obj, Offer) for obj, _ in result) == len(offers)
    # TODO - reactivate these assertions
    # assert all(0.0 <= score <= 1.0 for _, score in result)
    # assert all(isinstance(score, float) for _, score in result)
