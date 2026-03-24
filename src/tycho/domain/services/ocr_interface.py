from typing import Protocol


class IOCR(Protocol):
    async def extract_text(self, pdf_content: bytes) -> str: ...
