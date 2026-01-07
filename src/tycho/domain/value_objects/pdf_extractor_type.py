"""PDF extractor type value object."""

from enum import Enum


class PDFExtractorType(Enum):
    """Enum for PDF extractor implementation types."""

    OPENAI = "openai"
    ALBERT = "albert"

    def __str__(self):
        """Return string representation."""
        return self.value
