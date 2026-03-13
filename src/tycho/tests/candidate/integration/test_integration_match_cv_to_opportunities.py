import pytest
from faker import Faker
from pytest_django.asserts import assertNumQueries
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams

from config.app_config import AppConfig, QdrantConfig
from domain.entities.concours import Concours
from domain.entities.document import DocumentType
from domain.entities.vectorized_document import VectorizedDocument
from infrastructure.di.candidate.candidate_container import CandidateContainer
from infrastructure.di.shared.shared_container import SharedContainer
from infrastructure.gateways.shared.logger import LoggerService
from infrastructure.repositories.shared.qdrant_repository import QdrantRepository
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
        url="http://localhost:6333",
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


def generate_vectorized_documents(documents):
    vectorized_docs = []
    for obj in documents:
        if isinstance(obj, Concours):
            doc_type = DocumentType.CONCOURS
            metadata = {
                "category": obj.category,
                "ministry": obj.ministry,
                "access_modality": obj.access_modality or [],
            }
        else:
            doc_type = DocumentType.OFFERS
            metadata = {
                "verse": obj.verse.value if obj.verse else "FPE",
                "contract_type": obj.contract_type.value if obj.contract_type else None,
                "localisation": str(obj.localisation) if obj.localisation else None,
            }

        vectorized_docs.append(
            VectorizedDocument(
                entity_id=obj.id,
                document_type=doc_type,
                content=fake.sentence(),
                embedding=[0.2] * 1536,  # Mock embedding
                metadata=metadata,
            )
        )
    return vectorized_docs


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

    # Generate vectorized documents using entity UUIDs
    vectorized_concours = generate_vectorized_documents(concours_repo.get_all())
    vectorized_offers = generate_vectorized_documents(offers_repo.get_all())

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
