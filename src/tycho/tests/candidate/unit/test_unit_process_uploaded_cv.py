from uuid import UUID

import pytest

from domain.entities.cv_metadata import CVMetadata
from domain.exceptions.cv_errors import CVNotFoundError
from domain.value_objects.cv_processing_status import CVStatus
from infrastructure.exceptions.exceptions import ExternalApiError
from tests.utils.mock_api_response_factory import MockApiResponseFactory


async def test_execute_with_valid_pdf_updates_cv_metadatas(
    httpx_mock,
    albert_candidate_container,
    pdf_content,
    cv_metadata_initial,
    test_app_config,
):
    container = albert_candidate_container

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


async def test_execute_cv_metadatas_not_found(albert_candidate_container, pdf_content):
    container = albert_candidate_container
    cv_id = UUID("00000000-0000-0000-0000-000000000000")  # UUID that doesn't exist

    usecase = container.process_uploaded_cv_usecase()
    with pytest.raises(CVNotFoundError):
        await usecase.execute(cv_id, pdf_content)


async def test_execute_ocr_error(
    httpx_mock,
    albert_candidate_container,
    pdf_content,
    cv_metadata_initial,
    test_app_config,
):
    container = albert_candidate_container

    # Mock OCR service failure
    httpx_mock.add_response(
        method="POST",
        url=f"{test_app_config.ocr.base_url}extract-text",
        json={"error": "Internal server error"},
        status_code=500,
    )

    initial_cv, cv_id = cv_metadata_initial

    # Prepopulate the repository
    repo = container.async_cv_metadata_repository()
    await repo.save(initial_cv)

    usecase = container.process_uploaded_cv_usecase()

    with pytest.raises(ExternalApiError):
        await usecase.execute(cv_id, pdf_content)

    updated_cv = await repo.find_by_id(cv_id)
    assert updated_cv is not None
    assert updated_cv.status == CVStatus.FAILED


async def test_execute_json_decode_error_with_details(
    httpx_mock,
    albert_candidate_container,
    pdf_content,
    cv_metadata_initial,
    test_app_config,
):
    container = albert_candidate_container

    # Mock OCR service response (valid)
    ocr_response = MockApiResponseFactory.create_ocr_service_response()
    httpx_mock.add_response(
        method="POST",
        url=f"{test_app_config.ocr.base_url}extract-text",
        json=ocr_response,
        status_code=200,
    )

    # Mock Albert text formatter with invalid JSON
    invalid_json_content = '{"experiences": [invalid json here'
    invalid_albert_response = {
        "id": "chatcmpl-test123",
        "object": "chat.completion",
        "created": 1774004024,
        "model": "openweight-large",
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": invalid_json_content,
                    "refusal": None,
                    "annotations": None,
                    "audio": None,
                    "function_call": None,
                    "tool_calls": [],
                    "reasoning": None,
                },
                "finish_reason": "stop",
            }
        ],
        "usage": {
            "prompt_tokens": 1262,
            "completion_tokens": 432,
            "total_tokens": 1694,
            "cost": 0.0,
            "carbon": {
                "kWh": {"min": 0.022736131127999996, "max": 0.026871822072},
                "kgCO2eq": {
                    "min": 0.013437987405148953,
                    "max": 0.015880021922380184,
                },
            },
            "requests": 1,
        },
    }

    httpx_mock.add_response(
        method="POST",
        url=f"{test_app_config.albert.api_base_url}v1/chat/completions",
        json=invalid_albert_response,
        status_code=200,
    )

    # Unpack fixture data
    initial_cv, cv_id = cv_metadata_initial

    # Prepopulate the repository
    repo = container.async_cv_metadata_repository()
    await repo.save(initial_cv)

    usecase = container.process_uploaded_cv_usecase()

    with pytest.raises(ExternalApiError) as exc_info:
        await usecase.execute(cv_id, pdf_content)

    # Verify the error message contains detailed JSON parsing information
    error_message = str(exc_info.value)
    assert "Failed to parse JSON from Albert completion response" in error_message
