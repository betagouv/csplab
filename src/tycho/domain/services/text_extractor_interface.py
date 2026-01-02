"""Text extractor interface for content extraction."""

from typing import Any, Dict, Protocol, Union

from domain.entities.document import Document
from domain.interfaces.entity_interface import IEntity


class ITextExtractor(Protocol):
    """Interface for extracting text content from documents or clean entities."""

    def extract_content(self, source: Union[Document, IEntity]) -> str:
        """Extract text content from a document or clean entity."""
        ...

    def extract_metadata(self, source: Union[Document, IEntity]) -> Dict[str, Any]:
        """Extract metadata from a document or clean entity."""
        ...
