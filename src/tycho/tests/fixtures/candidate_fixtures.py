"""Shared fixtures for candidate tests."""

from uuid import UUID

import pytest
from django.utils import timezone
from pydantic import HttpUrl

from domain.entities.cv_metadata import CVMetadata
from domain.value_objects.cv_processing_status import CVStatus
from domain.value_objects.pdf_extractor_type import PDFExtractorType
from infrastructure.di.candidate.candidate_container import CandidateContainer
from infrastructure.external_gateways.configs.albert_config import AlbertConfig
from infrastructure.external_gateways.configs.openai_config import OpenAIConfig
from infrastructure.external_gateways.configs.pdf_extractor_config import (
    PDFExtractorConfig,
)
from infrastructure.gateways.shared.logger import LoggerService
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
    now = timezone.now()
    return CVMetadata(
        id=cv_id,
        filename="test_cv.pdf",
        status=CVStatus.PENDING,
        created_at=now,
        updated_at=now,
    ), cv_id
