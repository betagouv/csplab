"""PDF text extractor interface for CV content extraction."""

from typing import Any, Dict, Protocol


class IPDFTextExtractor(Protocol):
    """Interface for extracting structured content from PDF files."""

    def extract_text(self, pdf_content: bytes) -> Dict[str, Any]:
        """Extract structured content from PDF bytes.

        Args:
            pdf_content: PDF file content as bytes

        Returns:
            Structured data as dict with format:
            {
                "experiences": [
                    {
                        "title": str,
                        "company": str,
                        "sector": str|None,
                        "description": str
                    }
                ],
                "skills": [str]
            }

        Raises:
            ValueError: If PDF content is invalid or corrupted
        """
        ...

    def validate_pdf(self, pdf_content: bytes, max_size_mb: int = 5) -> bool:
        """Validate PDF format and size.

        Args:
            pdf_content: PDF file content as bytes
            max_size_mb: Maximum allowed file size in MB (default 5MB)

        Returns:
            True if PDF is valid, False otherwise
        """
        ...
