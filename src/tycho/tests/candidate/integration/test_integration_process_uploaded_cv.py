from http import HTTPStatus
from typing import Any, Dict
from uuid import UUID

import pytest

from config.app_config import AppConfig
from domain.entities.cv_metadata import CVMetadata
from domain.exceptions.cv_errors import CVNotFoundError
from domain.value_objects.cv_processing_status import CVStatus
from infrastructure.di.candidate.candidate_container import CandidateContainer
from infrastructure.di.shared.shared_container import SharedContainer
from infrastructure.exceptions.exceptions import ExternalApiError
from infrastructure.gateways.shared.logger import LoggerService
from tests.factories.cv_metadata_factory import create_cv_metadata_initial
from tests.utils.mock_api_response_factory import MockApiResponseFactory
from tests.utils.pdf_test_utils import create_minimal_valid_pdf


def mock_ocr_response(
    httpx_mock,
    config,
    ocr_response: Dict[str, Any] | None = None,
    status_code: int = 200,
):
    if not ocr_response:
        ocr_response = MockApiResponseFactory.create_ocr_service_response()

    httpx_mock.add_response(
        method="POST",
        url=f"{config.ocr.base_url}extract-text",
        json=ocr_response,
        status_code=status_code,
    )


def mock_llm_response(
    httpx_mock,
    config,
    llm_response: Dict[str, Any] | None = None,
    status_code: int = 200,
):
    if not llm_response:
        llm_response = MockApiResponseFactory.create_formatter_response()

    httpx_mock.add_response(
        method="POST",
        url=f"{config.albert.api_base_url}v1/chat/completions",
        json=llm_response,
        status_code=status_code,
    )


@pytest.fixture
def candidate_container():
    container = CandidateContainer()

    shared_container = SharedContainer()

    app_config = AppConfig.from_django_settings()
    shared_container.app_config.override(app_config)

    logger_service = LoggerService()
    shared_container.logger_service.override(logger_service)

    container.shared_container.override(shared_container)

    container.app_config.override(app_config)
    container.logger_service.override(logger_service)

    return container


@pytest.fixture
def test_app_config(candidate_container):
    return candidate_container.app_config()


@pytest.fixture
def pdf_content():
    return create_minimal_valid_pdf()


@pytest.fixture
def cv_metadata_initial():
    return create_cv_metadata_initial()


@pytest.fixture
def usecase_and_repo(candidate_container):
    usecase = candidate_container.process_uploaded_cv_usecase()
    repo = candidate_container.async_cv_metadata_repository()
    return usecase, repo


async def test_execute_with_valid_pdf_updates_cv_metadatas(
    db,
    httpx_mock,
    candidate_container,
    pdf_content,
    cv_metadata_initial,
    test_app_config,
):

    mock_ocr_response(httpx_mock, test_app_config)
    mock_llm_response(httpx_mock, test_app_config)

    # Unpack fixture data
    initial_cv, cv_id = cv_metadata_initial

    # Prepopulate the repository
    repo = candidate_container.async_cv_metadata_repository()
    await repo.save(initial_cv)

    usecase = candidate_container.process_uploaded_cv_usecase()

    result = await usecase.execute(cv_id, pdf_content)
    assert isinstance(result, CVMetadata)
    assert result.status == CVStatus.COMPLETED


async def test_execute_cv_metadatas_not_found(candidate_container, db, pdf_content):
    cv_id = UUID("00000000-0000-0000-0000-000000000000")  # UUID that doesn't exist

    usecase = candidate_container.process_uploaded_cv_usecase()
    with pytest.raises(CVNotFoundError):
        await usecase.execute(cv_id, pdf_content)


async def test_execute_with_api_failure_saves_failed_status_to_database(
    db,
    httpx_mock,
    candidate_container,
    pdf_content,
    cv_metadata_initial,
    test_app_config,
):

    # Mock OCR service failure
    mock_ocr_response(
        httpx_mock,
        test_app_config,
        ocr_response={"error": "OCR Service Error"},
        status_code=500,
    )

    # Unpack fixture data
    initial_cv, cv_id = cv_metadata_initial

    # Prepopulate the repository with PENDING status
    repo = candidate_container.async_cv_metadata_repository()
    await repo.save(initial_cv)

    usecase = candidate_container.process_uploaded_cv_usecase()

    with pytest.raises(ExternalApiError):
        await usecase.execute(cv_id, pdf_content)

    # Verify that CV metadata was saved with FAILED status
    updated_cv = await repo.find_by_id(cv_id)
    assert updated_cv is not None
    assert updated_cv.status == CVStatus.FAILED
    assert updated_cv.updated_at > initial_cv.updated_at


async def test_execute_albert_fenced_json_response_success(
    db,
    httpx_mock,
    candidate_container,
    pdf_content,
    cv_metadata_initial,
    test_app_config,
):

    # Mock OCR service success
    mock_ocr_response(httpx_mock, test_app_config)

    # Mock Albert response with fenced JSON
    albert_fenced_response = (
        MockApiResponseFactory.create_formatter_fenced_json_response()
    )
    mock_llm_response(
        httpx_mock,
        test_app_config,
        llm_response=albert_fenced_response,
    )

    # Unpack fixture data
    initial_cv, cv_id = cv_metadata_initial

    # Prepopulate the repository
    repo = candidate_container.async_cv_metadata_repository()
    await repo.save(initial_cv)

    usecase = candidate_container.process_uploaded_cv_usecase()

    result = await usecase.execute(cv_id, pdf_content)
    assert isinstance(result, CVMetadata)
    assert result.status == CVStatus.COMPLETED


async def test_execute_albert_http_error_with_valid_error_response(
    db,
    httpx_mock,
    usecase_and_repo,
    pdf_content,
    cv_metadata_initial,
    test_app_config,
):
    mock_ocr_response(httpx_mock, test_app_config)

    albert_error_response = MockApiResponseFactory.create_formatter_error_response()
    mock_llm_response(
        httpx_mock,
        test_app_config,
        llm_response=albert_error_response,
        status_code=HTTPStatus.UNAUTHORIZED,
    )

    usecase, repo = usecase_and_repo
    initial_cv, cv_id = cv_metadata_initial

    await repo.save(initial_cv)

    with pytest.raises(ExternalApiError) as exc_info:
        await usecase.execute(cv_id, pdf_content)

    error_message = str(exc_info.value)
    assert "Invalid API key provided" in error_message
    assert exc_info.value.status_code == HTTPStatus.UNAUTHORIZED


async def test_execute_albert_invalid_response_structure(
    db,
    httpx_mock,
    usecase_and_repo,
    pdf_content,
    cv_metadata_initial,
    test_app_config,
):
    mock_ocr_response(httpx_mock, test_app_config)

    albert_invalid_response = MockApiResponseFactory.create_formatter_invalid_response()
    mock_llm_response(
        httpx_mock,
        test_app_config,
        llm_response=albert_invalid_response,
    )

    usecase, repo = usecase_and_repo
    initial_cv, cv_id = cv_metadata_initial

    await repo.save(initial_cv)

    with pytest.raises(ExternalApiError) as exc_info:
        await usecase.execute(cv_id, pdf_content)

    error_message = str(exc_info.value)
    assert "Invalid Albert completion response structure" in error_message


async def test_execute_albert_empty_choices_response(
    db,
    httpx_mock,
    usecase_and_repo,
    pdf_content,
    cv_metadata_initial,
    test_app_config,
):
    mock_ocr_response(httpx_mock, test_app_config)

    albert_empty_choices_response = (
        MockApiResponseFactory.create_formatter_empty_choices_response()
    )
    mock_llm_response(
        httpx_mock,
        test_app_config,
        llm_response=albert_empty_choices_response,
    )

    usecase, repo = usecase_and_repo
    initial_cv, cv_id = cv_metadata_initial

    await repo.save(initial_cv)

    with pytest.raises(ExternalApiError) as exc_info:
        await usecase.execute(cv_id, pdf_content)

    error_message = str(exc_info.value)
    assert "No completion choices returned from Albert API" in error_message


async def test_execute_albert_invalid_fenced_json_response(
    db,
    httpx_mock,
    usecase_and_repo,
    pdf_content,
    cv_metadata_initial,
    test_app_config,
):
    mock_ocr_response(httpx_mock, test_app_config)

    albert_invalid_fenced_response = (
        MockApiResponseFactory.create_formatter_invalid_fenced_json_response()
    )
    mock_llm_response(
        httpx_mock,
        test_app_config,
        llm_response=albert_invalid_fenced_response,
    )

    usecase, repo = usecase_and_repo
    initial_cv, cv_id = cv_metadata_initial

    await repo.save(initial_cv)

    with pytest.raises(ExternalApiError) as exc_info:
        await usecase.execute(cv_id, pdf_content)

    error_message = str(exc_info.value)
    assert "Failed to parse JSON from Albert completion response" in error_message


async def test_execute_ocr_http_error_with_valid_error_response(
    db,
    httpx_mock,
    usecase_and_repo,
    pdf_content,
    cv_metadata_initial,
    test_app_config,
):
    ocr_error_response = MockApiResponseFactory.create_ocr_service_error_response()
    mock_ocr_response(
        httpx_mock,
        test_app_config,
        ocr_response=ocr_error_response,
        status_code=HTTPStatus.BAD_REQUEST,
    )

    usecase, repo = usecase_and_repo
    initial_cv, cv_id = cv_metadata_initial

    await repo.save(initial_cv)

    with pytest.raises(ExternalApiError) as exc_info:
        await usecase.execute(cv_id, pdf_content)

    error_message = str(exc_info.value)
    assert "Invalid file format or corrupted PDF" in error_message
    assert exc_info.value.status_code == HTTPStatus.BAD_REQUEST


async def test_execute_ocr_http_error_with_invalid_error_response(
    db,
    httpx_mock,
    usecase_and_repo,
    pdf_content,
    cv_metadata_initial,
    test_app_config,
):
    mock_ocr_response(
        httpx_mock,
        test_app_config,
        ocr_response={"unexpected": "error format"},
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
    )

    usecase, repo = usecase_and_repo
    initial_cv, cv_id = cv_metadata_initial

    await repo.save(initial_cv)

    with pytest.raises(ExternalApiError) as exc_info:
        await usecase.execute(cv_id, pdf_content)

    error_message = str(exc_info.value)
    assert "OCR service error: 500" in error_message
    assert exc_info.value.status_code == HTTPStatus.INTERNAL_SERVER_ERROR


async def test_execute_ocr_invalid_success_response_structure(
    db,
    httpx_mock,
    usecase_and_repo,
    pdf_content,
    cv_metadata_initial,
    test_app_config,
):
    ocr_invalid_response = MockApiResponseFactory.create_ocr_service_invalid_response()
    mock_ocr_response(
        httpx_mock,
        test_app_config,
        ocr_response=ocr_invalid_response,
    )

    usecase, repo = usecase_and_repo
    initial_cv, cv_id = cv_metadata_initial

    await repo.save(initial_cv)

    with pytest.raises(ExternalApiError) as exc_info:
        await usecase.execute(cv_id, pdf_content)

    error_message = str(exc_info.value)
    assert "Failed to parse JSON response" in error_message
