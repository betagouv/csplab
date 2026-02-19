"""Shared fixtures for candidate tests."""

from datetime import datetime, timezone
from uuid import UUID

import pytest
from pydantic import HttpUrl

from domain.entities.concours import Concours
from domain.entities.cv_metadata import CVMetadata
from domain.entities.document import DocumentType
from domain.entities.vectorized_document import VectorizedDocument
from domain.value_objects.access_modality import AccessModality
from domain.value_objects.category import Category
from domain.value_objects.cv_processing_status import CVStatus
from domain.value_objects.ministry import Ministry
from domain.value_objects.nor import NOR
from domain.value_objects.pdf_extractor_type import PDFExtractorType
from infrastructure.di.candidate.candidate_container import CandidateContainer
from infrastructure.django_apps.candidate.models.cv_metadata import CVMetadataModel
from infrastructure.external_gateways.configs.albert_config import AlbertConfig
from infrastructure.external_gateways.configs.openai_config import OpenAIConfig
from infrastructure.external_gateways.configs.pdf_extractor_config import (
    PDFExtractorConfig,
)
from infrastructure.gateways.shared.logger import LoggerService
from tests.factories.cv_metadata_factory import CVMetadataFactory
from tests.fixtures.vectorize_test_factories import (
    create_test_offer,
)
from tests.utils.async_in_memory_cv_metadata_repository import (
    AsyncInMemoryCVMetadataRepository,
)
from tests.utils.in_memory_cv_metadata_repository import InMemoryCVMetadataRepository
from tests.utils.pdf_test_utils import create_minimal_valid_pdf


@pytest.fixture(name="pdf_extractor_configs", scope="session")
def pdf_extractor_configs_fixture():
    """PDF extractor configurations."""
    albert_config = AlbertConfig(
        api_base_url=HttpUrl("https://albert.api.etalab.gouv.fr"),
        api_key="test-albert-key",
        model_name="albert-large",
        dpi=200,
    )
    openai_config = OpenAIConfig(
        api_key="test-api-key",
        model="gpt-4o",
        base_url=HttpUrl("https://openrouter.ai/api/v1"),
    )
    return {
        "albert": albert_config,
        "openai": openai_config,
    }


def _create_candidate_container(
    pdf_extractor_configs, pdf_extractor_type: PDFExtractorType, in_memory: bool
):
    """Factory function to create candidate containers with specified configuration."""
    container = CandidateContainer()

    logger_service = LoggerService()
    container.logger_service.override(logger_service)

    if in_memory:
        # Use in-memory repositories for unit tests
        async_in_memory_cv_repo = AsyncInMemoryCVMetadataRepository()
        container.async_cv_metadata_repository.override(async_in_memory_cv_repo)

        # Keep sync repository for tests that still need it
        in_memory_cv_repo = InMemoryCVMetadataRepository()
        container.postgres_cv_metadata_repository.override(in_memory_cv_repo)

    # Configure PDF extractor
    pdf_config = PDFExtractorConfig(
        pdf_extractor_type=pdf_extractor_type,
        albert_config=pdf_extractor_configs["albert"],
        openai_config=pdf_extractor_configs["openai"],
    )
    container.config.override(pdf_config)

    return container


@pytest.fixture(name="albert_candidate_container")
def albert_candidate_container_fixture(pdf_extractor_configs):
    """Set up candidate container with Albert extractor and in-memory repository."""
    return _create_candidate_container(
        pdf_extractor_configs, PDFExtractorType.ALBERT, in_memory=True
    )


@pytest.fixture(name="openai_candidate_container")
def openai_candidate_container_fixture(pdf_extractor_configs):
    """Set up candidate container with OpenAI extractor and in-memory repository."""
    return _create_candidate_container(
        pdf_extractor_configs, PDFExtractorType.OPENAI, in_memory=True
    )


@pytest.fixture(name="albert_integration_container")
def albert_integration_container_fixture(pdf_extractor_configs):
    """Set up integration container with Albert extractor and Django persistence."""
    return _create_candidate_container(
        pdf_extractor_configs, PDFExtractorType.ALBERT, in_memory=False
    )


@pytest.fixture(name="openai_integration_container")
def openai_integration_container_fixture(pdf_extractor_configs):
    """Set up integration container with OpenAI extractor and Django persistence."""
    return _create_candidate_container(
        pdf_extractor_configs, PDFExtractorType.OPENAI, in_memory=False
    )


@pytest.fixture(name="pdf_content")
def pdf_content_fixture():
    """Valid PDF content for testing."""
    return create_minimal_valid_pdf()


@pytest.fixture(name="cv_metadata_initial")
def cv_metadata_initial_fixture():
    """Initial CV metadata for testing."""
    cv_id = UUID("00000000-0000-0000-0000-000000000001")
    now = datetime.now(timezone.utc)
    return CVMetadata(
        id=cv_id,
        filename="test_cv.pdf",
        status=CVStatus.PENDING,
        created_at=now,
        updated_at=now,
    ), cv_id


@pytest.fixture(name="cv_metadata_completed")
def cv_metadata_completed_fixture(cv_metadata_initial):
    """CV metadata with COMPLETED status and search query."""
    cv_metadata, cv_id = cv_metadata_initial
    cv_metadata.status = CVStatus.COMPLETED
    cv_metadata.search_query = "Python developer with Django experience"
    cv_metadata.extracted_text = {
        "experiences": ["Software Engineer"],
        "skills": ["Python", "Django"],
    }
    return cv_metadata, cv_id


@pytest.fixture(name="cv_metadata_failed")
def cv_metadata_failed_fixture(cv_metadata_initial):
    """CV metadata with FAILED status."""
    cv_metadata, cv_id = cv_metadata_initial
    cv_metadata.status = CVStatus.FAILED
    return cv_metadata, cv_id


@pytest.fixture(name="concours")
def concours_fixture():
    """Create test concours data."""
    return [
        Concours(
            nor_original=NOR("MENA2400001A"),
            nor_list=[NOR("MENA2400001A")],
            category=Category.A,
            ministry=Ministry.MAA,
            access_modality=[AccessModality.CONCOURS_EXTERNE],
            corps="Ingénieur des systèmes d'information",
            grade="Ingénieur principal",
            written_exam_date=datetime.now(timezone.utc),
            open_position_number=10,
        ),
        Concours(
            nor_original=NOR("AGRI2400002B"),
            nor_list=[NOR("AGRI2400002B")],
            category=Category.A,
            ministry=Ministry.MAA,
            access_modality=[AccessModality.CONCOURS_EXTERNE],
            corps="Attaché d'administration",
            grade="Attaché principal",
            written_exam_date=datetime.now(timezone.utc),
            open_position_number=5,
        ),
    ]


@pytest.fixture(name="vectorized_concours_documents")
def vectorized_concours_documents_fixture(concours):
    """Create test vectorized documents for concours."""
    documents = []
    for c in concours:
        vectorized_doc = VectorizedDocument(
            id=c.id,
            entity_id=c.id,
            document_type=DocumentType.CONCOURS,
            content=f"{c.corps} {c.grade}",
            embedding=[0.1] * 3072,  # Mock embedding
            metadata={"source": "test"},
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        documents.append(vectorized_doc)
    return documents


@pytest.fixture(name="offers")
def offers_fixture():
    """Create test offers datas."""
    return [create_test_offer(i) for i in range(4, 7)]


@pytest.fixture(name="vectorized_offers_documents")
def vectorized_offers_documents_fixture(offers):
    """Create test vectorized documents for offers."""
    return [
        VectorizedDocument(
            id=c.id,
            entity_id=c.id,
            document_type=DocumentType.OFFERS,
            content=f"{c.external_id} {c.title}",
            embedding=[0.2] * 3072,  # Mock embedding
            metadata={"source": "test"},
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        for c in offers
    ]


@pytest.fixture(name="db_cv_uuid")
def db_cv_uuid_fixture(status: CVStatus = CVStatus.COMPLETED) -> UUID:
    """Create a CV with given status in database and return its UUID."""
    cv_metadata = CVMetadataFactory.build(status=status)
    CVMetadataModel.from_entity(cv_metadata).save()
    return cv_metadata.id
