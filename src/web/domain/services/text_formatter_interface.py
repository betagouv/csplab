from typing import Protocol

from domain.value_objects.cv_extraction_types import CVExtractionResult


class ITextFormatter(Protocol):
    async def format_text(self, extracted_text: str) -> CVExtractionResult: ...
