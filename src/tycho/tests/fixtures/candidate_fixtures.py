"""Shared fixtures for candidate tests."""

import json

import pytest
from pydantic import HttpUrl

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


@pytest.fixture(name="candidate_container")
def candidate_container_fixture(pdf_extractor_configs):
    """Set up candidate container with in-memory repository for unit tests."""
    container = CandidateContainer()

    logger_service = LoggerService()
    container.logger_service.override(logger_service)

    # Use async in-memory repository for unit tests
    async_in_memory_cv_repo = AsyncInMemoryCVMetadataRepository()
    container.async_cv_metadata_repository.override(async_in_memory_cv_repo)

    # Keep sync repository for tests that still need it
    in_memory_cv_repo = InMemoryCVMetadataRepository()
    container.postgres_cv_metadata_repository.override(in_memory_cv_repo)

    # Default to Albert configuration
    pdf_config = PDFExtractorConfig(
        pdf_extractor_type=PDFExtractorType.ALBERT,
        albert_config=pdf_extractor_configs["albert"],
        openai_config=pdf_extractor_configs["openai"],
    )
    container.config.override(pdf_config)

    return container


@pytest.fixture(name="openai_candidate_container")
def openai_candidate_container_fixture(pdf_extractor_configs):
    """Set up candidate container with OpenAI extractor for unit tests."""
    container = CandidateContainer()

    logger_service = LoggerService()
    container.logger_service.override(logger_service)

    # Use async in-memory repository for unit tests
    async_in_memory_cv_repo = AsyncInMemoryCVMetadataRepository()
    container.async_cv_metadata_repository.override(async_in_memory_cv_repo)

    # Keep sync repository for tests that still need it
    in_memory_cv_repo = InMemoryCVMetadataRepository()
    container.postgres_cv_metadata_repository.override(in_memory_cv_repo)

    pdf_config = PDFExtractorConfig(
        pdf_extractor_type=PDFExtractorType.OPENAI,
        albert_config=pdf_extractor_configs["albert"],
        openai_config=pdf_extractor_configs["openai"],
    )
    container.config.override(pdf_config)

    return container


@pytest.fixture(name="integration_container")
def integration_container_fixture(pdf_extractor_configs):
    """Set up integration container with Django persistence."""
    container = CandidateContainer()

    logger_service = LoggerService()
    container.logger_service.override(logger_service)

    # Default to Albert configuration
    pdf_config = PDFExtractorConfig(
        pdf_extractor_type=PDFExtractorType.ALBERT,
        albert_config=pdf_extractor_configs["albert"],
        openai_config=pdf_extractor_configs["openai"],
    )
    container.config.override(pdf_config)

    return container


@pytest.fixture(name="openai_integration_container")
def openai_integration_container_fixture(pdf_extractor_configs):
    """Set up integration container with OpenAI extractor."""
    container = CandidateContainer()

    logger_service = LoggerService()
    container.logger_service.override(logger_service)

    pdf_config = PDFExtractorConfig(
        pdf_extractor_type=PDFExtractorType.OPENAI,
        albert_config=pdf_extractor_configs["albert"],
        openai_config=pdf_extractor_configs["openai"],
    )
    container.config.override(pdf_config)

    return container


@pytest.fixture(name="process_cv_usecase")
def process_cv_usecase_fixture(candidate_container):
    """Process CV usecase with Albert extractor for unit tests."""
    return candidate_container.process_uploaded_cv_usecase()


@pytest.fixture(name="openai_process_cv_usecase")
def openai_process_cv_usecase_fixture(openai_candidate_container):
    """Process CV usecase with OpenAI extractor for unit tests."""
    return openai_candidate_container.process_uploaded_cv_usecase()


@pytest.fixture(name="process_cv_usecase_integration")
def process_cv_usecase_integration_fixture(integration_container):
    """Process CV usecase for integration tests with Albert extractor."""
    return integration_container.process_uploaded_cv_usecase()


@pytest.fixture(name="openai_process_cv_usecase_integration")
def openai_process_cv_usecase_integration_fixture(openai_integration_container):
    """Process CV usecase for integration tests with OpenAI extractor."""
    return openai_integration_container.process_uploaded_cv_usecase()


@pytest.fixture(params=["albert", "openai"])
def extractor_config(request):
    """Parametrized fixture for both Albert and OpenAI extractors."""
    if request.param == "albert":
        return {
            "type": "albert",
            "api_url": "https://albert.api.etalab.gouv.fr/v1/ocr-beta",
            "usecase_fixture": "process_cv_usecase",
            "container_fixture": "candidate_container",
            "response_wrapper": lambda response: response,
            "retry_count": 1,
        }
    else:  # openai
        return {
            "type": "openai",
            "api_url": "https://openrouter.ai/api/v1/chat/completions",
            "usecase_fixture": "openai_process_cv_usecase",
            "container_fixture": "openai_candidate_container",
            "response_wrapper": lambda response: {
                "choices": [{"message": {"content": json.dumps(response)}}]
            },
            "retry_count": 3,
        }


@pytest.fixture(params=["albert", "openai"])
def extractor_config_integration(request):
    """Parametrized fixture for both Albert and OpenAI extractors."""
    if request.param == "albert":
        return {
            "type": "albert",
            "api_url": "https://albert.api.etalab.gouv.fr/v1/ocr-beta",
            "usecase_fixture": "process_cv_usecase_integration",
            "response_wrapper": lambda response: response,
            "retry_count": 1,
        }
    else:  # openai
        return {
            "type": "openai",
            "api_url": "https://openrouter.ai/api/v1/chat/completions",
            "usecase_fixture": "openai_process_cv_usecase_integration",
            "response_wrapper": lambda response: {
                "choices": [{"message": {"content": json.dumps(response)}}]
            },
            "retry_count": 3,
        }


@pytest.fixture(name="pdf_content")
def pdf_content_fixture():
    """Valid PDF content for testing."""
    return create_minimal_valid_pdf()
