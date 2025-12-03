"""Text extractor interface for document content extraction."""

from typing import Any, Dict, Protocol

from core.entities.document import Document


class ITextExtractor(Protocol):
    """Interface for extracting text content from documents."""

    def extract_content(self, document: Document) -> str:
        """Extract text content from a document based on its type."""
        ...

    def extract_metadata(self, document: Document) -> Dict[str, Any]:
        """Extract metadata from a document based on its type."""
        ...
