"""Corps cleaner adapter."""

from typing import List

from core.entities.corps import Corps
from core.entities.document import Document, DocumentType
from core.errors.domain_errors import InvalidDocumentTypeError
from core.services.logger_interface import ILogger
from core.value_objects.access_modality import AccessModality
from core.value_objects.category import Category
from core.value_objects.diploma import Diploma
from core.value_objects.label import Label
from core.value_objects.ministry import Ministry


class CorpsCleaner:
    """Adapter for cleaning raw documents into Corps entities."""

    def __init__(self, logger: ILogger):
        """Initialize with logger dependency."""
        self.logger = logger

    def clean(self, raw_documents: List[Document]) -> List[Corps]:
        """Clean raw documents and return Corps entities."""
        for document in raw_documents:
            if document.type != DocumentType.CORPS:
                raise InvalidDocumentTypeError(document.type.value)

        corps_list = []

        for document in raw_documents:
            try:
                corps = self._transform_to_corps(document)
                corps_list.append(corps)
            except Exception as e:
                # Log error but continue processing other documents
                logger_instance = self.logger.get_logger("CorpsCleaner::clean")
                logger_instance.error(f"Error processing document {document.id}: {e}")
                continue

        return corps_list

    def _transform_to_corps(self, document: Document) -> Corps:
        """Transform a raw document into a Corps entity."""
        # raw_data = document.raw_data

        # Extract and clean data from raw document

        # Create value objects
        # TODO implement mappers for these value objects

        return Corps(
            id=1,
            code="123",
            category=Category.A,
            ministry=Ministry.MEN,
            diploma=Diploma(value=4),
            access_modalities=[AccessModality.CONCOURS_EXTERNE],
            label=Label(
                short_value="PROF LYCE PROF AGRI",
                value="Professeurs de lycée professionnel agricole",
            ),
        )
