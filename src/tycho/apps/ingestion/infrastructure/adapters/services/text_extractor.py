"""Document text extractor service for content extraction."""

from typing import Any, Dict, Union

from core.entities.concours import Concours
from core.entities.corps import Corps
from core.entities.document import Document
from core.interfaces.entity_interface import IEntity
from core.services.text_extractor_interface import ITextExtractor


class TextExtractor(ITextExtractor):
    """Service for extracting text content and metadata from documents or entities."""

    def extract_content(self, source: Union[Document, IEntity]) -> str:
        """Extract text content from a document or clean entity."""
        if isinstance(source, Document):
            return self._extract_from_document(source)
        elif isinstance(source, Corps):
            return self._extract_from_corps(source)
        elif isinstance(source, Concours):
            return self._extract_from_concours(source)
        else:
            raise NotImplementedError(
                f"Content extraction not implemented for {type(source)}"
            )

    def extract_metadata(self, source: Union[Document, IEntity]) -> Dict[str, Any]:
        """Extract metadata from a document or clean entity."""
        if isinstance(source, Document):
            return self._extract_metadata_from_document(source)
        elif isinstance(source, Corps):
            return self._extract_metadata_from_corps(source)
        elif isinstance(source, Concours):
            return self._extract_metadata_from_concours(source)
        else:
            raise NotImplementedError(
                f"Metadata extraction not implemented for {type(source)}"
            )

    def _extract_from_document(self, document: Document) -> str:
        """Extract content from raw document."""
        raise NotImplementedError(
            f"Content extraction not implemented for document type {document.type}"
        )

    def _extract_from_corps(self, corps: Corps) -> str:
        """Extract content from Corps entity."""
        return corps.label.value

    def _extract_metadata_from_document(self, document: Document) -> Dict[str, Any]:
        """Extract metadata from raw document."""
        raise NotImplementedError(
            f"Metadata extraction not implemented for document type {document.type}"
        )

    def _extract_metadata_from_corps(self, corps: Corps) -> Dict[str, Any]:
        """Extract metadata from Corps entity."""
        return {
            "category": corps.category.value if corps.category else None,
            "access_mod": [am.value for am in corps.access_modalities],
            "ministry": corps.ministry.value,
        }

    def _extract_from_concours(self, concours: Concours) -> str:
        """Extract content from Concours entity."""
        return f"{concours.corps} {concours.grade}".strip()

    def _extract_metadata_from_concours(self, concours: Concours) -> Dict[str, Any]:
        """Extract metadata from Concours entity."""
        return {
            "category": concours.category.value,
            "ministry": concours.ministry.value,
            "access_modality": [am.value for am in concours.access_modality],
        }
