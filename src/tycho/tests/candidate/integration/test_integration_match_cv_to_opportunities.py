import pytest
import responses
from django.conf import settings
from faker import Faker
from pytest_django.asserts import assertNumQueries

from config.app_config import AppConfig
from domain.entities.document import DocumentType
from domain.value_objects.category import Category
from domain.value_objects.verse import Verse
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

TWO_DOCUMENTS = 2
THREE_DOCUMENTS = 3
SIX_DOCUMENTS = 6


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
        metadata = {
            "category": concours_entity.category.value,
            "ministry": concours_entity.ministry.value,
            "access_modality": [],
        }
        vectorized_doc = VectorizedDocumentFactory.create(
            entity_id=concours_entity.id,
            document_type=DocumentType.CONCOURS,
            content=fake.sentence(),
            embedding_dimensions=settings.EMBEDDING_DIMENSION,
            metadata=metadata,
        )
        vectorized_concours.append(vectorized_doc)

    vectorized_offers = []
    offer_entities = list(offers_repo.get_all())
    for offer_entity in offer_entities:
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


@responses.activate
@pytest.mark.django_db
def test_vectorize_qdrant_search_empty_filters(_integration_candidate_container):
    # Mock Albert API
    test_app_config = _integration_candidate_container.app_config()
    albert_url = f"{test_app_config.albert.api_base_url}v1/embeddings"
    mock_response = MockApiResponseFactory.create_albert_embedding_response()
    responses.add(
        responses.POST,
        albert_url,
        json=mock_response,
        status=200,
        content_type="application/json",
    )

    cv_metadata, cv_id = create_cv_metadata_completed()
    # Create test data like in the working test
    offers = OfferFactory.create_batch(3)

    # Setup CV metadata in real DB
    cv_repo = _integration_candidate_container.postgres_cv_metadata_repository()
    cv_repo.save(cv_metadata)

    offers_repo = _integration_candidate_container.shared_container.offers_repository()
    offers_repo.upsert_batch([OfferModel.to_entity(offer) for offer in offers])

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
    vector_repo.upsert_batch(vectorized_offers, DocumentType.OFFERS)

    usecase = _integration_candidate_container.match_cv_to_opportunities_usecase()
    with assertNumQueries(
        1  # select OfferModel
    ):
        results = usecase.execute(cv_metadata)

    assert isinstance(results, list)
    assert len(results) == THREE_DOCUMENTS

    similarities = [r[1] for r in results]
    assert sorted(similarities, reverse=True) == similarities


@responses.activate
@pytest.mark.django_db
def test_vectorize_qdrant_search_list_filters(_integration_candidate_container):
    # Mock Albert API

    INDEX_REGION = 2
    test_app_config = _integration_candidate_container.app_config()
    albert_url = f"{test_app_config.albert.api_base_url}v1/embeddings"
    mock_response = MockApiResponseFactory.create_albert_embedding_response()
    responses.add(
        responses.POST,
        albert_url,
        json=mock_response,
        status=200,
        content_type="application/json",
    )

    cv_metadata, cv_id = create_cv_metadata_completed()
    offers = [
        OfferFactory.create(verse=Verse.FPE),
        OfferFactory.create(verse=Verse.FPH),
        OfferFactory.create(verse=Verse.FPT),
    ]

    concours = [
        ConcoursFactory.create(category=Category.A),
        ConcoursFactory.create(category=Category.B),
        ConcoursFactory.create(category=Category.C),
    ]

    cv_repo = _integration_candidate_container.postgres_cv_metadata_repository()
    cv_repo.save(cv_metadata)

    offers_repo = _integration_candidate_container.shared_container.offers_repository()
    offers_repo.upsert_batch([OfferModel.to_entity(offer) for offer in offers])

    concours_repo = (
        _integration_candidate_container.shared_container.concours_repository()
    )
    concours_repo.upsert_batch([ConcoursModel.to_entity(c) for c in concours])

    vectorized_offers = []
    offer_entities = list(offers_repo.get_all())
    for i, offer_entity in enumerate(offer_entities):
        if i < INDEX_REGION:
            localisation = {
                "country": "FRA",
                "region": "11",
                "department": "75",
            }
        else:
            localisation = {
                "country": "FRA",
                "region": "75",
                "department": "40",
            }

        metadata = {
            "verse": offer_entity.verse.value,
            "category": None,
            "localisation": localisation,
        }
        vectorized_doc = VectorizedDocumentFactory.create(
            entity_id=offer_entity.id,
            document_type=DocumentType.OFFERS,
            content=fake.sentence(),
            embedding_dimensions=settings.EMBEDDING_DIMENSION,
            metadata=metadata,
        )
        vectorized_offers.append(vectorized_doc)

    vector_repo = _integration_candidate_container.shared_container.vector_repository()

    vector_repo.upsert_batch(vectorized_offers, DocumentType.OFFERS)

    vectorized_concours = []
    for concours_entity in concours_repo.get_all():
        metadata = {
            "category": concours_entity.category.value,
            "ministry": concours_entity.ministry.value,
            "access_modality": [],
        }
        vectorized_doc = VectorizedDocumentFactory.create(
            entity_id=concours_entity.id,
            document_type=DocumentType.CONCOURS,
            content=fake.sentence(),
            embedding_dimensions=settings.EMBEDDING_DIMENSION,
            metadata=metadata,
        )
        vectorized_concours.append(vectorized_doc)

    vector_repo.upsert_batch(vectorized_concours, DocumentType.CONCOURS)

    usecase = _integration_candidate_container.match_cv_to_opportunities_usecase()
    all_offers = usecase.execute(
        cv_metadata,
        filters={
            "document_type": DocumentType.OFFERS.value,
        },
    )

    assert len(all_offers) == THREE_DOCUMENTS

    all_offers_and_concours = usecase.execute(
        cv_metadata,
        filters={
            "document_type": [DocumentType.OFFERS.value, DocumentType.CONCOURS.value],
        },
        limit=10,
    )

    assert len(all_offers_and_concours) == SIX_DOCUMENTS

    offers_and_concours_fpe = usecase.execute(
        cv_metadata,
        filters={
            "document_type": [DocumentType.OFFERS.value, DocumentType.CONCOURS.value],
            "verse": Verse.FPE.value,
        },
        limit=10,
    )

    assert len(offers_and_concours_fpe) == 1

    concours_a_b = usecase.execute(
        cv_metadata,
        filters={
            "document_type": DocumentType.CONCOURS.value,
            "category": [Category.A.value, Category.B.value],
        },
        limit=10,
    )

    assert len(concours_a_b) == TWO_DOCUMENTS

    offers_ile_de_france = usecase.execute(
        cv_metadata,
        filters={
            "document_type": DocumentType.OFFERS.value,
            "region": "11",
        },
        limit=10,
    )

    assert len(offers_ile_de_france) == TWO_DOCUMENTS

    offers_landes = usecase.execute(
        cv_metadata,
        filters={
            "document_type": DocumentType.OFFERS.value,
            "region": "75",
        },
        limit=10,
    )

    assert len(offers_landes) == 1
