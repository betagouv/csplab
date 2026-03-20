from typing import Protocol


class IPDFValidator(Protocol):
    async def validate_pdf(self, content: bytes) -> bool: ...
