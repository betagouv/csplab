import pytest
import responses
from django.conf import settings
from faker import Faker
from pytest_django.asserts import assertNumQueries

from config.app_config import AppConfig
from domain.entities.document import DocumentType
from infrastructure.di.candidate.candidate_container import CandidateContainer
from infrastructure.di.shared.shared_container import SharedContainer
from infrastructure.django_apps.shared.models.concours import ConcoursModel
from infrastructure.django_apps.shared.models.offer import OfferModel
from infrastructure.external_gateways.albert_embedding_generator import (
    AlbertEmbeddingGenerator,
)
from infrastructure.gateways.shared.http_client import SyncHttpClient
from infrastructure.gateways.shared.logger import LoggerService
from tests.factories.concours_factory import ConcoursFactory
from tests.factories.offer_factory import OfferFactory
from tests.factories.vectorized_document_factory import VectorizedDocumentFactory

# Import fixtures needed for this test
from tests.fixtures.candidate_fixtures import create_cv_metadata_completed
from tests.fixtures.shared_fixtures import (
    create_shared_qdrant_repository,
)
from tests.utils.mock_api_response_factory import MockApiResponseFactory

fake = Faker()


@pytest.fixture
def _integration_candidate_container():
    shared_qdrant_repository = create_shared_qdrant_repository()

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
    http_client = SyncHttpClient()
    embedding_generator = AlbertEmbeddingGenerator(
        config=app_config.albert, http_client=http_client
    )
    shared_container.embedding_generator.override(embedding_generator)

    # Use shared Qdrant repository fixture
    shared_container.vector_repository.override(shared_qdrant_repository)

    container.shared_container.override(shared_container)

    # Setup app config and logger for candidate container too
    container.app_config.override(app_config)
    container.logger_service.override(logger_service)

    return container


@responses.activate
@pytest.mark.django_db
def test_execute_with_valid_cv_returns_opportunities(
    _integration_candidate_container,
):
    # Mock Albert API
    app_config = _integration_candidate_container.app_config()
    albert_url = f"{app_config.albert.api_base_url}v1/embeddings"
    mock_response = MockApiResponseFactory.create_albert_embedding_response()
    responses.add(
        responses.POST,
        albert_url,
        json=mock_response,
        status=200,
        content_type="application/json",
    )

    cv_metadata, cv_id = create_cv_metadata_completed()
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
    concours_repo.upsert_batch([ConcoursModel.to_entity(c) for c in concours])

    offers_repo = _integration_candidate_container.shared_container.offers_repository()
    offers_repo.upsert_batch([OfferModel.to_entity(offer) for offer in offers])

    # Generate vectorized documents using VectorizedDocumentFactory
    vectorized_concours = []
    for concours_entity in concours_repo.get_all():
        vectorized_doc = VectorizedDocumentFactory.create(
            entity_id=concours_entity.id,
            document_type=DocumentType.CONCOURS,
            content=fake.sentence(),
            embedding_dimensions=settings.EMBEDDING_DIMENSION,
        )
        vectorized_concours.append(vectorized_doc)

    vectorized_offers = []
    for offer_entity in offers_repo.get_all():
        vectorized_doc = VectorizedDocumentFactory.create(
            entity_id=offer_entity.id,
            document_type=DocumentType.OFFERS,
            content=fake.sentence(),
            embedding_dimensions=settings.EMBEDDING_DIMENSION,
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

    similarities = [score for _, score in results]
    assert sorted(similarities, reverse=True) == similarities

    assert all(0.0 <= score <= 1 for score in similarities)
    assert all(isinstance(score, float) for score in similarities)
