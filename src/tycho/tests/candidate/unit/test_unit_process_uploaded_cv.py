"""Unit test cases for ProcessUploadedCVUsecase."""

import pytest

from domain.exceptions.cv_errors import InvalidPDFError


@pytest.mark.parametrize(
    "container_name", ["albert_candidate_container", "openai_candidate_container"]
)
@pytest.mark.asyncio
async def test_execute_with_invalid_pdf_raises_invalid_pdf_error(
    request, container_name
):
    """Test that invalid PDF content raises InvalidPDFError."""
    container = request.getfixturevalue(container_name)

    pdf_content = b"This is not a PDF file"
    filename = "invalid.pdf"

    usecase = container.process_uploaded_cv_usecase()

    with pytest.raises(InvalidPDFError) as exc_info:
        await usecase.execute(filename, pdf_content)

    assert exc_info.value.filename == filename
    cv_repo = container.async_cv_metadata_repository()
    assert cv_repo.count() == 0


@pytest.mark.parametrize(
    "container_name", ["albert_candidate_container", "openai_candidate_container"]
)
@pytest.mark.asyncio
async def test_execute_with_empty_pdf_raises_invalid_pdf_error(request, container_name):
    """Test that empty PDF content raises InvalidPDFError."""
    container = request.getfixturevalue(container_name)

    pdf_content = b""
    filename = "empty.pdf"

    usecase = container.process_uploaded_cv_usecase()

    with pytest.raises(InvalidPDFError) as exc_info:
        await usecase.execute(filename, pdf_content)

    assert exc_info.value.filename == filename
    cv_repo = container.async_cv_metadata_repository()
    assert cv_repo.count() == 0
