import json
import os
from typing import cast
from unittest.mock import AsyncMock, MagicMock, Mock

import pytest
from asgiref.sync import sync_to_async
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import connections
from faker import Faker
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, PayloadSchemaType, VectorParams
from referentiel.repositories.concours_repository_interface import IConcoursRepository
from referentiel.repositories.corps_repository_interface import ICorpsRepository
from referentiel.repositories.metier_repository_interface import IMetierRepository
from referentiel.repositories.offers_repository_interface import IOffersRepository
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from application.candidate.usecases.get_opportunity_details import (
    GetOpportunityDetailsUsecase,
)
from application.candidate.usecases.initialize_cv_metadata import (
    InitializeCVMetadataUsecase,
)
from application.candidate.usecases.match_cv_to_opportunities import (
    MatchCVToOpportunitiesUsecase,
)
from application.candidate.usecases.process_uploaded_cv import ProcessUploadedCVUsecase
from application.candidate.usecases.submit_application import SubmitApplicationUsecase
from application.identite.usecases.create_agent import CreateAgentUsecase
from application.identite.usecases.create_organisme import CreateOrganismeUsecase
from application.ingestion.usecases.archive_offers import ArchiveOffersUsecase
from application.ingestion.usecases.clean_documents import CleanDocumentsUsecase
from application.ingestion.usecases.get_offers_by_source import (
    GetOffersBySourceUseCase,
)
from application.ingestion.usecases.list_offers import ListOffersUseCase
from application.ingestion.usecases.list_sources import ListSourcesUseCase
from application.ingestion.usecases.load_documents import LoadDocumentsUsecase
from application.ingestion.usecases.upsert_offers import UpsertOffersUseCase
from application.ingestion.usecases.vectorize_documents import VectorizeDocumentsUsecase
from application.recruteur.usecases.get_organisme_recruteur import (
    GetOrganismeRecruteurUsecase,
)
from application.recruteur.usecases.initialize_organisme_steps import (
    InitializeOrganismeStepsUsecase,
)
from config.app_config import AppConfig
from domain.candidate.repositories.candidature_repository_interface import (
    ICandidatureRepository,
)
from domain.candidate.repositories.cv_metadata_repository_interface import (
    ICVMetadataRepository,
)
from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.identite.repositories.agent_repository_interface import IAgentRepository
from domain.identite.repositories.organisme_repository_interface import (
    IOrganismeRepository,
)
from domain.identite.repositories.utilisateur_repository_interface import (
    IUtilisateurRepository,
)
from domain.ingestion.entities.document import DocumentType
from domain.ingestion.exceptions.document_error import UnsupportedDocumentTypeError
from domain.ingestion.repositories.document_repository_interface import (
    IDocumentRepository,
)
from domain.ingestion.repositories.source_repository_interface import ISourceRepository
from domain.ingestion.repositories.user_source_repository_interface import (
    IUserSourceRepository,
)
from domain.ingestion.repositories.vector_repository_interface import IVectorRepository
from domain.recruteur.repositories.organisme_repository_interface import (
    IOrganismeRecruteurRepository,
)
from infrastructure.di.ingestion.ingestion_container import IngestionContainer
from infrastructure.di.shared.shared_container import SharedContainer
from infrastructure.gateways.candidate.query_builder import QueryBuilder
from infrastructure.gateways.shared.logger import LoggerService
from infrastructure.repositories.shared.qdrant_repository import QdrantRepository
from tests.factories.identite.utilisateur_factory import UtilisateurFactory
from tests.utils.async_in_memory_cv_metadata_repository import (
    AsyncInMemoryCVMetadataRepository,
)
from tests.utils.interface_aware_mock import create_interface_aware_mock
from tests.utils.mock_api_response_factory import MockApiResponseFactory
from tests.utils.pdf_test_utils import create_minimal_valid_pdf

fake = Faker()

USER_MODEL = get_user_model()


@pytest.fixture(autouse=True)
async def close_worker_thread_connections():
    yield
    # async ORM calls (via sync_to_async) open a DB connection in a worker thread.
    # close_all() runs in that same thread via sync_to_async, closing the connection
    # before the test database is dropped at session teardown.
    await sync_to_async(connections.close_all)()


@pytest.fixture(name="api_client")
def api_client_fixture(db):
    return APIClient()


@pytest.fixture(name="test_user")
def test_user_fixture(db):
    return UtilisateurFactory.create_model()


@pytest.fixture(name="authenticated_client")
def authenticated_client_fixture(api_client, test_user):
    refresh = RefreshToken.for_user(test_user)
    token = str(refresh.access_token)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return api_client


@pytest.fixture(name="api_key_client")
def api_key_client_fixture(api_client):
    api_client.credentials(HTTP_AUTHORIZATION="Api-Key test-ingestion-api-key")
    return api_client


@pytest.fixture(name="ingestion_container")
def ingestion_container_fixture(db):
    shared_container = SharedContainer()
    app_config = AppConfig.from_django_settings()
    logger_service = LoggerService("ingestion")
    shared_container.app_config.override(app_config)
    shared_container.logger_service.override(logger_service)
    container = IngestionContainer()
    container.app_config.override(app_config)
    container.logger_service.override(logger_service)
    container.shared_container.override(shared_container)
    return container


def create_collection(client: QdrantClient, collection_name: str):
    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(
            size=settings.EMBEDDING_DIMENSION, distance=Distance.COSINE
        ),
    )

    indexes = [
        "document_type",
        "category",
        "verse",
        "localisation.region",
        "localisation.country",
        "localisation.department",
    ]

    for field_name in indexes:
        client.create_payload_index(
            collection_name=collection_name,
            field_name=field_name,
            field_schema=PayloadSchemaType.KEYWORD,
        )


def create_shared_qdrant_repository():
    app_config = AppConfig.from_django_settings()
    worker_id = os.environ.get("PYTEST_XDIST_WORKER", "master")
    collection_name = f"fonction_publique_test_{worker_id}"
    client = QdrantClient(url=app_config.qdrant.url)

    try:
        client.delete_collection(collection_name=collection_name)
    except Exception:
        logger_service = LoggerService()
        logger_service.warning(
            f"Collection {collection_name} does not exist, skipping deletion."
        )
        pass

    create_collection(client, collection_name)

    logger_service = LoggerService()
    qdrant_repo = QdrantRepository(app_config.qdrant, logger_service)
    qdrant_repo.collection_name = collection_name
    return qdrant_repo


@pytest.fixture
def match_cv_to_opportunities_usecase():
    logger_service = LoggerService()

    embedding_generator_mock = Mock()
    embedding_generator_mock.generate_embedding = AsyncMock(
        return_value=[0.1, 0.2, 0.3]
    )
    concours_repo = cast(
        IConcoursRepository, create_interface_aware_mock(IConcoursRepository)
    )
    offers_repo = cast(
        IOffersRepository, create_interface_aware_mock(IOffersRepository)
    )
    metiers_repo = cast(
        IMetierRepository, create_interface_aware_mock(IMetierRepository)
    )
    cv_repo = cast(
        ICVMetadataRepository, create_interface_aware_mock(ICVMetadataRepository)
    )
    vector_repo = cast(
        IVectorRepository, create_interface_aware_mock(IVectorRepository)
    )

    return MatchCVToOpportunitiesUsecase(
        cv_metadata_repository=cv_repo,
        embedding_generator=embedding_generator_mock,
        vector_repository=vector_repo,
        concours_repository=concours_repo,
        offers_repository=offers_repo,
        metiers_repository=metiers_repo,
        logger=logger_service,
    )


@pytest.fixture
def process_uploaded_cv_usecase():
    logger_service = LoggerService()
    async_cv_repo = AsyncInMemoryCVMetadataRepository()
    query_builder = QueryBuilder()

    # Utiliser les factories pour créer les mocks
    ocr_mock = create_ocr_mock()
    text_formatter_mock = create_text_formatter_mock()

    return ProcessUploadedCVUsecase(
        ocr=ocr_mock,
        text_formatter=text_formatter_mock,
        query_builder=query_builder,
        async_cv_metadata_repository=async_cv_repo,
        logger=logger_service,
    )


@pytest.fixture
def pdf_content():
    return create_minimal_valid_pdf()


def create_ocr_mock():
    ocr_mock = Mock()
    ocr_response = MockApiResponseFactory.create_ocr_service_response()
    ocr_mock.extract_text = AsyncMock(return_value=ocr_response["text"])
    return ocr_mock


def create_text_formatter_mock():
    embedding_response = MockApiResponseFactory.create_formatter_response()
    content = embedding_response["choices"][0]["message"]["content"]
    cv_data = json.loads(content)

    formatted_data_mock = Mock()
    formatted_data_mock.experiences = cv_data["experiences"]
    formatted_data_mock.skills = cv_data["skills"]
    formatted_data_mock.model_dump.return_value = cv_data

    text_formatter_mock = Mock()
    text_formatter_mock.format_text = AsyncMock(return_value=formatted_data_mock)

    return text_formatter_mock


@pytest.fixture
def initialize_cv_metadata_usecase():
    cv_metadata_repository = cast(
        ICVMetadataRepository, create_interface_aware_mock(ICVMetadataRepository)
    )
    return InitializeCVMetadataUsecase(cv_metadata_repository)


@pytest.fixture
def load_documents_usecase():
    logger_service = LoggerService()
    document_repo = create_interface_aware_mock(IDocumentRepository)

    mock_strategy = Mock()
    mock_strategy.load_documents = AsyncMock()

    strategy_factory = Mock()
    strategy_factory.create.return_value = mock_strategy

    return LoadDocumentsUsecase(
        strategy_factory=strategy_factory,
        document_repository=cast(IDocumentRepository, document_repo),
        logger=logger_service,
    )


def mock_cleaning_result(entities, cleaning_errors):
    mock_result = Mock()
    mock_result.entities = entities
    mock_result.cleaning_errors = cleaning_errors
    return mock_result


@pytest.fixture
def clean_documents_usecase():
    logger_service = LoggerService()
    document_repo = cast(
        IDocumentRepository, create_interface_aware_mock(IDocumentRepository)
    )

    document_cleaner = Mock()
    document_cleaner.clean.return_value = mock_cleaning_result([], [])

    repository_factory = Mock()

    corps_repo = create_interface_aware_mock(ICorpsRepository)
    concours_repo = create_interface_aware_mock(IConcoursRepository)
    metier_repo = create_interface_aware_mock(IMetierRepository)
    offers_repo = create_interface_aware_mock(IOffersRepository)

    def get_repository(document_type):
        if document_type == DocumentType.CORPS:
            return corps_repo
        elif document_type == DocumentType.CONCOURS:
            return concours_repo
        elif document_type == DocumentType.METIERS:
            return metier_repo
        elif document_type == DocumentType.OFFERS:
            return offers_repo
        else:
            raise UnsupportedDocumentTypeError(
                f"Unsupported document type: {document_type}"
            )

    repository_factory.get_repository.side_effect = get_repository

    return CleanDocumentsUsecase(
        document_repository=document_repo,
        document_cleaner=document_cleaner,
        repository_factory=repository_factory,
        logger=logger_service,
    )


@pytest.fixture
def vectorize_documents_usecase():
    logger_service = LoggerService()
    vector_repo = cast(
        IVectorRepository, create_interface_aware_mock(IVectorRepository)
    )

    text_extractor = Mock()
    text_extractor.extract_content.return_value = "Extracted text content"
    text_extractor.extract_metadata.return_value = {"key": "value"}

    embedding_generator = Mock()
    embedding_generator.generate_embedding = AsyncMock(return_value=[0.1, 0.2, 0.3])

    repository_factory = Mock()
    mock_source_repo = Mock()
    mock_source_repo.get_pending_processing.return_value = []
    mock_source_repo.mark_as_processed.return_value = None
    mock_source_repo.mark_as_pending.return_value = None
    repository_factory.get_repository.return_value = mock_source_repo

    return VectorizeDocumentsUsecase(
        vector_repository=vector_repo,
        text_extractor=text_extractor,
        embedding_generator=embedding_generator,
        logger=logger_service,
        repository_factory=repository_factory,
    )


@pytest.fixture
def archive_offers_usecase():
    logger = MagicMock()
    vector_repo = cast(
        IVectorRepository, create_interface_aware_mock(IVectorRepository)
    )
    offers_repo = cast(
        IOffersRepository, create_interface_aware_mock(IOffersRepository)
    )

    return ArchiveOffersUsecase(
        offers_repository=offers_repo,
        document_gateway=MagicMock(),
        vector_repository=vector_repo,
        logger=logger,
    )


@pytest.fixture
def list_offers_usecase():
    logger = MagicMock()
    offers_repo = cast(
        IOffersRepository, create_interface_aware_mock(IOffersRepository)
    )

    return ListOffersUseCase(
        offers_repository=offers_repo,
        logger=logger,
    )


@pytest.fixture
def upsert_offers_usecase():
    logger = MagicMock()
    offers_repo = cast(
        IOffersRepository, create_interface_aware_mock(IOffersRepository)
    )
    user_source_repo = cast(
        IUserSourceRepository, create_interface_aware_mock(IUserSourceRepository)
    )
    utilisateur_repo = cast(
        IUtilisateurRepository, create_interface_aware_mock(IUtilisateurRepository)
    )

    return UpsertOffersUseCase(
        offers_repository=offers_repo,
        logger=logger,
        user_source_repository=user_source_repo,
        utilisateur_repository=utilisateur_repo,
    )


@pytest.fixture
def get_offers_by_source_usecase():
    offers_repo = cast(
        IOffersRepository, create_interface_aware_mock(IOffersRepository)
    )
    user_source_repo = cast(
        IUserSourceRepository, create_interface_aware_mock(IUserSourceRepository)
    )
    utilisateur_repo = cast(
        IUtilisateurRepository, create_interface_aware_mock(IUtilisateurRepository)
    )

    return GetOffersBySourceUseCase(
        offers_repository=offers_repo,
        user_source_repository=user_source_repo,
        utilisateur_repository=utilisateur_repo,
    )


@pytest.fixture
def list_sources_usecase():
    source_repo = cast(
        ISourceRepository, create_interface_aware_mock(ISourceRepository)
    )

    return ListSourcesUseCase(
        source_repository=source_repo,
    )


@pytest.fixture
def get_opportunity_details_usecase():
    logger = MagicMock()
    offers_repository = cast(
        IOffersRepository, create_interface_aware_mock(IOffersRepository)
    )
    concours_repository = cast(
        IConcoursRepository, create_interface_aware_mock(IConcoursRepository)
    )
    metiers_repository = cast(
        IMetierRepository, create_interface_aware_mock(IMetierRepository)
    )
    return GetOpportunityDetailsUsecase(
        logger=logger,
        offers_repository=offers_repository,
        concours_repository=concours_repository,
        metiers_repository=metiers_repository,
    )


@pytest.fixture
def submit_application_usecase():
    candidature_repository = MagicMock(spec=ICandidatureRepository)
    actors_validator = MagicMock()
    return SubmitApplicationUsecase(
        candidature_repository=candidature_repository,
        actors_validator=actors_validator,
        audit_log_writer=MagicMock(spec=AuditLogWriter),
        logger=MagicMock(),
    )


@pytest.fixture
def create_agent_usecase():
    agent_repository = cast(
        IAgentRepository, create_interface_aware_mock(IAgentRepository)
    )
    utilisateur_repository = cast(
        IUtilisateurRepository, create_interface_aware_mock(IUtilisateurRepository)
    )
    return CreateAgentUsecase(
        agent_repository=agent_repository,
        utilisateur_repository=utilisateur_repository,
    )


@pytest.fixture
def create_organisme_usecase():
    organisme_repository = cast(
        IOrganismeRepository, create_interface_aware_mock(IOrganismeRepository)
    )
    return CreateOrganismeUsecase(organisme_repository=organisme_repository)


@pytest.fixture
def get_organisme_recruteur_usecase():
    organisme_repository = cast(
        IOrganismeRecruteurRepository, create_interface_aware_mock(IOrganismeRepository)
    )
    return GetOrganismeRecruteurUsecase(organisme_repository=organisme_repository)


@pytest.fixture
def initialize_organisme_steps_usecase():
    repository = cast(
        IOrganismeRecruteurRepository,
        create_interface_aware_mock(IOrganismeRecruteurRepository),
    )
    return InitializeOrganismeStepsUsecase(organisme_repository=repository)
