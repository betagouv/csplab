import pytest

from application.usecases.extract_text_usecase import ExtractTextUsecase


@pytest.mark.asyncio
async def test_extract_text(mock_pdf_extractor, sample_pdf_content):
    usecase = ExtractTextUsecase(mock_pdf_extractor)

    result = await usecase.execute(sample_pdf_content)

    mock_pdf_extractor.extract_text.assert_called_once_with(sample_pdf_content)
    assert result == "Sample extracted text"
