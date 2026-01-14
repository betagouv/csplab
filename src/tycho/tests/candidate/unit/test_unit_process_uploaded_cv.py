"""Unit test cases for ProcessUploadedCVUsecase."""

import pytest

from domain.exceptions.cv_errors import InvalidPDFError

# Test constants
EXPECTED_EXPERIENCES_COUNT = 1
EXPECTED_SKILLS_COUNT = 2


@pytest.mark.asyncio
async def test_execute_with_invalid_pdf_raises_invalid_pdf_error(
    request, extractor_config
):
    """Test that invalid PDF content raises InvalidPDFError."""
    pdf_content = b"This is not a PDF file"
    filename = f"invalid_{extractor_config['type']}.pdf"

    usecase = request.getfixturevalue(extractor_config["usecase_fixture"])
    container = request.getfixturevalue(extractor_config["container_fixture"])

    with pytest.raises(InvalidPDFError) as exc_info:
        await usecase.execute(filename, pdf_content)

    assert exc_info.value.filename == filename
    cv_repo = container.async_cv_metadata_repository()
    assert cv_repo.count() == 0


@pytest.mark.asyncio
async def test_execute_with_empty_pdf_raises_invalid_pdf_error(
    request, extractor_config
):
    """Test that empty PDF content raises InvalidPDFError."""
    pdf_content = b""
    filename = f"empty_{extractor_config['type']}.pdf"

    usecase = request.getfixturevalue(extractor_config["usecase_fixture"])
    container = request.getfixturevalue(extractor_config["container_fixture"])

    with pytest.raises(InvalidPDFError) as exc_info:
        await usecase.execute(filename, pdf_content)

    assert exc_info.value.filename == filename
    cv_repo = container.async_cv_metadata_repository()
    assert cv_repo.count() == 0
