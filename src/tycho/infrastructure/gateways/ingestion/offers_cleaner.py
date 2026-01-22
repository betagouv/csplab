"""Offers cleaner adapter."""

from typing import List

from domain.entities.document import Document, DocumentType
from domain.entities.offer import Offer
from domain.exceptions.document_error import InvalidDocumentTypeError
from domain.services.document_cleaner_interface import IDocumentCleaner
from domain.services.logger_interface import ILogger


class OffersCleaner(IDocumentCleaner[Offer]):
    """Adapter for cleaning raw documents of type OFFERS into Offers entities."""

    def __init__(self, logger: ILogger):
        """Initialize with logger dependency."""
        self.logger = logger.get_logger("OffersCleaner::clean")

    def clean(self, raw_documents: List[Document]) -> List[Offer]:
        """Clean raw documents and return Offers entities."""
        if not raw_documents:
            return []

        for document in raw_documents:
            if document.type != DocumentType.OFFERS:
                raise InvalidDocumentTypeError(document.type.value)

        # TODO: Implement actual cleaning logic for TalentSoft offers
        self.logger.info(
            f"Processing {len(raw_documents)} offer documents (not implemented yet)"
        )
        return []
