from http import HTTPStatus
from uuid import UUID

import pytest

from domain.entities.cv_metadata import CVMetadata
from domain.exceptions.cv_errors import CVNotFoundError
from domain.value_objects.cv_processing_status import CVStatus
from infrastructure.exceptions.exceptions import ExternalApiError
from tests.utils.mock_api_response_factory import MockApiResponseFactory


@pytest.mark.django_db
async def test_execute_with_valid_pdf_updates_cv_metadatas(
    httpx_mock,
    albert_integration_container,
    pdf_content,
    cv_metadata_initial,
    test_app_config,
):
    container = albert_integration_container

    # Mock OCR service response
    ocr_response = MockApiResponseFactory.create_ocr_service_response()

    httpx_mock.add_response(
        method="POST",
        url=f"{test_app_config.ocr.base_url}extract-text",
        json=ocr_response,
        status_code=200,
    )

    # Mock Albert text formatter response
    albert_response = MockApiResponseFactory.create_albert_formatter_response()

    httpx_mock.add_response(
        method="POST",
        url=f"{test_app_config.albert.api_base_url}v1/chat/completions",
        json=albert_response,
        status_code=200,
    )

    # Unpack fixture data
    initial_cv, cv_id = cv_metadata_initial

    # Prepopulate the repository
    repo = container.async_cv_metadata_repository()
    await repo.save(initial_cv)

    usecase = container.process_uploaded_cv_usecase()

    result = await usecase.execute(cv_id, pdf_content)
    assert isinstance(result, CVMetadata)
    assert result.status == CVStatus.COMPLETED


@pytest.mark.django_db
async def test_execute_cv_metadatas_not_found(
    albert_integration_container, pdf_content
):
    container = albert_integration_container
    cv_id = UUID("00000000-0000-0000-0000-000000000000")  # UUID that doesn't exist

    usecase = container.process_uploaded_cv_usecase()
    with pytest.raises(CVNotFoundError):
        await usecase.execute(cv_id, pdf_content)


@pytest.mark.django_db
async def test_execute_with_api_failure_saves_failed_status_to_database(
    httpx_mock,
    albert_integration_container,
    pdf_content,
    cv_metadata_initial,
    test_app_config,
):
    container = albert_integration_container

    # Mock OCR service failure
    httpx_mock.add_response(
        method="POST",
        url=f"{test_app_config.ocr.base_url}extract-text",
        json={"error": "OCR Service Error"},
        status_code=500,
    )

    # Unpack fixture data
    initial_cv, cv_id = cv_metadata_initial

    # Prepopulate the repository with PENDING status
    repo = container.async_cv_metadata_repository()
    await repo.save(initial_cv)

    usecase = container.process_uploaded_cv_usecase()

    with pytest.raises(ExternalApiError):
        await usecase.execute(cv_id, pdf_content)

    # Verify that CV metadata was saved with FAILED status
    updated_cv = await repo.find_by_id(cv_id)
    assert updated_cv is not None
    assert updated_cv.status == CVStatus.FAILED
    assert updated_cv.updated_at > initial_cv.updated_at


@pytest.mark.django_db
async def test_execute_albert_http_error_with_valid_error_response(
    httpx_mock,
    albert_integration_container,
    pdf_content,
    cv_metadata_initial,
    test_app_config,
):
    container = albert_integration_container

    # Mock OCR service success
    ocr_response = MockApiResponseFactory.create_ocr_service_response()
    httpx_mock.add_response(
        method="POST",
        url=f"{test_app_config.ocr.base_url}extract-text",
        json=ocr_response,
        status_code=HTTPStatus.OK,
    )

    # Mock Albert HTTP error with valid error response
    albert_error_response = (
        MockApiResponseFactory.create_albert_formatter_error_response()
    )
    httpx_mock.add_response(
        method="POST",
        url=f"{test_app_config.albert.api_base_url}v1/chat/completions",
        json=albert_error_response,
        status_code=HTTPStatus.UNAUTHORIZED,
    )

    # Unpack fixture data
    initial_cv, cv_id = cv_metadata_initial

    # Prepopulate the repository
    repo = container.async_cv_metadata_repository()
    await repo.save(initial_cv)

    usecase = container.process_uploaded_cv_usecase()

    with pytest.raises(ExternalApiError) as exc_info:
        await usecase.execute(cv_id, pdf_content)

    error_message = str(exc_info.value)
    assert "Invalid API key provided" in error_message
    assert exc_info.value.status_code == HTTPStatus.UNAUTHORIZED


@pytest.mark.django_db
async def test_execute_albert_http_error_with_invalid_error_response(
    httpx_mock,
    albert_integration_container,
    pdf_content,
    cv_metadata_initial,
    test_app_config,
):
    container = albert_integration_container

    # Mock OCR service success
    ocr_response = MockApiResponseFactory.create_ocr_service_response()
    httpx_mock.add_response(
        method="POST",
        url=f"{test_app_config.ocr.base_url}extract-text",
        json=ocr_response,
        status_code=200,
    )

    # Mock Albert HTTP error with invalid error response
    httpx_mock.add_response(
        method="POST",
        url=f"{test_app_config.albert.api_base_url}v1/chat/completions",
        json={"unexpected": "error format"},
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
    )

    # Unpack fixture data
    initial_cv, cv_id = cv_metadata_initial

    # Prepopulate the repository
    repo = container.async_cv_metadata_repository()
    await repo.save(initial_cv)

    usecase = container.process_uploaded_cv_usecase()

    with pytest.raises(ExternalApiError) as exc_info:
        await usecase.execute(cv_id, pdf_content)

    error_message = str(exc_info.value)
    assert "Albert completion API error: 500" in error_message
    assert exc_info.value.status_code == HTTPStatus.INTERNAL_SERVER_ERROR


@pytest.mark.django_db
async def test_execute_albert_invalid_response_structure(
    httpx_mock,
    albert_integration_container,
    pdf_content,
    cv_metadata_initial,
    test_app_config,
):
    container = albert_integration_container

    # Mock OCR service success
    ocr_response = MockApiResponseFactory.create_ocr_service_response()
    httpx_mock.add_response(
        method="POST",
        url=f"{test_app_config.ocr.base_url}extract-text",
        json=ocr_response,
        status_code=HTTPStatus.OK,
    )

    # Mock Albert invalid response structure
    albert_invalid_response = (
        MockApiResponseFactory.create_albert_formatter_invalid_response()
    )
    httpx_mock.add_response(
        method="POST",
        url=f"{test_app_config.albert.api_base_url}v1/chat/completions",
        json=albert_invalid_response,
        status_code=HTTPStatus.OK,
    )

    # Unpack fixture data
    initial_cv, cv_id = cv_metadata_initial

    # Prepopulate the repository
    repo = container.async_cv_metadata_repository()
    await repo.save(initial_cv)

    usecase = container.process_uploaded_cv_usecase()

    with pytest.raises(ExternalApiError) as exc_info:
        await usecase.execute(cv_id, pdf_content)

    error_message = str(exc_info.value)
    assert "Invalid Albert completion response structure" in error_message


@pytest.mark.django_db
async def test_execute_albert_empty_choices_response(
    httpx_mock,
    albert_integration_container,
    pdf_content,
    cv_metadata_initial,
    test_app_config,
):
    container = albert_integration_container

    # Mock OCR service success
    ocr_response = MockApiResponseFactory.create_ocr_service_response()
    httpx_mock.add_response(
        method="POST",
        url=f"{test_app_config.ocr.base_url}extract-text",
        json=ocr_response,
        status_code=HTTPStatus.OK,
    )

    # Mock Albert response with empty choices
    albert_empty_choices_response = (
        MockApiResponseFactory.create_albert_formatter_empty_choices_response()
    )
    httpx_mock.add_response(
        method="POST",
        url=f"{test_app_config.albert.api_base_url}v1/chat/completions",
        json=albert_empty_choices_response,
        status_code=HTTPStatus.OK,
    )

    # Unpack fixture data
    initial_cv, cv_id = cv_metadata_initial

    # Prepopulate the repository
    repo = container.async_cv_metadata_repository()
    await repo.save(initial_cv)

    usecase = container.process_uploaded_cv_usecase()

    with pytest.raises(ExternalApiError) as exc_info:
        await usecase.execute(cv_id, pdf_content)

    error_message = str(exc_info.value)
    assert "No completion choices returned from Albert API" in error_message


@pytest.mark.django_db
async def test_execute_albert_fenced_json_response_success(
    httpx_mock,
    albert_integration_container,
    pdf_content,
    cv_metadata_initial,
    test_app_config,
):
    container = albert_integration_container

    # Mock OCR service success
    ocr_response = MockApiResponseFactory.create_ocr_service_response()
    httpx_mock.add_response(
        method="POST",
        url=f"{test_app_config.ocr.base_url}extract-text",
        json=ocr_response,
        status_code=HTTPStatus.OK,
    )

    # Mock Albert response with fenced JSON
    albert_fenced_response = (
        MockApiResponseFactory.create_albert_formatter_fenced_json_response()
    )
    httpx_mock.add_response(
        method="POST",
        url=f"{test_app_config.albert.api_base_url}v1/chat/completions",
        json=albert_fenced_response,
        status_code=HTTPStatus.OK,
    )

    # Unpack fixture data
    initial_cv, cv_id = cv_metadata_initial

    # Prepopulate the repository
    repo = container.async_cv_metadata_repository()
    await repo.save(initial_cv)

    usecase = container.process_uploaded_cv_usecase()

    result = await usecase.execute(cv_id, pdf_content)
    assert isinstance(result, CVMetadata)
    assert result.status == CVStatus.COMPLETED


@pytest.mark.django_db
async def test_execute_albert_invalid_fenced_json_response(
    httpx_mock,
    albert_integration_container,
    pdf_content,
    cv_metadata_initial,
    test_app_config,
):
    container = albert_integration_container

    # Mock OCR service success
    ocr_response = MockApiResponseFactory.create_ocr_service_response()
    httpx_mock.add_response(
        method="POST",
        url=f"{test_app_config.ocr.base_url}extract-text",
        json=ocr_response,
        status_code=HTTPStatus.OK,
    )

    # Mock Albert response with invalid fenced JSON
    albert_invalid_fenced_response = (
        MockApiResponseFactory.create_albert_formatter_invalid_fenced_json_response()
    )
    httpx_mock.add_response(
        method="POST",
        url=f"{test_app_config.albert.api_base_url}v1/chat/completions",
        json=albert_invalid_fenced_response,
        status_code=HTTPStatus.OK,
    )

    # Unpack fixture data
    initial_cv, cv_id = cv_metadata_initial

    # Prepopulate the repository
    repo = container.async_cv_metadata_repository()
    await repo.save(initial_cv)

    usecase = container.process_uploaded_cv_usecase()

    with pytest.raises(ExternalApiError) as exc_info:
        await usecase.execute(cv_id, pdf_content)

    error_message = str(exc_info.value)
    assert "Failed to parse JSON from Albert completion response" in error_message


@pytest.mark.django_db
async def test_execute_ocr_http_error_with_valid_error_response(
    httpx_mock,
    albert_integration_container,
    pdf_content,
    cv_metadata_initial,
    test_app_config,
):
    container = albert_integration_container

    # Mock OCR service HTTP error with valid error response
    ocr_error_response = MockApiResponseFactory.create_ocr_service_error_response()
    httpx_mock.add_response(
        method="POST",
        url=f"{test_app_config.ocr.base_url}extract-text",
        json=ocr_error_response,
        status_code=HTTPStatus.BAD_REQUEST,
    )

    # Unpack fixture data
    initial_cv, cv_id = cv_metadata_initial

    # Prepopulate the repository
    repo = container.async_cv_metadata_repository()
    await repo.save(initial_cv)

    usecase = container.process_uploaded_cv_usecase()

    with pytest.raises(ExternalApiError) as exc_info:
        await usecase.execute(cv_id, pdf_content)

    error_message = str(exc_info.value)
    assert "Invalid file format or corrupted PDF" in error_message
    assert exc_info.value.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.django_db
async def test_execute_ocr_http_error_with_invalid_error_response(
    httpx_mock,
    albert_integration_container,
    pdf_content,
    cv_metadata_initial,
    test_app_config,
):
    container = albert_integration_container

    # Mock OCR service HTTP error with invalid error response (line 38)
    httpx_mock.add_response(
        method="POST",
        url=f"{test_app_config.ocr.base_url}extract-text",
        json={"unexpected": "error format"},
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
    )

    # Unpack fixture data
    initial_cv, cv_id = cv_metadata_initial

    # Prepopulate the repository
    repo = container.async_cv_metadata_repository()
    await repo.save(initial_cv)

    usecase = container.process_uploaded_cv_usecase()

    with pytest.raises(ExternalApiError) as exc_info:
        await usecase.execute(cv_id, pdf_content)

    error_message = str(exc_info.value)
    assert "OCR service error: 500" in error_message
    assert exc_info.value.status_code == HTTPStatus.INTERNAL_SERVER_ERROR


@pytest.mark.django_db
async def test_execute_ocr_invalid_success_response_structure(
    httpx_mock,
    albert_integration_container,
    pdf_content,
    cv_metadata_initial,
    test_app_config,
):
    container = albert_integration_container

    # Mock OCR service with invalid success response structure (lines 58-59)
    ocr_invalid_response = MockApiResponseFactory.create_ocr_service_invalid_response()
    httpx_mock.add_response(
        method="POST",
        url=f"{test_app_config.ocr.base_url}extract-text",
        json=ocr_invalid_response,
        status_code=HTTPStatus.OK,
    )

    # Unpack fixture data
    initial_cv, cv_id = cv_metadata_initial

    # Prepopulate the repository
    repo = container.async_cv_metadata_repository()
    await repo.save(initial_cv)

    usecase = container.process_uploaded_cv_usecase()

    with pytest.raises(ExternalApiError) as exc_info:
        await usecase.execute(cv_id, pdf_content)

    error_message = str(exc_info.value)
    assert "Failed to parse JSON response" in error_message
