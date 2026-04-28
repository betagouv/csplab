import json
from unittest.mock import AsyncMock, Mock
from uuid import UUID

import pytest

from application.candidate.usecases.process_uploaded_cv import (
    ProcessUploadedCVUsecase,
)
from domain.entities.cv_metadata import CVMetadata
from domain.exceptions.cv_errors import CVNotFoundError
from domain.value_objects.cv_processing_status import CVStatus
from infrastructure.gateways.candidate.query_builder import QueryBuilder
from infrastructure.gateways.shared.logger import LoggerService
from tests.factories.cv_metadata_factory import (
    create_cv_metadata_initial,
)
from tests.utils.async_in_memory_cv_metadata_repository import (
    AsyncInMemoryCVMetadataRepository,
)
from tests.utils.mock_api_response_factory import MockApiResponseFactory
from tests.utils.pdf_test_utils import create_minimal_valid_pdf


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
def usecase_and_repo():
    logger_service = LoggerService()
    async_cv_repo = AsyncInMemoryCVMetadataRepository()
    query_builder = QueryBuilder()

    # Utiliser les factories pour créer les mocks
    ocr_mock = create_ocr_mock()
    text_formatter_mock = create_text_formatter_mock()

    usecase = ProcessUploadedCVUsecase(
        ocr=ocr_mock,
        text_formatter=text_formatter_mock,
        query_builder=query_builder,
        async_cv_metadata_repository=async_cv_repo,
        logger=logger_service,
    )

    return usecase, async_cv_repo, ocr_mock, text_formatter_mock


@pytest.fixture
def pdf_content():
    return create_minimal_valid_pdf()


@pytest.fixture
def cv_metadata_initial():
    return create_cv_metadata_initial()


async def test_execute_with_valid_pdf_updates_cv_metadatas(
    usecase_and_repo,
    pdf_content,
    cv_metadata_initial,
):
    usecase, repo, _, _ = usecase_and_repo
    initial_cv, cv_id = cv_metadata_initial

    await repo.save(initial_cv)

    result = await usecase.execute(cv_id, pdf_content)
    assert isinstance(result, CVMetadata)
    assert result.status == CVStatus.COMPLETED


async def test_execute_cv_metadatas_not_found(usecase_and_repo, pdf_content):
    cv_id = UUID("00000000-0000-0000-0000-000000000000")

    usecase, _, _, _ = usecase_and_repo
    with pytest.raises(CVNotFoundError):
        await usecase.execute(cv_id, pdf_content)
