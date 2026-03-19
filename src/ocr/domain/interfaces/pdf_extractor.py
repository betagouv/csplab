from typing import Protocol


class IPDFTextExtractor(Protocol):
    async def extract_text(self, pdf_content: bytes) -> str: ...
