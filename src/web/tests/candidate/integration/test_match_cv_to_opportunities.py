import pytest
from django.conf import settings
from faker import Faker
from pytest_django.asserts import assertNumQueries

from config.app_config import AppConfig
from domain.entities.document import DocumentType
from domain.value_objects.category import Category
from domain.value_objects.cv_processing_status import CVStatus
from domain.value_objects.verse import Verse
from infrastructure.di.candidate.candidate_container import CandidateContainer
from infrastructure.di.shared.shared_container import SharedContainer
from infrastructure.django_apps.shared.models.concours import ConcoursModel
from infrastructure.django_apps.shared.models.metier import MetierModel
from infrastructure.django_apps.shared.models.offer import OfferModel
from infrastructure.gateways.shared.logger import LoggerService
from tests.factories.concours_factory import ConcoursFactory
from tests.factories.cv_metadata_factory import CVMetadataFactory
from tests.factories.metier_factory import MetierFactory
from tests.factories.offer_factory import OfferFactory
from tests.factories.vectorized_document_factory import VectorizedDocumentFactory
from tests.utils.mock_api_response_factory import MockApiResponseFactory
from tests.utils.shared_fixtures import (
    create_shared_qdrant_repository,
)

fake = Faker()

TWO_DOCUMENTS = 2
THREE_DOCUMENTS = 3
SIX_DOCUMENTS = 6
INDEX_REGION = 2


def mock_embedding_response(
    httpx_mock,
    config,
    status_code: int = 200,
):
    albert_url = f"{config.albert.api_base_url}v1/embeddings"
    mock_response = MockApiResponseFactory.create_embedding_response()
    httpx_mock.add_response(
        method="POST",
        url=albert_url,
        json=mock_response,
        status_code=status_code,
        is_reusable=True,
    )


@pytest.fixture
def candidate_container():
    shared_qdrant_repository = create_shared_qdrant_repository()

    container = CandidateContainer()

    shared_container = SharedContainer()

    app_config = AppConfig.from_django_settings()
    shared_container.app_config.override(app_config)

    logger_service = LoggerService()
    shared_container.logger_service.override(logger_service)

    shared_container.vector_repository.override(shared_qdrant_repository)

    container.shared_container.override(shared_container)

    container.app_config.override(app_config)
    container.logger_service.override(logger_service)

    return container


@pytest.fixture
def test_app_config(candidate_container):
    return candidate_container.app_config()


@pytest.fixture
def cv_metadata():
    return CVMetadataFactory.create_entity(
        status=CVStatus.COMPLETED,
        search_query="Python developer with Django experience",
        extracted_text={
            "experiences": ["Software Engineer"],
            "skills": ["Python", "Django"],
        },
    )


@pytest.mark.httpx_mock(should_mock=lambda request: "albert" in str(request.url))
def test_execute_with_valid_cv_returns_opportunities(
    db, candidate_container, test_app_config, httpx_mock, cv_metadata
):
    # Mock Albert API
    mock_embedding_response(httpx_mock, test_app_config)

    concours = ConcoursFactory.create_model_batch(2)
    offers = OfferFactory.create_model_batch(3)
    metiers = MetierFactory.create_model_batch(3)

    limit = len(offers) + len(concours) - 1

    # Setup CV metadata in real DB
    cv_repo = candidate_container.postgres_cv_metadata_repository()
    cv_repo.save(cv_metadata)

    # Populate concours data in real DB
    concours_repo = candidate_container.shared_container.concours_repository()
    concours_repo.upsert_batch([ConcoursModel.to_entity(c) for c in concours])

    offers_repo = candidate_container.shared_container.offers_repository()
    offers_repo.upsert_batch([OfferModel.to_entity(offer) for offer in offers])

    metiers_repo = candidate_container.shared_container.metiers_repository()
    metiers_repo.upsert_batch([MetierModel.to_entity(metier) for metier in metiers])

    # Generate vectorized documents using VectorizedDocumentFactory
    vectorized_concours = []
    for concours_entity in concours_repo.get_all():
        metadata = {
            "category": concours_entity.category.value,
            "ministry": concours_entity.ministry.value,
            "access_modality": [],
        }
        vectorized_doc = VectorizedDocumentFactory.create_entity(
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
        vectorized_doc = VectorizedDocumentFactory.create_entity(
            entity_id=offer_entity.id,
            document_type=DocumentType.OFFERS,
            content=fake.sentence(),
            embedding_dimensions=settings.EMBEDDING_DIMENSION,
        )
        vectorized_offers.append(vectorized_doc)

    # Populate vector data in real DB
    vector_repo = candidate_container.shared_container.vector_repository()
    vector_repo.upsert_batch(vectorized_concours, DocumentType.CONCOURS)
    vector_repo.upsert_batch(vectorized_offers, DocumentType.OFFERS)

    usecase = candidate_container.match_cv_to_opportunities_usecase()
    with assertNumQueries(
        1  # select ConcoursModel
        + 1  # select OfferModel
    ):
        results = usecase.execute(cv_metadata, limit=limit)

    assert isinstance(results, list)
    assert len(results) == limit

    similarities = [score for _, score in results]
    assert sorted(similarities, reverse=True) == similarities


@pytest.mark.httpx_mock(should_mock=lambda request: "albert" in str(request.url))
def test_vectorize_qdrant_search_empty_filters(
    db, candidate_container, test_app_config, httpx_mock, cv_metadata
):
    # Mock Albert API
    mock_embedding_response(httpx_mock, test_app_config)

    # Create test data like in the working test
    offers = OfferFactory.create_model_batch(3)

    # Setup CV metadata in real DB
    cv_repo = candidate_container.postgres_cv_metadata_repository()
    cv_repo.save(cv_metadata)

    offers_repo = candidate_container.shared_container.offers_repository()
    offers_repo.upsert_batch([OfferModel.to_entity(offer) for offer in offers])

    vectorized_offers = []
    for offer_entity in offers_repo.get_all():
        vectorized_doc = VectorizedDocumentFactory.create_entity(
            entity_id=offer_entity.id,
            document_type=DocumentType.OFFERS,
            content=fake.sentence(),
            embedding_dimensions=settings.EMBEDDING_DIMENSION,
        )
        vectorized_offers.append(vectorized_doc)

    # Populate vector data in real DB
    vector_repo = candidate_container.shared_container.vector_repository()
    vector_repo.upsert_batch(vectorized_offers, DocumentType.OFFERS)

    usecase = candidate_container.match_cv_to_opportunities_usecase()
    with assertNumQueries(
        1  # select OfferModel
    ):
        results = usecase.execute(cv_metadata)

    assert isinstance(results, list)
    assert len(results) == THREE_DOCUMENTS

    similarities = [r[1] for r in results]
    assert sorted(similarities, reverse=True) == similarities


@pytest.mark.httpx_mock(should_mock=lambda request: "albert" in str(request.url))
def test_vectorize_qdrant_search_list_filters(
    db, candidate_container, test_app_config, httpx_mock, cv_metadata
):
    mock_embedding_response(httpx_mock, test_app_config)

    offers = [
        OfferFactory.create_model(verse=Verse.FPE),
        OfferFactory.create_model(verse=Verse.FPH),
        OfferFactory.create_model(verse=Verse.FPT),
    ]

    concours = [
        ConcoursFactory.create_model(category=Category.A),
        ConcoursFactory.create_model(category=Category.B),
        ConcoursFactory.create_model(category=Category.C),
    ]

    cv_repo = candidate_container.postgres_cv_metadata_repository()
    cv_repo.save(cv_metadata)

    offers_repo = candidate_container.shared_container.offers_repository()
    offers_repo.upsert_batch([OfferModel.to_entity(offer) for offer in offers])

    concours_repo = candidate_container.shared_container.concours_repository()
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
        vectorized_doc = VectorizedDocumentFactory.create_entity(
            entity_id=offer_entity.id,
            document_type=DocumentType.OFFERS,
            content=fake.sentence(),
            embedding_dimensions=settings.EMBEDDING_DIMENSION,
            metadata=metadata,
        )
        vectorized_offers.append(vectorized_doc)

    vector_repo = candidate_container.shared_container.vector_repository()

    vector_repo.upsert_batch(vectorized_offers, DocumentType.OFFERS)

    vectorized_concours = []
    for concours_entity in concours_repo.get_all():
        metadata = {
            "category": concours_entity.category.value,
            "ministry": concours_entity.ministry.value,
            "access_modality": [],
        }
        vectorized_doc = VectorizedDocumentFactory.create_entity(
            entity_id=concours_entity.id,
            document_type=DocumentType.CONCOURS,
            content=fake.sentence(),
            embedding_dimensions=settings.EMBEDDING_DIMENSION,
            metadata=metadata,
        )
        vectorized_concours.append(vectorized_doc)

    vector_repo.upsert_batch(vectorized_concours, DocumentType.CONCOURS)

    usecase = candidate_container.match_cv_to_opportunities_usecase()
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
            "document_type": [
                DocumentType.OFFERS.value,
                DocumentType.CONCOURS.value,
            ],
        },
        limit=10,
    )

    assert len(all_offers_and_concours) == SIX_DOCUMENTS

    offers_and_concours_fpe = usecase.execute(
        cv_metadata,
        filters={
            "document_type": [
                DocumentType.OFFERS.value,
                DocumentType.CONCOURS.value,
            ],
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
