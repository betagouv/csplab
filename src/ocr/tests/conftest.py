from unittest.mock import Mock

import pytest

from domain.interfaces.pdf_extractor import IPDFTextExtractor


@pytest.fixture
def mock_pdf_extractor():
    mock = Mock(spec=IPDFTextExtractor)
    mock.extract_text.return_value = "Sample extracted text"
    return mock


@pytest.fixture
def sample_pdf_content():
    return b"fake pdf content for testing"
