from random import random

import pytest
from faker import Faker
from pytest_django.asserts import assertNumQueries

from domain.entities.concours import Concours
from domain.entities.document import DocumentType
from domain.entities.vectorized_document import VectorizedDocument
from infrastructure.di.candidate.candidate_container import CandidateContainer
from infrastructure.di.shared.shared_container import SharedContainer
from infrastructure.gateways.shared.logger import LoggerService
from tests.factories.concours_factory import ConcoursFactory
from tests.factories.offer_factory import OfferFactory
from tests.fixtures.fixture_loader import load_fixture
from tests.utils.mock_embedding_generator import MockEmbeddingGenerator

fake = Faker()


@pytest.fixture
def _integration_candidate_container():
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
    return [
        VectorizedDocument(
            entity_id=obj.id,
            document_type=DocumentType.CONCOURS
            if isinstance(obj, Concours)
            else DocumentType.OFFERS,
            content=fake.word(),
            embedding=[0.2 + random() / 10000] * 3072,
            metadata={"source": "test"},
        )
        for obj in documents
    ]


def test_execute_with_valid_cv_returns_opportunities(
    db,
    _integration_candidate_container,
    cv_metadata_completed,
):
    cv_metadata, cv_id = cv_metadata_completed
    concours = ConcoursFactory.create_batch(2)
    offers = OfferFactory.create_batch(3)
    limit = len(offers) + len(concours) - 1

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
    vectorized_concours = generate_vectorized_documents(concours_repo.get_all())
    vectorized_offers = generate_vectorized_documents(offers_repo.get_all())

    # Populate vector data in real DB
    vector_repo = _integration_candidate_container.shared_container.vector_repository()
    vector_repo.upsert_batch(vectorized_concours, DocumentType.CONCOURS.value)
    vector_repo.upsert_batch(vectorized_offers, DocumentType.OFFERS.value)

    usecase = _integration_candidate_container.match_cv_to_opportunities_usecase()
    with assertNumQueries(
        1  # select VectorizedDocument
        + 1  # select ConcoursModel
        + 1  # select OfferModel
    ):
        results = usecase.execute(cv_metadata, limit=limit)

    assert isinstance(results, list)
    assert len(results) == limit

    similarities = [score for _, score in results]
    assert sorted(similarities, reverse=True) == similarities

    assert all(0.0 <= score <= 1 for score in similarities)
    assert all(isinstance(score, float) for score in similarities)
