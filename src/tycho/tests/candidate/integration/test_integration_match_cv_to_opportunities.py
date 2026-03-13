import pytest
from faker import Faker
from pytest_django.asserts import assertNumQueries
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams

from config.app_config import AppConfig, QdrantConfig
from domain.entities.document import DocumentType
from infrastructure.di.candidate.candidate_container import CandidateContainer
from infrastructure.di.shared.shared_container import SharedContainer
from infrastructure.gateways.shared.logger import LoggerService
from infrastructure.repositories.shared.qdrant_repository import QdrantRepository
from tests.factories.concours_factory import ConcoursFactory
from tests.factories.offer_factory import OfferFactory
from tests.factories.vectorized_document_factory import VectorizedDocumentFactory
from tests.fixtures.fixture_loader import load_fixture
from tests.utils.mock_embedding_generator import MockEmbeddingGenerator

fake = Faker()


@pytest.fixture
def _integration_candidate_container():

    container = CandidateContainer()

    # Setup shared container with real repositories (except embedding generator)
    shared_container = SharedContainer()

    # Add app config to shared container (MISSING BEFORE!)
    app_config = AppConfig.from_django_settings()
    shared_container.app_config.override(app_config)

    # Add logger service to shared container
    logger_service = LoggerService()
    shared_container.logger_service.override(logger_service)

    # Use mock embedding generator for consistent test results
    embedding_fixtures = load_fixture("../fixtures/embedding_fixtures.json")
    embedding_generator = MockEmbeddingGenerator(embedding_fixtures)
    shared_container.embedding_generator.override(embedding_generator)

    # Create Qdrant repository with in-memory client like ingestion tests
    qdrant_config = QdrantConfig(
        url=None,
        api_key="",
        timeout=30,
        prefer_grpc=False,
    )
    qdrant_repo = QdrantRepository(qdrant_config, logger_service)
    qdrant_repo.client = QdrantClient(":memory:")

    # Create test collection with simple vector config
    qdrant_repo.client.create_collection(
        collection_name=qdrant_repo.collection_name,
        vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
    )

    # Override vector repository with our configured Qdrant
    shared_container.vector_repository.override(qdrant_repo)

    container.shared_container.override(shared_container)

    # Setup app config and logger for candidate container too
    container.app_config.override(app_config)
    container.logger_service.override(logger_service)

    return container


@pytest.mark.django_db
def test_execute_with_valid_cv_returns_opportunities(
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

    # Generate vectorized documents using VectorizedDocumentFactory
    vectorized_concours = []
    for concours_entity in concours_repo.get_all():
        vectorized_doc = VectorizedDocumentFactory.create(
            entity_id=concours_entity.id,
            document_type=DocumentType.CONCOURS,
            content=fake.sentence(),
            embedding_dimensions=1536,  # Use 1536 for Qdrant compatibility
        )
        vectorized_concours.append(vectorized_doc)

    vectorized_offers = []
    for offer_entity in offers_repo.get_all():
        vectorized_doc = VectorizedDocumentFactory.create(
            entity_id=offer_entity.id,
            document_type=DocumentType.OFFERS,
            content=fake.sentence(),
            embedding_dimensions=1536,
        )
        vectorized_offers.append(vectorized_doc)

    # Populate vector data in real DB
    vector_repo = _integration_candidate_container.shared_container.vector_repository()
    vector_repo.upsert_batch(vectorized_concours, DocumentType.CONCOURS)
    vector_repo.upsert_batch(vectorized_offers, DocumentType.OFFERS)

    usecase = _integration_candidate_container.match_cv_to_opportunities_usecase()
    with assertNumQueries(
        1  # select ConcoursModel
        + 1  # select OfferModel
    ):
        results = usecase.execute(cv_metadata, limit=limit)

    assert isinstance(results, list)
    assert len(results) == limit

    similarities = [r[1] for r in results]
    assert sorted(similarities, reverse=True) == similarities

    # TODO - reactivate these assertions
    # assert all(0.0 <= score <= 1.0 for _, score in result)
    # assert all(isinstance(score, float) for _, score in result)
