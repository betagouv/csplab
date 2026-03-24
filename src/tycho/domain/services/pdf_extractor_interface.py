from typing import Protocol

from domain.value_objects.cv_extraction_types import CVExtractionResult


class IPDFTextExtractor(Protocol):
    async def extract_text(self, pdf_content: bytes) -> CVExtractionResult: ...
